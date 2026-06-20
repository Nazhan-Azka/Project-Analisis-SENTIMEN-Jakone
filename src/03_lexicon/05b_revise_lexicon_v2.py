import logging
from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
LEXICON_DIR = ROOT_DIR / "data" / "lexicon"
ACTIVE_LEXICON_DIR = LEXICON_DIR / "active"
ARCHIVE_LEXICON_DIR = LEXICON_DIR / "archive"

INPUT_POSITIVE_PATH = ARCHIVE_LEXICON_DIR / "lexicon_final_positive.tsv"
INPUT_NEGATIVE_PATH = ARCHIVE_LEXICON_DIR / "lexicon_final_negative.tsv"
OUTPUT_POSITIVE_PATH = ACTIVE_LEXICON_DIR / "lexicon_v3_positive.tsv"
OUTPUT_NEGATIVE_PATH = ACTIVE_LEXICON_DIR / "lexicon_v3_negative.tsv"
ASPECT_TERMS_PATH = ACTIVE_LEXICON_DIR / "kata_aspek_domain.txt"

NEGATION_TERMS = {
    "tidak",
    "bukan",
    "belum",
    "kurang",
    "jangan",
    "tak",
    "ga",
    "gak",
    "nggak",
    "ngga",
    "kagak",
    "tanpa",
    "tanpa ada",
}

ASPECT_TERMS = {
    "saldo",
    "transaksi",
    "aktivasi",
    "kode",
    "login",
    "verifikasi",
    "akun",
    "rekening",
    "transfer",
    "data",
    "otp",
    "pin",
    "password",
    "autentikasi",
    "qris",
    "blokir",
    "masuk",
}

GENERAL_TERMS = {
    "ada",
    "mau",
    "coba",
    "perlu",
    "tolong",
    "kasih",
    "informasi",
    "penting",
    "masuk",
    "normal",
    "respon",
    "administrator",
    "cukup",
    "bebas",
    "selesai",
}

MOVE_POSITIVE_TO_NEGATIVE = {
    "absurd": -0.6,
    "acuh tak acuh": -0.6,
}

MOVE_NEGATIVE_TO_POSITIVE = {
    "bantu": 0.6,
    "jelas": 0.6,
    "sederhana": 0.6,
}

IMPORTANT_POSITIVE = {
    "aman": 0.6,
    "nyaman": 0.6,
    "mudah": 0.6,
    "lancar": 0.6,
    "cepat": 0.6,
    "berhasil": 0.6,
    "bagus": 0.6,
    "baik": 0.6,
    "mantap": 0.6,
    "puas": 0.6,
    "responsif": 0.6,
    "stabil": 0.6,
    "mempermudah": 0.6,
    "membantu": 0.6,
    "terbaik": 0.6,
}

IMPORTANT_NEGATIVE = {
    "error": -0.6,
    "gagal": -0.6,
    "gangguan": -0.6,
    "masalah": -0.6,
    "penipuan": -0.6,
    "bobol": -0.6,
    "membobol": -0.6,
    "ditipu": -0.6,
    "bahaya": -0.6,
    "hilang": -0.6,
    "bug": -0.6,
    "lambat": -0.6,
    "ribet": -0.6,
    "susah": -0.6,
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def read_lexicon(path: Path) -> pd.DataFrame:
    logger.info("Membaca lexicon: %s", path.relative_to(ROOT_DIR))
    if not path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

    df = pd.read_csv(path, sep="\t")
    required_columns = {"word", "weight"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Kolom wajib tidak ditemukan pada {path}: {missing_columns}")

    df = df[["word", "weight"]].copy()
    df["word"] = df["word"].fillna("").astype(str).str.strip().str.lower()
    df["weight"] = pd.to_numeric(df["weight"], errors="coerce")
    df = df[(df["word"] != "") & df["weight"].notna()].copy()
    return df.drop_duplicates("word", keep="first").reset_index(drop=True)


def remove_terms(df: pd.DataFrame, terms: set[str]) -> tuple[pd.DataFrame, int]:
    before = len(df)
    cleaned = df[~df["word"].isin(terms)].copy()
    return cleaned.reset_index(drop=True), before - len(cleaned)


def upsert_with_bound(
    df: pd.DataFrame,
    word: str,
    required_weight: float,
    positive: bool,
) -> pd.DataFrame:
    df = df.copy()
    mask = df["word"] == word

    if mask.any():
        current_weight = float(df.loc[mask, "weight"].iloc[0])
        if positive and current_weight < required_weight:
            df.loc[mask, "weight"] = required_weight
        elif not positive and current_weight > required_weight:
            df.loc[mask, "weight"] = required_weight
    else:
        df = pd.concat(
            [df, pd.DataFrame([{"word": word, "weight": required_weight}])],
            ignore_index=True,
        )
    return df


def sort_and_save(df: pd.DataFrame, path: Path) -> None:
    output = df.drop_duplicates("word", keep="first").sort_values("word").reset_index(drop=True)
    output.to_csv(path, sep="\t", index=False)
    logger.info("Menyimpan %s (%s kata)", path.relative_to(ROOT_DIR), len(output))


def main() -> None:
    logger.info("Memulai revisi residual lexicon v3")
    LEXICON_DIR.mkdir(parents=True, exist_ok=True)
    ACTIVE_LEXICON_DIR.mkdir(parents=True, exist_ok=True)

    positive = read_lexicon(INPUT_POSITIVE_PATH)
    negative = read_lexicon(INPUT_NEGATIVE_PATH)
    positive_initial = len(positive)
    negative_initial = len(negative)

    negative, removed_negation = remove_terms(negative, NEGATION_TERMS)

    positive, removed_aspect_positive = remove_terms(positive, ASPECT_TERMS)
    negative, removed_aspect_negative = remove_terms(negative, ASPECT_TERMS)
    removed_aspect = removed_aspect_positive + removed_aspect_negative

    positive, removed_general_positive = remove_terms(positive, GENERAL_TERMS)
    negative, removed_general_negative = remove_terms(negative, GENERAL_TERMS)
    removed_general = removed_general_positive + removed_general_negative

    moved_positive_to_negative = 0
    for word, weight in MOVE_POSITIVE_TO_NEGATIVE.items():
        positive, removed_count = remove_terms(positive, {word})
        moved_positive_to_negative += removed_count
        negative = upsert_with_bound(negative, word, weight, positive=False)

    moved_negative_to_positive = 0
    for word, weight in MOVE_NEGATIVE_TO_POSITIVE.items():
        negative, removed_count = remove_terms(negative, {word})
        moved_negative_to_positive += removed_count
        positive = upsert_with_bound(positive, word, weight, positive=True)

    for word, weight in IMPORTANT_POSITIVE.items():
        positive = upsert_with_bound(positive, word, weight, positive=True)

    for word, weight in IMPORTANT_NEGATIVE.items():
        negative = upsert_with_bound(negative, word, weight, positive=False)

    overlap = set(positive["word"]) & set(negative["word"])
    if overlap:
        raise ValueError(f"Masih ada kata overlap positif-negatif: {sorted(overlap)[:20]}")

    ASPECT_TERMS_PATH.write_text("\n".join(sorted(ASPECT_TERMS)) + "\n", encoding="utf-8")
    logger.info("Menyimpan daftar kata aspek: %s", ASPECT_TERMS_PATH.relative_to(ROOT_DIR))

    sort_and_save(positive, OUTPUT_POSITIVE_PATH)
    sort_and_save(negative, OUTPUT_NEGATIVE_PATH)

    print("\nRingkasan revisi residual lexicon v3")
    print(f"Positif awal: {positive_initial}")
    print(f"Negatif awal: {negative_initial}")
    print(f"Kata negasi dihapus dari negatif: {removed_negation}")
    print(f"Kata aspek dihapus dari positif: {removed_aspect_positive}")
    print(f"Kata aspek dihapus dari negatif: {removed_aspect_negative}")
    print(f"Total kata aspek dihapus: {removed_aspect}")
    print(f"Kata umum dihapus dari positif: {removed_general_positive}")
    print(f"Kata umum dihapus dari negatif: {removed_general_negative}")
    print(f"Total kata umum dihapus: {removed_general}")
    print(f"Kata dipindahkan positif ke negatif: {moved_positive_to_negative}")
    print(f"Kata dipindahkan negatif ke positif: {moved_negative_to_positive}")
    print(f"Total kata positif v3: {len(positive.drop_duplicates('word'))}")
    print(f"Total kata negatif v3: {len(negative.drop_duplicates('word'))}")
    print(f"Output positif v3: {OUTPUT_POSITIVE_PATH.relative_to(ROOT_DIR)}")
    print(f"Output negatif v3: {OUTPUT_NEGATIVE_PATH.relative_to(ROOT_DIR)}")
    print(f"Output kata aspek: {ASPECT_TERMS_PATH.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
