import importlib.util
import logging
from pathlib import Path
import sys

import pandas as pd


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


ROOT_DIR = Path(__file__).resolve().parents[2]
VALIDATION_SAMPLE_PATH = ROOT_DIR / "data" / "processed" / "lexicon_validation_sample.csv"
OUTPUT_PATH = ROOT_DIR / "outputs" / "audit" / "validasi_v1_vs_v3.csv"
LABELING_V3_SCRIPT_PATH = Path(__file__).resolve().with_name("04c_labeling_inset_v3.py")

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_labeling_v3_module():
    spec = importlib.util.spec_from_file_location("labeling_inset_v3", LABELING_V3_SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize_label(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).str.strip().str.lower()


def calculate_accuracy(df: pd.DataFrame, prediction_column: str) -> float:
    valid_df = df[df["manual_label"].isin({"positif", "negatif", "netral"})].copy()
    if valid_df.empty:
        raise ValueError("Tidak ada manual_label valid untuk menghitung akurasi.")
    return float((valid_df[prediction_column] == valid_df["manual_label"]).mean() * 100)


def main() -> None:
    logger.info("Memulai validasi manual otomatis v3")
    if not VALIDATION_SAMPLE_PATH.exists():
        raise FileNotFoundError(f"File validasi manual tidak ditemukan: {VALIDATION_SAMPLE_PATH}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    labeling_v3 = load_labeling_v3_module()

    validation_df = pd.read_csv(VALIDATION_SAMPLE_PATH)
    required_columns = {"clean_review", "manual_label", "label"}
    missing_columns = required_columns - set(validation_df.columns)
    if missing_columns:
        raise ValueError(f"Kolom wajib tidak ditemukan pada file validasi: {missing_columns}")

    positive_dict = labeling_v3.build_lexicon_dict(labeling_v3.load_lexicon(labeling_v3.POSITIVE_LEXICON_PATH))
    negative_dict = labeling_v3.build_lexicon_dict(labeling_v3.load_lexicon(labeling_v3.NEGATIVE_LEXICON_PATH))

    logger.info("Menghitung label v3 pada 100 sampel validasi")
    output_df = validation_df.copy()
    output_df["manual_label"] = normalize_label(output_df["manual_label"])
    output_df["label_v1"] = normalize_label(output_df["label"])
    output_df["skor_v3"] = output_df["clean_review"].apply(
        lambda text: labeling_v3.hitung_skor(
            text,
            positive_dict,
            negative_dict,
            labeling_v3.NEGATION_WORDS,
        )
    )
    output_df["label_v3"] = output_df["skor_v3"].apply(labeling_v3.assign_label)
    output_df["benar_v1"] = output_df["label_v1"] == output_df["manual_label"]
    output_df["benar_v3"] = output_df["label_v3"] == output_df["manual_label"]

    accuracy_v1 = calculate_accuracy(output_df, "label_v1")
    accuracy_v3 = calculate_accuracy(output_df, "label_v3")
    improvement = accuracy_v3 - accuracy_v1

    comparison_df = output_df[
        ["clean_review", "manual_label", "label_v1", "label_v3", "benar_v1", "benar_v3"]
    ].copy()

    logger.info("Menyimpan hasil validasi: %s", OUTPUT_PATH.relative_to(ROOT_DIR))
    comparison_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("\nRingkasan Validasi Manual V3")
    print(f"Jumlah sampel valid: {int(output_df['manual_label'].isin({'positif', 'negatif', 'netral'}).sum())}")
    print(f"Akurasi v1 pada 100 sampel manual: {accuracy_v1:.2f}%")
    print(f"Akurasi v3 pada 100 sampel manual: {accuracy_v3:.2f}%")
    print(f"Peningkatan: {improvement:.2f}%")
    print(f"Output validasi: {OUTPUT_PATH.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
