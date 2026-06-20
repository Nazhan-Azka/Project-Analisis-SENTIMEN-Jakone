from pathlib import Path
import inspect
import json
import logging
import os
import random
import sys

try:
    import numpy as np
    import pandas as pd
    import torch
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support
    from sklearn.utils.class_weight import compute_class_weight
    from torch import nn
    from transformers import (
        AutoModelForSequenceClassification,
        AutoTokenizer,
        Trainer,
        TrainingArguments,
        set_seed as transformers_set_seed,
    )
except ImportError as exc:
    print("\nDependensi Python belum lengkap untuk fine-tuning IndoBERT.")
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
MODEL_OUTPUT_DIR = ROOT_DIR / "models" / "indobert_v3_baseline"
EXPERIMENT_OUTPUT_DIR = ROOT_DIR / "outputs" / "modeling" / "indobert_v3_baseline"

LABEL_MAPPING_PATH = MODEL_OUTPUT_DIR / "label_mapping.json"
TRAINING_CONFIG_PATH = EXPERIMENT_OUTPUT_DIR / "training_config.json"
VALIDATION_METRICS_PATH = EXPERIMENT_OUTPUT_DIR / "validation_metrics.json"
TRAINING_LOG_PATH = EXPERIMENT_OUTPUT_DIR / "training_log.json"

MODEL_NAME = "indobenchmark/indobert-base-p1"
TEXT_COLUMN = "review"
LABEL_COLUMN = "label"
SPLIT_COLUMN = "split_set"
REQUIRED_COLUMNS = {TEXT_COLUMN, LABEL_COLUMN, SPLIT_COLUMN}

LABEL_ORDER = ["negatif", "netral", "positif"]
LABEL2ID = {"negatif": 0, "netral": 1, "positif": 2}
ID2LABEL = {0: "negatif", 1: "netral", 2: "positif"}

SEED = 42
EPOCHS = 2
BATCH_SIZE = 8
LEARNING_RATE = 2e-5
MAX_LENGTH = 128
WEIGHT_DECAY = 0.01
WARMUP_RATIO = 0.1
USE_CLASS_WEIGHT = False
ALLOW_OVERWRITE_MODEL = False

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class SentimentDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        item = {key: value[index] for key, value in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[index], dtype=torch.long)
        return item


class WeightedTrainer(Trainer):
    def __init__(self, class_weights=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits
        weight = self.class_weights.to(logits.device) if self.class_weights is not None else None
        loss = nn.CrossEntropyLoss(weight=weight)(logits, labels)
        return (loss, outputs) if return_outputs else loss


def set_all_seeds(seed: int = SEED) -> None:
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    transformers_set_seed(seed)


def get_device() -> torch.device:
    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        print(f"CUDA tersedia. Training menggunakan GPU: {device_name}")
        return torch.device("cuda")

    print("WARNING: CUDA/GPU tidak tersedia. Training IndoBERT di CPU akan sangat lambat.")
    return torch.device("cpu")


def prepare_output_dirs() -> None:
    MODEL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    EXPERIMENT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def validate_no_model_overwrite() -> None:
    existing_model_files = [
        MODEL_OUTPUT_DIR / "config.json",
        MODEL_OUTPUT_DIR / "model.safetensors",
        MODEL_OUTPUT_DIR / "pytorch_model.bin",
    ]
    if not ALLOW_OVERWRITE_MODEL and any(path.exists() for path in existing_model_files):
        raise FileExistsError(
            f"Folder model sudah berisi model: {MODEL_OUTPUT_DIR}\n"
            "Agar tidak menimpa model lama, pindahkan/rename folder tersebut atau ubah "
            "ALLOW_OVERWRITE_MODEL = True jika memang ingin menjalankan ulang eksperimen yang sama."
        )


def validate_dataset_path() -> None:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset v3 tidak ditemukan: {DATASET_PATH}")


def load_dataset() -> pd.DataFrame:
    logger.info("Membaca dataset: %s", DATASET_PATH.relative_to(ROOT_DIR))
    df = pd.read_csv(DATASET_PATH)
    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(f"Kolom wajib tidak ditemukan: {', '.join(sorted(missing_columns))}")

    df = df[[TEXT_COLUMN, LABEL_COLUMN, SPLIT_COLUMN]].copy()
    df[TEXT_COLUMN] = df[TEXT_COLUMN].fillna("").astype(str).str.strip()
    df[LABEL_COLUMN] = df[LABEL_COLUMN].fillna("").astype(str).str.strip().str.lower()
    df[SPLIT_COLUMN] = df[SPLIT_COLUMN].fillna("").astype(str).str.strip().str.lower()

    valid_mask = (
        (df[TEXT_COLUMN] != "")
        & df[LABEL_COLUMN].isin(LABEL2ID)
        & df[SPLIT_COLUMN].isin({"train", "val", "test"})
    )
    invalid_count = int((~valid_mask).sum())
    if invalid_count:
        logger.warning("Menghapus %s baris tidak valid sebelum training", invalid_count)

    df = df[valid_mask].reset_index(drop=True)
    df["label_id"] = df[LABEL_COLUMN].map(LABEL2ID).astype(int)
    if df.empty:
        raise ValueError("Dataset kosong setelah validasi.")
    return df


def split_train_val(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    train_df = df[df[SPLIT_COLUMN] == "train"].reset_index(drop=True)
    val_df = df[df[SPLIT_COLUMN] == "val"].reset_index(drop=True)
    if train_df.empty or val_df.empty:
        raise ValueError("Split train dan val harus tersedia dan tidak kosong.")
    return train_df, val_df


def tokenize_dataframe(tokenizer, df: pd.DataFrame):
    return tokenizer(
        df[TEXT_COLUMN].tolist(),
        max_length=MAX_LENGTH,
        truncation=True,
        padding="max_length",
    )


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    accuracy = accuracy_score(labels, predictions)
    macro_precision, macro_recall, macro_f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="macro",
        zero_division=0,
    )
    _, _, weighted_f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="weighted",
        zero_division=0,
    )
    return {
        "accuracy": float(accuracy),
        "macro_precision": float(macro_precision),
        "macro_recall": float(macro_recall),
        "macro_f1": float(macro_f1),
        "weighted_f1": float(weighted_f1),
    }


def calculate_class_weights(train_df: pd.DataFrame) -> torch.Tensor | None:
    if not USE_CLASS_WEIGHT:
        return None

    class_ids = np.array([0, 1, 2])
    class_weights = compute_class_weight(
        class_weight="balanced",
        classes=class_ids,
        y=train_df["label_id"].to_numpy(),
    )
    logger.info(
        "Class weight aktif: negatif=%.6f, netral=%.6f, positif=%.6f",
        class_weights[0],
        class_weights[1],
        class_weights[2],
    )
    return torch.tensor(class_weights, dtype=torch.float)


def build_training_arguments() -> TrainingArguments:
    args = {
        "output_dir": str(EXPERIMENT_OUTPUT_DIR / "checkpoints"),
        "num_train_epochs": EPOCHS,
        "per_device_train_batch_size": BATCH_SIZE,
        "per_device_eval_batch_size": BATCH_SIZE,
        "learning_rate": LEARNING_RATE,
        "weight_decay": WEIGHT_DECAY,
        "warmup_ratio": WARMUP_RATIO,
        "logging_dir": str(EXPERIMENT_OUTPUT_DIR / "logs"),
        "logging_steps": 50,
        "save_strategy": "epoch",
        "eval_strategy": "epoch",
        "load_best_model_at_end": True,
        "metric_for_best_model": "macro_f1",
        "greater_is_better": True,
        "save_total_limit": 2,
        "seed": SEED,
        "data_seed": SEED,
        "report_to": "none",
    }

    # overwrite_output_dir tidak dipakai karena tidak kompatibel pada sebagian versi transformers.
    # Proteksi overwrite model tetap ditangani oleh validate_no_model_overwrite().
    signature = inspect.signature(TrainingArguments.__init__)
    if "eval_strategy" not in signature.parameters:
        args["evaluation_strategy"] = args.pop("eval_strategy")

    return TrainingArguments(**args)


def save_json(data, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def save_label_mapping() -> None:
    save_json({"label2id": LABEL2ID, "id2label": {str(k): v for k, v in ID2LABEL.items()}}, LABEL_MAPPING_PATH)


def build_training_config(train_df: pd.DataFrame, val_df: pd.DataFrame, device: torch.device) -> dict:
    return {
        "dataset_path": str(DATASET_PATH.relative_to(ROOT_DIR)),
        "model_name": MODEL_NAME,
        "model_output_dir": str(MODEL_OUTPUT_DIR.relative_to(ROOT_DIR)),
        "text_column": TEXT_COLUMN,
        "label_column": LABEL_COLUMN,
        "split_column": SPLIT_COLUMN,
        "label_order": LABEL_ORDER,
        "label2id": LABEL2ID,
        "epochs": EPOCHS,
        "batch_size": BATCH_SIZE,
        "learning_rate": LEARNING_RATE,
        "max_length": MAX_LENGTH,
        "random_seed": SEED,
        "weight_decay": WEIGHT_DECAY,
        "warmup_ratio": WARMUP_RATIO,
        "use_class_weight": USE_CLASS_WEIGHT,
        "device": str(device),
        "train_count": int(len(train_df)),
        "val_count": int(len(val_df)),
        "train_label_distribution": train_df[LABEL_COLUMN].value_counts().reindex(LABEL_ORDER, fill_value=0).astype(int).to_dict(),
        "val_label_distribution": val_df[LABEL_COLUMN].value_counts().reindex(LABEL_ORDER, fill_value=0).astype(int).to_dict(),
    }


def print_initial_summary(train_df: pd.DataFrame, val_df: pd.DataFrame, device: torch.device) -> None:
    print("\nRingkasan Setup Fine-Tuning IndoBERT V3 Baseline")
    print(f"Dataset: {DATASET_PATH.relative_to(ROOT_DIR)}")
    print(f"Jumlah data train: {len(train_df)}")
    print(f"Jumlah data val: {len(val_df)}")
    print("\nDistribusi label train:")
    print(train_df[LABEL_COLUMN].value_counts().reindex(LABEL_ORDER, fill_value=0).to_string())
    print("\nDistribusi label val:")
    print(val_df[LABEL_COLUMN].value_counts().reindex(LABEL_ORDER, fill_value=0).to_string())
    print(f"\nLabel mapping: {LABEL2ID}")
    print(f"Device: {device}")
    print(
        "Konfigurasi: "
        f"model={MODEL_NAME}, epoch={EPOCHS}, batch_size={BATCH_SIZE}, "
        f"lr={LEARNING_RATE}, max_length={MAX_LENGTH}, class_weight={USE_CLASS_WEIGHT}"
    )


def print_final_summary(metrics: dict) -> None:
    print("\nRingkasan Hasil Validation")
    print(f"Validation accuracy: {metrics.get('eval_accuracy', 0):.6f}")
    print(f"Validation macro F1: {metrics.get('eval_macro_f1', 0):.6f}")
    print(f"Validation weighted F1: {metrics.get('eval_weighted_f1', 0):.6f}")
    print(f"Model disimpan: {MODEL_OUTPUT_DIR.relative_to(ROOT_DIR)}")
    print(f"Training config: {TRAINING_CONFIG_PATH.relative_to(ROOT_DIR)}")
    print(f"Validation metrics: {VALIDATION_METRICS_PATH.relative_to(ROOT_DIR)}")
    print(f"Training log: {TRAINING_LOG_PATH.relative_to(ROOT_DIR)}")


def build_trainer(trainer_class, trainer_kwargs: dict, tokenizer):
    """Membuat Trainer lintas versi transformers tanpa memakai argumen tokenizer."""
    try:
        return trainer_class(**trainer_kwargs, processing_class=tokenizer)
    except TypeError as exc:
        if "processing_class" not in str(exc):
            raise
        logger.warning(
            "Trainer tidak mendukung processing_class pada versi transformers ini. "
            "Membuat Trainer tanpa processing_class."
        )
        return trainer_class(**trainer_kwargs)


def fine_tune() -> None:
    set_all_seeds(SEED)
    prepare_output_dirs()
    validate_no_model_overwrite()
    validate_dataset_path()

    df = load_dataset()
    train_df, val_df = split_train_val(df)
    device = get_device()
    print_initial_summary(train_df, val_df, device)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    train_dataset = SentimentDataset(tokenize_dataframe(tokenizer, train_df), train_df["label_id"].tolist())
    val_dataset = SentimentDataset(tokenize_dataframe(tokenizer, val_df), val_df["label_id"].tolist())

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(LABEL_ORDER),
        label2id=LABEL2ID,
        id2label=ID2LABEL,
    )

    class_weights = calculate_class_weights(train_df)
    trainer_class = WeightedTrainer if USE_CLASS_WEIGHT else Trainer
    trainer_kwargs = {
        "model": model,
        "args": build_training_arguments(),
        "train_dataset": train_dataset,
        "eval_dataset": val_dataset,
        "compute_metrics": compute_metrics,
    }
    if USE_CLASS_WEIGHT:
        trainer_kwargs["class_weights"] = class_weights
    trainer = build_trainer(trainer_class, trainer_kwargs, tokenizer)

    save_json(build_training_config(train_df, val_df, device), TRAINING_CONFIG_PATH)
    save_label_mapping()

    trainer.train()
    validation_metrics = trainer.evaluate(eval_dataset=val_dataset)

    trainer.save_model(str(MODEL_OUTPUT_DIR))
    tokenizer.save_pretrained(MODEL_OUTPUT_DIR)
    save_label_mapping()

    save_json(validation_metrics, VALIDATION_METRICS_PATH)
    save_json(trainer.state.log_history, TRAINING_LOG_PATH)
    print_final_summary(validation_metrics)


def main() -> None:
    try:
        fine_tune()
    except (FileNotFoundError, FileExistsError, ValueError, RuntimeError, OSError) as exc:
        print("\nProses fine-tuning IndoBERT v3 baseline gagal.")
        print(str(exc))
        print("\nPerbaiki input, dependensi, atau resource komputasi terlebih dahulu, lalu jalankan ulang script.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
