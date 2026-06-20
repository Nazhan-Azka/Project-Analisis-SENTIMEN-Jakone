from pathlib import Path
import sys

import pandas as pd


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


LEXICON_DIR = Path("data/lexicon")
POSITIVE_PATH = LEXICON_DIR / "positive.tsv"
NEGATIVE_PATH = LEXICON_DIR / "negative.tsv"
ENCODINGS = ["utf-8", "latin-1", "ISO-8859-1"]

WORD_COLUMN_CANDIDATES = {
    "word",
    "kata",
    "term",
    "token",
    "phrase",
    "sentiment_word",
}
WEIGHT_COLUMN_CANDIDATES = {
    "weight",
    "bobot",
    "score",
    "nilai",
    "polarity",
    "sentiment_score",
}


def check_required_files():
    """Mengecek folder dan file lexicon yang wajib tersedia."""
    LEXICON_DIR.mkdir(parents=True, exist_ok=True)

    missing_files = [
        path for path in [POSITIVE_PATH, NEGATIVE_PATH] if not path.exists()
    ]
    if missing_files:
        print("File InSet Lexicon belum lengkap.")
        print("\nFile yang belum ada:")
        for path in missing_files:
            print(f"- {path}")
        print("\nSilakan letakkan file berikut ke folder data/lexicon/:")
        print("- data/lexicon/positive.tsv")
        print("- data/lexicon/negative.tsv")
        print("\nPengecekan dihentikan. Belum ada proses labeling sentimen.")
        return False

    return True


def read_tsv_with_fallback(path):
    """Membaca file TSV dengan beberapa opsi encoding."""
    errors = []

    for encoding in ENCODINGS:
        try:
            df = pd.read_csv(path, sep="\t", encoding=encoding)
            return df, encoding
        except UnicodeDecodeError as exc:
            errors.append(f"{encoding}: {exc}")
        except Exception as exc:
            raise RuntimeError(f"Gagal membaca {path}: {exc}") from exc

    error_text = "\n".join(errors)
    raise UnicodeError(
        f"Gagal membaca {path} dengan encoding {', '.join(ENCODINGS)}.\n{error_text}"
    )


def find_column(columns, candidates):
    normalized_columns = {str(column).strip().lower(): column for column in columns}
    for candidate in candidates:
        if candidate in normalized_columns:
            return normalized_columns[candidate]
    return None


def inspect_lexicon_format(df, label):
    """Mengecek kolom kata dan bobot dengan nama kolom yang fleksibel."""
    word_column = find_column(df.columns, WORD_COLUMN_CANDIDATES)
    weight_column = find_column(df.columns, WEIGHT_COLUMN_CANDIDATES)
    normalized_columns = {str(column).strip().lower() for column in df.columns}

    print(f"\nFormat {label}:")
    print(f"- Kolom kata terdeteksi: {word_column if word_column else 'tidak ditemukan'}")
    print(f"- Kolom bobot terdeteksi: {weight_column if weight_column else 'tidak ditemukan'}")

    if {"word", "weight"}.issubset(normalized_columns):
        print("- Status format: valid, kolom word dan weight ditemukan.")
    elif word_column and weight_column:
        print("- Status format: dapat dibaca, tetapi nama kolom bukan word dan weight.")
    else:
        print("- Status format: perlu dicek ulang, kolom kata atau bobot belum terdeteksi.")


def print_lexicon_summary(positive_df, negative_df, positive_encoding, negative_encoding):
    print("\nRingkasan InSet Lexicon")
    print(f"Encoding positive.tsv: {positive_encoding}")
    print(f"Encoding negative.tsv: {negative_encoding}")
    print(f"Jumlah kata pada positive.tsv: {len(positive_df)}")
    print(f"Jumlah kata pada negative.tsv: {len(negative_df)}")

    print("\nNama kolom positive.tsv:")
    print(list(positive_df.columns))

    print("\nNama kolom negative.tsv:")
    print(list(negative_df.columns))

    inspect_lexicon_format(positive_df, "positive.tsv")
    inspect_lexicon_format(negative_df, "negative.tsv")

    print("\n5 baris pertama positive.tsv:")
    print(positive_df.head().to_string(index=False))

    print("\n5 baris pertama negative.tsv:")
    print(negative_df.head().to_string(index=False))

    print("\nPengecekan selesai. Belum ada proses labeling sentimen.")


def main():
    print("Pengecekan file InSet Lexicon")
    print(f"Folder lexicon: {LEXICON_DIR}")

    if not check_required_files():
        return

    try:
        positive_df, positive_encoding = read_tsv_with_fallback(POSITIVE_PATH)
        negative_df, negative_encoding = read_tsv_with_fallback(NEGATIVE_PATH)
    except Exception as exc:
        print("\nGagal membaca file InSet Lexicon.")
        print(str(exc))
        print("\nPastikan positive.tsv dan negative.tsv adalah file TSV yang valid.")
        print("Pengecekan dihentikan. Belum ada proses labeling sentimen.")
        return

    print_lexicon_summary(
        positive_df,
        negative_df,
        positive_encoding,
        negative_encoding,
    )


if __name__ == "__main__":
    main()
