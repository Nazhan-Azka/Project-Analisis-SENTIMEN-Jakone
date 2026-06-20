from pathlib import Path
import logging
import sys

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


INPUT_PATH = Path("data/processed/jakone_reviews_labeled_v3.csv")
OUTPUT_PATH = Path("data/final/06_jakone_modeling_master_v3.csv")
SUMMARY_PATH = Path("outputs/audit/distribusi_split_v3.csv")

RANDOM_STATE = 42
VALID_LABELS = {"positif", "negatif", "netral"}
SPLIT_ORDER = ["train", "val", "test"]
LABEL_ORDER = ["positif", "negatif", "netral"]
TEXT_SOURCE_CANDIDATES = ["clean_review", "review"]
LABEL_SOURCE_COLUMN = "label_v3"
STANDARD_OUTPUT_COLUMNS = ["review", "label", "split_set"]

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def validate_input_file():
    """Mengecek file input agar pesan error umum tetap jelas."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"File input tidak ditemukan: {INPUT_PATH}\n"
            "Jalankan tahap labeling v3 terlebih dahulu."
        )


def load_dataset():
    """Membaca dataset hasil labeling tanpa mengubah file input asli."""
    logger.info("Membaca dataset labeled: %s", INPUT_PATH)
    df = pd.read_csv(INPUT_PATH)
    return df


def validate_required_columns(df):
    """Mengecek kolom wajib sebelum split dataset."""
    if not any(column in df.columns for column in TEXT_SOURCE_CANDIDATES):
        raise ValueError("Kolom teks wajib tidak ditemukan: clean_review atau review")

    required_columns = {LABEL_SOURCE_COLUMN}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))
        raise ValueError(f"Kolom wajib tidak ditemukan: {missing_text}")


def choose_text_column(df):
    """Memilih clean_review sebagai teks utama jika tersedia, jika tidak memakai review."""
    if "clean_review" in df.columns:
        return "clean_review"
    return "review"


def clean_invalid_rows(df):
    """Membuat kolom standar review dan label, lalu menghapus baris tidak valid."""
    logger.info("Validasi baris sebelum split")
    df = df.copy()
    total_initial = len(df)
    text_column = choose_text_column(df)

    df["review"] = df[text_column].fillna("").astype(str).str.strip()
    df["label"] = df[LABEL_SOURCE_COLUMN].fillna("").astype(str).str.strip().str.lower()

    valid_mask = (
        (df["review"] != "")
        & (df["label"] != "")
        & (df["label"].isin(VALID_LABELS))
    )

    invalid_count = int((~valid_mask).sum())
    if invalid_count > 0:
        logger.warning("Menghapus %s baris tidak valid sebelum split", invalid_count)

    valid_df = df[valid_mask].reset_index(drop=True)
    return valid_df, total_initial, invalid_count


def perform_stratified_split(df):
    """Membagi data menjadi train 80%, validation 10%, dan test 10% secara stratified."""
    logger.info("Melakukan stratified split 80/10/10")
    train_df, temp_df = train_test_split(
        df,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=df["label"],
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.5,
        random_state=RANDOM_STATE,
        stratify=temp_df["label"],
    )

    train_df = train_df.copy()
    val_df = val_df.copy()
    test_df = test_df.copy()

    train_df["split_set"] = "train"
    val_df["split_set"] = "val"
    test_df["split_set"] = "test"

    final_df = pd.concat([train_df, val_df, test_df], ignore_index=True)
    final_df = final_df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
    return final_df


def order_output_columns(df):
    """Menempatkan kolom standar modeling di depan dan mempertahankan kolom audit tambahan."""
    extra_columns = [column for column in df.columns if column not in STANDARD_OUTPUT_COLUMNS]
    return df[STANDARD_OUTPUT_COLUMNS + extra_columns]


def build_distribution_summary(df):
    """Membuat ringkasan count dan persentase label untuk setiap split."""
    rows = []
    for split_set in SPLIT_ORDER:
        split_df = df[df["split_set"] == split_set]
        split_total = len(split_df)
        label_counts = split_df["label"].value_counts().reindex(LABEL_ORDER, fill_value=0)

        for label, count in label_counts.items():
            percentage = np.round((count / split_total * 100) if split_total else 0, 2)
            rows.append(
                {
                    "split_set": split_set,
                    "label": label,
                    "count": int(count),
                    "percentage": float(percentage),
                }
            )

    return pd.DataFrame(rows)


def print_summary(df, total_initial, invalid_count, distribution_summary):
    """Menampilkan ringkasan hasil split ke terminal."""
    total_valid = len(df)
    print("\nRingkasan Split Dataset")
    print(f"Jumlah data awal: {total_initial}")
    print(f"Jumlah data tidak valid yang dihapus: {invalid_count}")
    print(f"Jumlah data valid setelah pembersihan: {total_valid}")

    print("\nDistribusi label total:")
    print(df["label"].value_counts().reindex(LABEL_ORDER, fill_value=0).to_string())

    print("\nJumlah data per split:")
    print(df["split_set"].value_counts().reindex(SPLIT_ORDER, fill_value=0).to_string())

    print("\nDistribusi label per split:")
    count_table = pd.crosstab(df["split_set"], df["label"]).reindex(
        index=SPLIT_ORDER,
        columns=LABEL_ORDER,
        fill_value=0,
    )
    print(count_table.to_string())

    print("\nPersentase label per split:")
    percentage_table = count_table.div(count_table.sum(axis=1), axis=0).mul(100).round(2)
    print(percentage_table.astype(str).add("%").to_string())

    print("\nRingkasan distribusi split:")
    print(distribution_summary.to_string(index=False))

    print("\nContoh 5 baris output:")
    preview_columns = ["review", "label", "split_set"]
    preview_columns = [column for column in preview_columns if column in df.columns]
    print(df[preview_columns].head(5).to_string(index=False))


def main():
    try:
        logger.info("Memulai split dataset untuk modeling IndoBERT")
        validate_input_file()

        df = load_dataset()
        validate_required_columns(df)
        valid_df, total_initial, invalid_count = clean_invalid_rows(df)

        if valid_df.empty:
            raise ValueError("Tidak ada data valid untuk split dataset.")

        final_df = perform_stratified_split(valid_df)
        final_df = order_output_columns(final_df)
        distribution_summary = build_distribution_summary(final_df)

        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Menyimpan dataset final modeling: %s", OUTPUT_PATH)
        final_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

        logger.info("Menyimpan ringkasan distribusi split: %s", SUMMARY_PATH)
        distribution_summary.to_csv(SUMMARY_PATH, index=False, encoding="utf-8-sig")

        print_summary(final_df, total_initial, invalid_count, distribution_summary)
        print(f"\nDataset final: {OUTPUT_PATH}")
        print(f"Ringkasan distribusi: {SUMMARY_PATH}")
        print("\nSplit dataset selesai. Belum ada tokenisasi, training, evaluasi, atau model output.")
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print("\nProses split dataset gagal.")
        print(str(exc))
        print("\nPerbaiki input terlebih dahulu, lalu jalankan ulang script.")


if __name__ == "__main__":
    main()
