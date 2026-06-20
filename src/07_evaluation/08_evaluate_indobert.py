from pathlib import Path
import json
import logging
import sys

try:
    import numpy as np
    import pandas as pd
    import torch
    from sklearn.metrics import (
        accuracy_score,
        classification_report,
        confusion_matrix,
        precision_recall_fscore_support,
    )
    from torch.utils.data import DataLoader, TensorDataset
    from transformers import AutoConfig, AutoModelForSequenceClassification, AutoTokenizer
except ImportError as exc:
    print("\nDependensi Python belum lengkap untuk evaluasi IndoBERT.")
    print(f"Detail: {exc}")
    print("\nInstall dependensi terlebih dahulu:")
    print("python -m pip install -r requirements.txt")
    raise SystemExit(1)


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


ROOT_DIR = Path(__file__).resolve().parents[2]
DATASET_PATH = ROOT_DIR / "data" / "final" / "06_jakone_modeling_master_v3.csv"
MODEL_DIR = ROOT_DIR / "models" / "indobert_v3_baseline"
LABEL_MAPPING_PATH = MODEL_DIR / "label_mapping.json"
EVALUATION_DIR = ROOT_DIR / "outputs" / "evaluation" / "indobert_v3_baseline"

TEST_METRICS_PATH = EVALUATION_DIR / "test_metrics.json"
CLASSIFICATION_REPORT_PATH = EVALUATION_DIR / "classification_report.csv"
CONFUSION_MATRIX_PATH = EVALUATION_DIR / "confusion_matrix.csv"
PREDICTIONS_PATH = EVALUATION_DIR / "test_predictions.csv"

TEXT_COLUMN = "review"
LABEL_COLUMN = "label"
SPLIT_COLUMN = "split_set"
REQUIRED_COLUMNS = {TEXT_COLUMN, LABEL_COLUMN, SPLIT_COLUMN}

LABEL_ORDER = ["negatif", "netral", "positif"]
MAX_LENGTH = 128
BATCH_SIZE = 32

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def prepare_output_dirs() -> None:
    EVALUATION_DIR.mkdir(parents=True, exist_ok=True)


def get_device() -> torch.device:
    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        print(f"CUDA tersedia. Evaluation menggunakan GPU: {device_name}")
        return torch.device("cuda")

    print("WARNING: CUDA/GPU tidak tersedia. Evaluation di CPU bisa lebih lambat.")
    return torch.device("cpu")


def validate_inputs() -> None:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset v3 tidak ditemukan: {DATASET_PATH}")
    if not MODEL_DIR.exists():
        raise FileNotFoundError(f"Folder model tidak ditemukan: {MODEL_DIR}")
    if not LABEL_MAPPING_PATH.exists():
        raise FileNotFoundError(f"Label mapping tidak ditemukan: {LABEL_MAPPING_PATH}")


def load_label_mapping() -> tuple[dict[str, int], dict[int, str]]:
    logger.info("Membaca label mapping: %s", LABEL_MAPPING_PATH.relative_to(ROOT_DIR))
    with LABEL_MAPPING_PATH.open("r", encoding="utf-8") as file:
        mapping = json.load(file)

    label2id = {str(label).lower(): int(idx) for label, idx in mapping.get("label2id", {}).items()}
    expected = {"negatif": 0, "netral": 1, "positif": 2}
    if label2id != expected:
        raise ValueError("label_mapping.json harus berisi negatif=0, netral=1, positif=2.")
    id2label = {idx: label for label, idx in label2id.items()}
    return label2id, id2label


def load_test_data(label2id: dict[str, int]) -> pd.DataFrame:
    logger.info("Membaca dataset: %s", DATASET_PATH.relative_to(ROOT_DIR))
    df = pd.read_csv(DATASET_PATH)
    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(f"Kolom wajib tidak ditemukan: {', '.join(sorted(missing_columns))}")

    df = df.copy()
    df[TEXT_COLUMN] = df[TEXT_COLUMN].fillna("").astype(str).str.strip()
    df[LABEL_COLUMN] = df[LABEL_COLUMN].fillna("").astype(str).str.strip().str.lower()
    df[SPLIT_COLUMN] = df[SPLIT_COLUMN].fillna("").astype(str).str.strip().str.lower()

    test_df = df[df[SPLIT_COLUMN] == "test"].copy().reset_index(drop=True)
    if test_df.empty:
        raise ValueError("Data test kosong. Tidak ada baris dengan split_set == 'test'.")

    valid_mask = (test_df[TEXT_COLUMN] != "") & test_df[LABEL_COLUMN].isin(label2id)
    invalid_count = int((~valid_mask).sum())
    if invalid_count:
        logger.warning("Menghapus %s baris test tidak valid", invalid_count)

    test_df = test_df[valid_mask].reset_index(drop=True)
    test_df["true_id"] = test_df[LABEL_COLUMN].map(label2id).astype(int)
    return test_df


def load_model_and_tokenizer(label2id: dict[str, int], id2label: dict[int, str], device: torch.device):
    logger.info("Memuat tokenizer: %s", MODEL_DIR.relative_to(ROOT_DIR))
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)

    logger.info("Memuat model: %s", MODEL_DIR.relative_to(ROOT_DIR))
    config = AutoConfig.from_pretrained(MODEL_DIR)
    config.num_labels = len(LABEL_ORDER)
    config.label2id = label2id
    config.id2label = {idx: id2label[idx] for idx in sorted(id2label)}
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR, config=config)
    model.to(device)
    model.eval()
    return tokenizer, model


def build_test_loader(tokenizer, test_df: pd.DataFrame) -> DataLoader:
    encoded = tokenizer(
        test_df[TEXT_COLUMN].tolist(),
        max_length=MAX_LENGTH,
        padding="max_length",
        truncation=True,
        return_tensors="pt",
    )
    labels = torch.tensor(test_df["true_id"].to_numpy(), dtype=torch.long)
    dataset = TensorDataset(encoded["input_ids"], encoded["attention_mask"], labels)
    return DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=False)


def predict(model, data_loader: DataLoader, device: torch.device) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    true_ids = []
    pred_ids = []
    probabilities = []

    with torch.no_grad():
        for input_ids, attention_mask, labels in data_loader:
            input_ids = input_ids.to(device)
            attention_mask = attention_mask.to(device)
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            probs = torch.softmax(outputs.logits, dim=1)
            preds = torch.argmax(probs, dim=1)

            true_ids.extend(labels.numpy().tolist())
            pred_ids.extend(preds.cpu().numpy().tolist())
            probabilities.extend(probs.cpu().numpy().tolist())

    return np.array(true_ids), np.array(pred_ids), np.array(probabilities)


def build_predictions_df(
    test_df: pd.DataFrame,
    pred_ids: np.ndarray,
    probabilities: np.ndarray,
    id2label: dict[int, str],
) -> pd.DataFrame:
    output = pd.DataFrame()
    output["review"] = test_df[TEXT_COLUMN]
    output["true_label"] = test_df[LABEL_COLUMN]
    output["pred_label"] = [id2label[int(idx)] for idx in pred_ids]
    output["true_id"] = test_df["true_id"].astype(int)
    output["pred_id"] = pred_ids.astype(int)
    output["confidence"] = probabilities.max(axis=1)
    output["prob_negatif"] = probabilities[:, 0]
    output["prob_netral"] = probabilities[:, 1]
    output["prob_positif"] = probabilities[:, 2]
    return output


def calculate_metrics(true_ids: np.ndarray, pred_ids: np.ndarray) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    accuracy = accuracy_score(true_ids, pred_ids)
    macro_precision, macro_recall, macro_f1, _ = precision_recall_fscore_support(
        true_ids,
        pred_ids,
        labels=[0, 1, 2],
        average="macro",
        zero_division=0,
    )
    weighted_precision, weighted_recall, weighted_f1, _ = precision_recall_fscore_support(
        true_ids,
        pred_ids,
        labels=[0, 1, 2],
        average="weighted",
        zero_division=0,
    )
    report_dict = classification_report(
        true_ids,
        pred_ids,
        labels=[0, 1, 2],
        target_names=LABEL_ORDER,
        output_dict=True,
        zero_division=0,
    )
    cm = confusion_matrix(true_ids, pred_ids, labels=[0, 1, 2])

    metrics = {
        "accuracy": float(accuracy),
        "macro_precision": float(macro_precision),
        "macro_recall": float(macro_recall),
        "macro_f1": float(macro_f1),
        "weighted_precision": float(weighted_precision),
        "weighted_recall": float(weighted_recall),
        "weighted_f1": float(weighted_f1),
        "label_order": LABEL_ORDER,
        "classification_report": report_dict,
        "confusion_matrix": cm.tolist(),
    }
    report_df = pd.DataFrame(report_dict).transpose()
    cm_df = pd.DataFrame(
        cm,
        index=[f"actual_{label}" for label in LABEL_ORDER],
        columns=[f"predicted_{label}" for label in LABEL_ORDER],
    )
    return metrics, report_df, cm_df


def save_outputs(metrics: dict, report_df: pd.DataFrame, cm_df: pd.DataFrame, predictions_df: pd.DataFrame) -> None:
    with TEST_METRICS_PATH.open("w", encoding="utf-8") as file:
        json.dump(metrics, file, ensure_ascii=False, indent=4)
    report_df.to_csv(CLASSIFICATION_REPORT_PATH, encoding="utf-8-sig")
    cm_df.to_csv(CONFUSION_MATRIX_PATH, encoding="utf-8-sig")
    predictions_df.to_csv(PREDICTIONS_PATH, index=False, encoding="utf-8-sig")


def print_summary(test_df: pd.DataFrame, device: torch.device, metrics: dict) -> None:
    print("\nRingkasan Evaluation IndoBERT V3 Baseline")
    print(f"Dataset: {DATASET_PATH.relative_to(ROOT_DIR)}")
    print(f"Model: {MODEL_DIR.relative_to(ROOT_DIR)}")
    print(f"Jumlah data test: {len(test_df)}")
    print("\nDistribusi label test:")
    print(test_df[LABEL_COLUMN].value_counts().reindex(LABEL_ORDER, fill_value=0).to_string())
    print(f"\nDevice: {device}")
    print(f"Accuracy: {metrics['accuracy']:.6f}")
    print(f"Macro F1: {metrics['macro_f1']:.6f}")
    print(f"Weighted F1: {metrics['weighted_f1']:.6f}")
    print(f"\nOutput evaluation: {EVALUATION_DIR.relative_to(ROOT_DIR)}")
    print(f"- {TEST_METRICS_PATH.relative_to(ROOT_DIR)}")
    print(f"- {CLASSIFICATION_REPORT_PATH.relative_to(ROOT_DIR)}")
    print(f"- {CONFUSION_MATRIX_PATH.relative_to(ROOT_DIR)}")
    print(f"- {PREDICTIONS_PATH.relative_to(ROOT_DIR)}")


def evaluate_indobert() -> dict:
    prepare_output_dirs()
    validate_inputs()
    label2id, id2label = load_label_mapping()
    test_df = load_test_data(label2id)
    device = get_device()
    tokenizer, model = load_model_and_tokenizer(label2id, id2label, device)
    test_loader = build_test_loader(tokenizer, test_df)

    true_ids, pred_ids, probabilities = predict(model, test_loader, device)
    predictions_df = build_predictions_df(test_df, pred_ids, probabilities, id2label)
    metrics, report_df, cm_df = calculate_metrics(true_ids, pred_ids)
    metrics["test_count"] = int(len(test_df))
    metrics["true_label_distribution"] = test_df[LABEL_COLUMN].value_counts().reindex(LABEL_ORDER, fill_value=0).astype(int).to_dict()
    metrics["pred_label_distribution"] = predictions_df["pred_label"].value_counts().reindex(LABEL_ORDER, fill_value=0).astype(int).to_dict()
    save_outputs(metrics, report_df, cm_df, predictions_df)
    print_summary(test_df, device, metrics)
    return metrics


def main() -> None:
    try:
        evaluate_indobert()
    except (FileNotFoundError, ValueError, RuntimeError, OSError) as exc:
        print("\nProses evaluation IndoBERT v3 baseline gagal.")
        print(str(exc))
        print("\nPerbaiki input, model, dependensi, atau resource komputasi terlebih dahulu, lalu jalankan ulang script.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
