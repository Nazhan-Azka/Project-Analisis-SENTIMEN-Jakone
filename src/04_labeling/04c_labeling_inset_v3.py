from pathlib import Path
import logging
import sys

import numpy as np
import pandas as pd


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT_DIR / "data" / "processed" / "jakone_reviews_clean.csv"
V1_PATH = ROOT_DIR / "data" / "processed" / "jakone_reviews_labeled.csv"
V2_PATH = ROOT_DIR / "data" / "final" / "06_jakone_modeling_refined_highconf.csv"
POSITIVE_LEXICON_PATH = ROOT_DIR / "data" / "lexicon" / "active" / "lexicon_v3_positive.tsv"
NEGATIVE_LEXICON_PATH = ROOT_DIR / "data" / "lexicon" / "active" / "lexicon_v3_negative.tsv"
OUTPUT_PATH = ROOT_DIR / "data" / "processed" / "jakone_reviews_labeled_v3.csv"
COMPARISON_PATH = ROOT_DIR / "outputs" / "audit" / "perbandingan_label_v1_v2_v3.csv"

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
    "ngga",
    "kagak",
    "tanpa",
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def validate_input_files() -> None:
    required_paths = [
        DATA_PATH,
        V1_PATH,
        POSITIVE_LEXICON_PATH,
        NEGATIVE_LEXICON_PATH,
    ]
    missing_paths = [path for path in required_paths if not path.exists()]
    if missing_paths:
        missing_text = "\n".join(f"- {path.relative_to(ROOT_DIR)}" for path in missing_paths)
        raise FileNotFoundError(f"File input belum lengkap:\n{missing_text}")


def load_lexicon(path: Path) -> pd.DataFrame:
    logger.info("Membaca lexicon: %s", path.relative_to(ROOT_DIR))
    df = pd.read_csv(path, sep="\t")
    required_columns = {"word", "weight"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Kolom lexicon tidak lengkap pada {path}: {missing_columns}")

    df = df[["word", "weight"]].copy()
    df["word"] = df["word"].fillna("").astype(str).str.strip().str.lower()
    df["weight"] = pd.to_numeric(df["weight"], errors="coerce")
    df = df[(df["word"] != "") & df["weight"].notna()].copy()
    return df.drop_duplicates("word", keep="first")


def build_lexicon_dict(df: pd.DataFrame) -> dict[str, float]:
    return {row.word: float(row.weight) for row in df.itertuples(index=False)}


def hitung_skor(teks, pos_dict, neg_dict, negation_words):
    tokens = str(teks).lower().split()
    skor_total = 0.0
    i = 0

    while i < len(tokens):
        if i + 2 < len(tokens):
            trigram = " ".join(tokens[i : i + 3])
            if trigram in pos_dict:
                ada_negasi = i > 0 and tokens[i - 1] in negation_words
                bobot = pos_dict[trigram]
                skor_total += -bobot if ada_negasi else bobot
                i += 3
                continue
            if trigram in neg_dict:
                ada_negasi = i > 0 and tokens[i - 1] in negation_words
                bobot = neg_dict[trigram]
                skor_total += -bobot if ada_negasi else bobot
                i += 3
                continue

        if i + 1 < len(tokens):
            bigram = " ".join(tokens[i : i + 2])
            if bigram in pos_dict:
                ada_negasi = i > 0 and tokens[i - 1] in negation_words
                bobot = pos_dict[bigram]
                skor_total += -bobot if ada_negasi else bobot
                i += 2
                continue
            if bigram in neg_dict:
                ada_negasi = i > 0 and tokens[i - 1] in negation_words
                bobot = neg_dict[bigram]
                skor_total += -bobot if ada_negasi else bobot
                i += 2
                continue

        token = tokens[i]
        ada_negasi = i > 0 and tokens[i - 1] in negation_words
        if token in pos_dict:
            bobot = pos_dict[token]
            skor_total += -bobot if ada_negasi else bobot
        elif token in neg_dict:
            bobot = neg_dict[token]
            skor_total += -bobot if ada_negasi else bobot
        i += 1

    return float(skor_total)


def assign_label(score: float) -> str:
    if score > 0:
        return "positif"
    if score < 0:
        return "negatif"
    return "netral"


def label_reviews_v3(df: pd.DataFrame, pos_dict: dict[str, float], neg_dict: dict[str, float]) -> pd.DataFrame:
    logger.info("Menghitung skor dan label v3")
    output = df.copy()
    output[TEXT_COLUMN] = output[TEXT_COLUMN].fillna("").astype(str)
    output["lexicon_score_v3"] = output[TEXT_COLUMN].apply(
        lambda text: hitung_skor(text, pos_dict, neg_dict, NEGATION_WORDS)
    )
    output["label_v3"] = output["lexicon_score_v3"].apply(assign_label)
    return output


def load_v1_reference() -> pd.DataFrame:
    logger.info("Membaca label v1: %s", V1_PATH.relative_to(ROOT_DIR))
    v1_df = pd.read_csv(V1_PATH)
    required_columns = {TEXT_COLUMN, "label", "lexicon_score"}
    missing_columns = required_columns - set(v1_df.columns)
    if missing_columns:
        raise ValueError(f"Kolom wajib v1 tidak ditemukan: {missing_columns}")

    columns = [TEXT_COLUMN, "label", "lexicon_score"]
    if "review_id" in v1_df.columns:
        columns.insert(0, "review_id")
    return v1_df[columns].rename(
        columns={"label": "label_v1", "lexicon_score": "skor_v1"}
    )


def load_v2_reference(v1_reference: pd.DataFrame) -> pd.DataFrame:
    if not V2_PATH.exists():
        logger.warning("File v2 tidak ditemukan. Label v2 akan disamakan dengan v1.")
        v2_df = v1_reference.copy()
        return v2_df.rename(columns={"label_v1": "label_v2", "skor_v1": "skor_v2"})

    logger.info("Membaca label v2: %s", V2_PATH.relative_to(ROOT_DIR))
    v2_raw = pd.read_csv(V2_PATH)
    required_columns = {TEXT_COLUMN, "label", "lexicon_score"}
    missing_columns = required_columns - set(v2_raw.columns)
    if missing_columns:
        raise ValueError(f"Kolom wajib v2 tidak ditemukan: {missing_columns}")

    columns = [TEXT_COLUMN, "label", "lexicon_score"]
    if "review_id" in v2_raw.columns:
        columns.insert(0, "review_id")
    return v2_raw[columns].rename(
        columns={"label": "label_v2", "lexicon_score": "skor_v2"}
    )


def build_comparison(v3_df: pd.DataFrame) -> pd.DataFrame:
    v1_df = load_v1_reference()
    v2_df = load_v2_reference(v1_df)
    v3_columns = [TEXT_COLUMN, "label_v3", "lexicon_score_v3"]
    if "review_id" in v3_df.columns:
        v3_columns.insert(0, "review_id")
    v3_ref = v3_df[v3_columns].rename(columns={"lexicon_score_v3": "skor_v3"})

    if "review_id" in v3_ref.columns and "review_id" in v1_df.columns:
        comparison = v3_ref.merge(v1_df, on="review_id", how="left", suffixes=("", "_v1text"))
        if TEXT_COLUMN in comparison.columns and f"{TEXT_COLUMN}_v1text" in comparison.columns:
            comparison = comparison.drop(columns=[f"{TEXT_COLUMN}_v1text"])
    else:
        comparison = v3_ref.merge(v1_df, on=TEXT_COLUMN, how="left")

    if "review_id" in comparison.columns and "review_id" in v2_df.columns:
        comparison = comparison.merge(v2_df, on="review_id", how="left", suffixes=("", "_v2text"))
        if f"{TEXT_COLUMN}_v2text" in comparison.columns:
            comparison = comparison.drop(columns=[f"{TEXT_COLUMN}_v2text"])
    else:
        comparison = comparison.merge(v2_df, on=TEXT_COLUMN, how="left")

    comparison["label_v2"] = comparison["label_v2"].fillna(comparison["label_v1"])
    comparison["skor_v2"] = comparison["skor_v2"].fillna(comparison["skor_v1"])

    columns = [TEXT_COLUMN, "label_v1", "label_v2", "label_v3", "skor_v1", "skor_v2", "skor_v3"]
    return comparison[columns]


def print_summary(v3_df: pd.DataFrame, comparison_df: pd.DataFrame) -> None:
    total = len(v3_df)
    label_counts = v3_df["label_v3"].value_counts().reindex(["positif", "negatif", "netral"], fill_value=0)
    label_percentages = (label_counts / total * 100).round(2)

    changed_v2_to_v3 = int((comparison_df["label_v2"] != comparison_df["label_v3"]).sum())
    changed_v1_to_v3 = int((comparison_df["label_v1"] != comparison_df["label_v3"]).sum())

    print("\nRingkasan Labeling V3")
    print(f"Total data: {total}")
    print("\nDistribusi label v3:")
    for label in ["positif", "negatif", "netral"]:
        print(f"- {label}: {int(label_counts[label])} ({label_percentages[label]}%)")
    print(f"\nData berubah dari v2 ke v3: {changed_v2_to_v3}")
    print(f"Data berubah dari v1 ke v3: {changed_v1_to_v3}")
    print(f"\nOutput label v3: {OUTPUT_PATH.relative_to(ROOT_DIR)}")
    print(f"Output perbandingan: {COMPARISON_PATH.relative_to(ROOT_DIR)}")


def main() -> None:
    try:
        logger.info("Memulai labeling v3 dengan dukungan frasa multi-kata")
        validate_input_files()
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        COMPARISON_PATH.parent.mkdir(parents=True, exist_ok=True)

        df = pd.read_csv(DATA_PATH)
        if TEXT_COLUMN not in df.columns:
            raise ValueError(f"Kolom wajib tidak ditemukan: {TEXT_COLUMN}")

        positive_dict = build_lexicon_dict(load_lexicon(POSITIVE_LEXICON_PATH))
        negative_dict = build_lexicon_dict(load_lexicon(NEGATIVE_LEXICON_PATH))
        overlap = set(positive_dict) & set(negative_dict)
        if overlap:
            raise ValueError(f"Masih ada overlap lexicon positif-negatif: {sorted(overlap)[:20]}")

        v3_df = label_reviews_v3(df, positive_dict, negative_dict)
        comparison_df = build_comparison(v3_df)

        logger.info("Menyimpan hasil labeling v3: %s", OUTPUT_PATH.relative_to(ROOT_DIR))
        v3_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

        logger.info("Menyimpan perbandingan label: %s", COMPARISON_PATH.relative_to(ROOT_DIR))
        comparison_df.to_csv(COMPARISON_PATH, index=False, encoding="utf-8-sig")

        print_summary(v3_df, comparison_df)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print("\nProses labeling v3 gagal.")
        print(str(exc))
        raise


if __name__ == "__main__":
    main()
