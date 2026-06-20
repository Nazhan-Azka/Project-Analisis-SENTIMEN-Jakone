from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

import pandas as pd


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


LEXICON_DIR = Path("data/lexicon")
POSITIVE_URL = "https://raw.githubusercontent.com/fajri91/InSet/master/positive.tsv"
NEGATIVE_URL = "https://raw.githubusercontent.com/fajri91/InSet/master/negative.tsv"
POSITIVE_PATH = LEXICON_DIR / "positive.tsv"
NEGATIVE_PATH = LEXICON_DIR / "negative.tsv"
OVERWRITE = False
ENCODINGS = ["utf-8", "latin-1", "ISO-8859-1"]
TIMEOUT_SECONDS = 30


def download_file(url, output_path):
    """Download file dari URL dan simpan ke path tujuan."""
    if output_path.exists() and not OVERWRITE:
        print(f"File sudah tersedia, tidak download ulang: {output_path}")
        return

    action = "Menimpa" if output_path.exists() and OVERWRITE else "Download"
    print(f"{action}: {url}")

    try:
        with urlopen(url, timeout=TIMEOUT_SECONDS) as response:
            content = response.read()
    except HTTPError as exc:
        raise RuntimeError(
            f"Gagal download {url}. HTTP status: {exc.code} {exc.reason}"
        ) from exc
    except URLError as exc:
        raise RuntimeError(
            f"Gagal koneksi ke {url}. Detail: {exc.reason}"
        ) from exc
    except TimeoutError as exc:
        raise RuntimeError(
            f"Koneksi timeout saat download {url}."
        ) from exc

    output_path.write_bytes(content)
    print(f"File disimpan ke: {output_path}")


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


def print_download_summary(positive_df, negative_df, positive_encoding, negative_encoding):
    print("\nRingkasan Download InSet Lexicon")
    print(f"Path positive.tsv: {POSITIVE_PATH}")
    print(f"Path negative.tsv: {NEGATIVE_PATH}")
    print(f"Encoding positive.tsv: {positive_encoding}")
    print(f"Encoding negative.tsv: {negative_encoding}")
    print(f"Jumlah kata positif: {len(positive_df)}")
    print(f"Jumlah kata negatif: {len(negative_df)}")

    print("\nNama kolom positive.tsv:")
    print(list(positive_df.columns))

    print("\nNama kolom negative.tsv:")
    print(list(negative_df.columns))

    print("\n5 baris pertama positive.tsv:")
    print(positive_df.head().to_string(index=False))

    print("\n5 baris pertama negative.tsv:")
    print(negative_df.head().to_string(index=False))

    print("\nDownload dan pengecekan awal selesai. Belum ada proses labeling sentimen.")


def main():
    print("Download InSet Lexicon")
    print(f"Folder lexicon: {LEXICON_DIR}")
    print(f"Overwrite: {OVERWRITE}")

    LEXICON_DIR.mkdir(parents=True, exist_ok=True)

    try:
        download_file(POSITIVE_URL, POSITIVE_PATH)
        download_file(NEGATIVE_URL, NEGATIVE_PATH)

        positive_df, positive_encoding = read_tsv_with_fallback(POSITIVE_PATH)
        negative_df, negative_encoding = read_tsv_with_fallback(NEGATIVE_PATH)
    except Exception as exc:
        print("\nProses download atau pembacaan lexicon gagal.")
        print(str(exc))
        print("\nPastikan koneksi internet tersedia dan URL GitHub dapat diakses.")
        print("Belum ada proses labeling sentimen.")
        return

    print_download_summary(
        positive_df,
        negative_df,
        positive_encoding,
        negative_encoding,
    )


if __name__ == "__main__":
    main()
