from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("output_analisis")
TARGET = OUTPUT_DIR / "HASIL_LENGKAP_UNTUK_REVIEW.txt"


def markdown_table(csv_path: Path) -> str:
    df = pd.read_csv(csv_path, keep_default_na=False)
    headers = [str(col) for col in df.columns]

    def format_cell(value: object) -> str:
        if pd.isna(value):
            return ""
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)

    rows = [[format_cell(value) for value in row] for row in df.itertuples(index=False, name=None)]
    widths = [
        max(len(headers[col_idx]), *(len(row[col_idx]) for row in rows))
        for col_idx in range(len(headers))
    ]

    def format_row(values: list[str]) -> str:
        return "| " + " | ".join(
            value.ljust(widths[idx]) for idx, value in enumerate(values)
        ) + " |"

    separator = "| " + " | ".join("-" * width for width in widths) + " |"
    return "\n".join([format_row(headers), separator, *(format_row(row) for row in rows)])


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    sections = [
        (
            "=== A. TABEL VOLUME KELUHAN PER TAHUN ===",
            markdown_table(OUTPUT_DIR / "tabel_volume_keluhan_per_tahun.csv"),
        ),
        (
            "=== B. TABEL RATA-RATA RATING PER TAHUN ===",
            markdown_table(OUTPUT_DIR / "tabel_rata_rata_rating_per_tahun.csv"),
        ),
        (
            "=== C. TABEL KATA KUNCI PER TAHUN ===",
            markdown_table(OUTPUT_DIR / "tabel_kata_kunci_per_tahun.csv"),
        ),
        (
            "=== D. CONTOH KUTIPAN PER TAHUN ===",
            markdown_table(OUTPUT_DIR / "contoh_kutipan_per_tahun.csv"),
        ),
        (
            "=== E. RINGKASAN NARASI ===",
            (OUTPUT_DIR / "ringkasan_narasi.txt").read_text(encoding="utf-8"),
        ),
    ]

    isi = "\n\n".join(f"{judul}\n{konten}" for judul, konten in sections)
    TARGET.write_text(isi, encoding="utf-8")
    print(isi)


if __name__ == "__main__":
    main()
