from pathlib import Path
import logging
import sys

import numpy as np
import pandas as pd


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


DATA_PATH = Path("data/processed/jakone_reviews_clean.csv")
POSITIVE_LEXICON_PATH = Path("data/lexicon/positive.tsv")
NEGATIVE_LEXICON_PATH = Path("data/lexicon/negative.tsv")
OUTPUT_PATH = Path("data/processed/jakone_reviews_labeled.csv")
VALIDATION_SAMPLE_PATH = Path("data/processed/lexicon_validation_sample.csv")

TEXT_COLUMN = "clean_review"
NEGATION_WORDS = {
    "tidak",
    "bukan",
    "belum",
    "kurang",
    "jangan",
    "tak",
    "ga",
    "gak",
    "nggak",
}

VALIDATION_SAMPLE_SIZE = 100
RANDOM_STATE = 42

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def validate_input_files():
    """Mengecek semua file input agar error umum tampil jelas tanpa traceback panjang."""
    required_files = [
        DATA_PATH,
        POSITIVE_LEXICON_PATH,
        NEGATIVE_LEXICON_PATH,
    ]
    missing_files = [path for path in required_files if not path.exists()]

    if missing_files:
        missing_text = "\n".join(f"- {path}" for path in missing_files)
        raise FileNotFoundError(
            "File input belum lengkap:\n"
            f"{missing_text}\n\n"
            "Pastikan dataset clean dan file InSet Lexicon sudah tersedia."
        )


def load_dataset(path):
    """Membaca dataset hasil preprocessing dan memastikan kolom clean_review tersedia."""
    logger.info("Membaca dataset: %s", path)
    df = pd.read_csv(path)

    if TEXT_COLUMN not in df.columns:
        raise ValueError(f"Kolom wajib tidak ditemukan pada dataset: {TEXT_COLUMN}")

    df[TEXT_COLUMN] = df[TEXT_COLUMN].fillna("").astype(str)
    return df


def load_lexicon(path, sentiment_type):
    """Membaca lexicon TSV dan mengubah kolom weight menjadi float."""
    logger.info("Membaca lexicon %s: %s", sentiment_type, path)
    df = pd.read_csv(path, sep="\t")

    required_columns = {"word", "weight"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))
        raise ValueError(f"Kolom lexicon tidak lengkap pada {path}: {missing_text}")

    df = df[["word", "weight"]].copy()
    df["word"] = df["word"].fillna("").astype(str).str.strip().str.lower()
    df["weight"] = pd.to_numeric(df["weight"], errors="coerce")
    df = df[(df["word"] != "") & df["weight"].notna()]
    return df


def build_lexicon_dictionaries(positive_df, negative_df):
    """Membuat dictionary skor positif dan negatif dari InSet Lexicon."""
    positive_dict = {
        row.word: float(abs(row.weight))
        for row in positive_df.itertuples(index=False)
    }
    negative_dict = {
        row.word: -float(abs(row.weight))
        for row in negative_df.itertuples(index=False)
    }
    return positive_dict, negative_dict


def calculate_sentiment_score(text, positive_dict, negative_dict):
    """Menghitung total skor sentimen dari token clean_review dengan aturan negasi sederhana."""
    tokens = str(text).split()
    total_score = 0.0

    for index, token in enumerate(tokens):
        if token in positive_dict:
            token_score = positive_dict[token]
        elif token in negative_dict:
            token_score = negative_dict[token]
        else:
            continue

        previous_token = tokens[index - 1] if index > 0 else ""
        if previous_token in NEGATION_WORDS:
            token_score = -token_score

        total_score += token_score

    return total_score


def assign_label(score):
    """Mengubah skor lexicon menjadi label positif, negatif, atau netral."""
    if score > 0:
        return "positif"
    if score < 0:
        return "negatif"
    return "netral"


def label_reviews(df, positive_dict, negative_dict):
    """Menambahkan kolom lexicon_score dan label pada dataset clean."""
    logger.info("Menghitung skor dan label sentimen")
    df = df.copy()
    df["lexicon_score"] = df[TEXT_COLUMN].apply(
        lambda text: calculate_sentiment_score(text, positive_dict, negative_dict)
    )
    df["lexicon_score"] = df["lexicon_score"].astype(float)
    df["label"] = np.where(
        df["lexicon_score"] > 0,
        "positif",
        np.where(df["lexicon_score"] < 0, "negatif", "netral"),
    )
    return df


def create_validation_sample(df):
    """Membuat 100 data acak untuk validasi manual label lexicon."""
    logger.info("Membuat sample validasi manual")
    sample_size = min(VALIDATION_SAMPLE_SIZE, len(df))
    sample_df = df.sample(n=sample_size, random_state=RANDOM_STATE).copy()
    sample_df["manual_label"] = ""
    sample_df["notes"] = ""
    return sample_df[
        [
            "review",
            "clean_review",
            "lexicon_score",
            "label",
            "manual_label",
            "notes",
        ]
    ].reset_index(drop=True)


def print_examples_by_label(df):
    """Menampilkan contoh 3 data untuk setiap kelas label."""
    for label in ["positif", "negatif", "netral"]:
        print(f"\nContoh 3 data label {label}:")
        subset = df[df["label"] == label][
            ["clean_review", "lexicon_score", "label"]
        ].head(3)
        if subset.empty:
            print(f"Tidak ada data dengan label {label}.")
        else:
            print(subset.to_string(index=False))


def print_summary(df):
    """Menampilkan total data, distribusi label, persentase label, dan contoh per kelas."""
    total_data = len(df)
    label_counts = df["label"].value_counts().reindex(
        ["positif", "negatif", "netral"],
        fill_value=0,
    )
    label_percentages = (label_counts / total_data * 100).round(2)

    print("\nRingkasan Labeling Sentimen InSet Lexicon")
    print(f"Total data: {total_data}")

    print("\nDistribusi label dalam jumlah:")
    print(label_counts.to_string())

    print("\nDistribusi label dalam persentase:")
    print(label_percentages.astype(str).add("%").to_string())

    print_examples_by_label(df)


def main():
    try:
        logger.info("Memulai labeling sentimen menggunakan InSet Lexicon")
        validate_input_files()
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

        df_clean = load_dataset(DATA_PATH)
        positive_df = load_lexicon(POSITIVE_LEXICON_PATH, "positif")
        negative_df = load_lexicon(NEGATIVE_LEXICON_PATH, "negatif")
        positive_dict, negative_dict = build_lexicon_dictionaries(
            positive_df,
            negative_df,
        )

        df_labeled = label_reviews(df_clean, positive_dict, negative_dict)
        validation_sample = create_validation_sample(df_labeled)

        logger.info("Menyimpan output utama: %s", OUTPUT_PATH)
        df_labeled.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

        logger.info("Menyimpan sample validasi manual: %s", VALIDATION_SAMPLE_PATH)
        validation_sample.to_csv(
            VALIDATION_SAMPLE_PATH,
            index=False,
            encoding="utf-8-sig",
        )

        print_summary(df_labeled)
        print(f"\nOutput utama: {OUTPUT_PATH}")
        print(f"Output validasi manual: {VALIDATION_SAMPLE_PATH}")
        print("\nLabeling selesai. Belum ada split dataset, training, evaluasi, atau visualisasi akhir.")
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print("\nProses labeling gagal.")
        print(str(exc))
        print("\nPerbaiki input terlebih dahulu, lalu jalankan ulang script.")


if __name__ == "__main__":
    main()
