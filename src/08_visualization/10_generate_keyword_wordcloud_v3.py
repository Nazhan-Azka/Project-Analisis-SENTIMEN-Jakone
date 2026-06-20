from pathlib import Path
import logging
import re
import sys

import pandas as pd

try:
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
except ImportError as exc:
    print("\nLibrary wordcloud/matplotlib belum tersedia.")
    print(f"Detail: {exc}")
    print("\nInstall dependency terlebih dahulu:")
    print("python -m pip install -r requirements.txt")
    raise SystemExit(1)


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


ROOT_DIR = Path(__file__).resolve().parents[2]
DATASET_PATH = ROOT_DIR / "data" / "final" / "06_jakone_modeling_master_v3.csv"
TEST_PREDICTIONS_PATH = ROOT_DIR / "outputs" / "evaluation" / "indobert_v3_baseline" / "test_predictions.csv"

ANALYSIS_DIR = ROOT_DIR / "outputs" / "analysis" / "indobert_v3_baseline"
FIGURE_DIR = ROOT_DIR / "outputs" / "figures" / "indobert_v3_baseline"

KEYWORD_SUMMARY_PATH = ANALYSIS_DIR / "keyword_issue_summary_v3.csv"
KEYWORD_BY_LABEL_PATH = ANALYSIS_DIR / "keyword_issue_by_label_v3.csv"
MISCLASSIFIED_KEYWORD_PATH = ANALYSIS_DIR / "keyword_issue_misclassified_v3.csv"

TEXT_COLUMN = "review"
LABEL_COLUMN = "label"
SPLIT_COLUMN = "split_set"
LABEL_ORDER = ["negatif", "netral", "positif"]

KEYWORDS = [
    "otp",
    "pin",
    "password",
    "login",
    "verifikasi",
    "kode",
    "akun",
    "saldo",
    "transaksi",
    "transfer",
    "rekening",
    "qris",
    "blokir",
    "error",
    "gagal",
    "hilang",
    "penipuan",
    "fraud",
    "bobol",
    "aman",
]

STOPWORDS = {
    "yang",
    "dan",
    "di",
    "ke",
    "dari",
    "ini",
    "itu",
    "untuk",
    "dengan",
    "saya",
    "aku",
    "nya",
    "si",
    "kok",
    "dong",
    "deh",
    "lah",
    "atau",
    "pada",
    "karena",
    "jadi",
    "sudah",
    "belum",
    "akan",
    "agar",
    "dalam",
    "sebagai",
    "seperti",
    "juga",
    "saja",
    "kami",
    "anda",
}

DOMAIN_TERMS_KEEP = {"otp", "login", "saldo", "transaksi", "akun", "pin", "kode"}

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def validate_inputs() -> None:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset v3 tidak ditemukan: {DATASET_PATH}")


def load_dataset() -> pd.DataFrame:
    logger.info("Membaca dataset v3: %s", DATASET_PATH.relative_to(ROOT_DIR))
    df = pd.read_csv(DATASET_PATH)
    required_columns = {TEXT_COLUMN, LABEL_COLUMN, SPLIT_COLUMN}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Kolom wajib tidak ditemukan: {', '.join(sorted(missing_columns))}")

    df = df.copy()
    df[TEXT_COLUMN] = df[TEXT_COLUMN].fillna("").astype(str).str.lower()
    df[LABEL_COLUMN] = df[LABEL_COLUMN].fillna("").astype(str).str.strip().str.lower()
    df[SPLIT_COLUMN] = df[SPLIT_COLUMN].fillna("").astype(str).str.strip().str.lower()
    df = df[(df[TEXT_COLUMN].str.strip() != "") & df[LABEL_COLUMN].isin(LABEL_ORDER)].reset_index(drop=True)
    return df


def count_keyword_occurrences(texts: pd.Series, keyword: str) -> int:
    pattern = re.compile(rf"(?<!\w){re.escape(keyword)}(?!\w)", flags=re.IGNORECASE)
    return int(texts.fillna("").astype(str).apply(lambda text: len(pattern.findall(text))).sum())


def build_keyword_summary(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    total_rows = len(df)
    text_series = df[TEXT_COLUMN]
    label_totals = df[LABEL_COLUMN].value_counts().reindex(LABEL_ORDER, fill_value=0)

    summary_rows = []
    by_label_rows = []

    for keyword in KEYWORDS:
        total_count = count_keyword_occurrences(text_series, keyword)
        label_counts = {}
        for label in LABEL_ORDER:
            label_text = df.loc[df[LABEL_COLUMN] == label, TEXT_COLUMN]
            count = count_keyword_occurrences(label_text, keyword)
            label_counts[label] = count
            label_total = int(label_totals[label])
            by_label_rows.append(
                {
                    "keyword": keyword,
                    "label": label,
                    "count": count,
                    "percentage_in_label": round((count / label_total * 100) if label_total else 0, 4),
                }
            )

        summary_rows.append(
            {
                "keyword": keyword,
                "total_count": total_count,
                "count": total_count,
                "percentage": round((total_count / total_rows * 100) if total_rows else 0, 4),
                "count_negatif": label_counts["negatif"],
                "count_netral": label_counts["netral"],
                "count_positif": label_counts["positif"],
            }
        )

    summary_df = pd.DataFrame(summary_rows).sort_values("total_count", ascending=False)
    by_label_df = pd.DataFrame(by_label_rows).sort_values(["label", "count"], ascending=[True, False])
    return summary_df, by_label_df


def build_misclassified_keyword_summary() -> pd.DataFrame | None:
    if not TEST_PREDICTIONS_PATH.exists():
        logger.warning("File test_predictions v3 tidak ditemukan, ringkasan salah prediksi dilewati: %s", TEST_PREDICTIONS_PATH)
        return None

    predictions = pd.read_csv(TEST_PREDICTIONS_PATH)
    required_columns = {"review", "true_label", "pred_label"}
    if not required_columns.issubset(predictions.columns):
        logger.warning("Kolom test_predictions tidak lengkap, ringkasan salah prediksi dilewati.")
        return None

    predictions = predictions.copy()
    predictions["review"] = predictions["review"].fillna("").astype(str).str.lower()
    misclassified = predictions[predictions["true_label"] != predictions["pred_label"]].copy()
    rows = []
    for keyword in KEYWORDS:
        rows.append(
            {
                "keyword": keyword,
                "misclassified_count": count_keyword_occurrences(misclassified["review"], keyword),
            }
        )
    return pd.DataFrame(rows).sort_values("misclassified_count", ascending=False)


def clean_for_wordcloud(text: str) -> str:
    text = re.sub(r"[^a-z0-9\s]", " ", str(text).lower())
    tokens = []
    for token in text.split():
        if token in DOMAIN_TERMS_KEEP or token not in STOPWORDS:
            tokens.append(token)
    return " ".join(tokens)


def generate_wordclouds(df: pd.DataFrame) -> list[Path]:
    output_paths = []
    for label in ["positif", "negatif", "netral"]:
        label_text = " ".join(df.loc[df[LABEL_COLUMN] == label, TEXT_COLUMN].apply(clean_for_wordcloud))
        if not label_text.strip():
            logger.warning("Tidak ada teks untuk wordcloud label %s. Dilewati.", label)
            continue

        wordcloud = WordCloud(
            width=1200,
            height=700,
            background_color="white",
            stopwords=STOPWORDS - DOMAIN_TERMS_KEEP,
            colormap="viridis",
            max_words=180,
            collocations=False,
        ).generate(label_text)

        output_path = FIGURE_DIR / f"wordcloud_{label}_v3.png"
        plt.figure(figsize=(12, 7))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.savefig(output_path, dpi=200, bbox_inches="tight", pad_inches=0.05)
        plt.close()
        output_paths.append(output_path)
        logger.info("Wordcloud disimpan: %s", output_path.relative_to(ROOT_DIR))

    return output_paths


def save_outputs(summary_df: pd.DataFrame, by_label_df: pd.DataFrame, misclassified_df: pd.DataFrame | None) -> list[Path]:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    summary_df.to_csv(KEYWORD_SUMMARY_PATH, index=False, encoding="utf-8-sig")
    by_label_df.to_csv(KEYWORD_BY_LABEL_PATH, index=False, encoding="utf-8-sig")

    output_paths = [KEYWORD_SUMMARY_PATH, KEYWORD_BY_LABEL_PATH]
    if misclassified_df is not None:
        misclassified_df.to_csv(MISCLASSIFIED_KEYWORD_PATH, index=False, encoding="utf-8-sig")
        output_paths.append(MISCLASSIFIED_KEYWORD_PATH)
    return output_paths


def print_summary(df: pd.DataFrame, output_paths: list[Path], wordcloud_paths: list[Path]) -> None:
    print("\nRingkasan Keyword Issue & WordCloud V3")
    print(f"Jumlah data: {len(df)}")
    print("\nDistribusi label:")
    print(df[LABEL_COLUMN].value_counts().reindex(LABEL_ORDER, fill_value=0).to_string())
    print(f"\nJumlah keyword dianalisis: {len(KEYWORDS)}")
    print("\nFile output keyword:")
    for path in output_paths:
        print(f"- {path.relative_to(ROOT_DIR)}")
    print("\nFile output wordcloud:")
    for path in wordcloud_paths:
        print(f"- {path.relative_to(ROOT_DIR)}")


def main() -> None:
    try:
        validate_inputs()
        ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
        FIGURE_DIR.mkdir(parents=True, exist_ok=True)
        df = load_dataset()
        summary_df, by_label_df = build_keyword_summary(df)
        misclassified_df = build_misclassified_keyword_summary()
        output_paths = save_outputs(summary_df, by_label_df, misclassified_df)
        wordcloud_paths = generate_wordclouds(df)
        print_summary(df, output_paths, wordcloud_paths)
    except (FileNotFoundError, ValueError, RuntimeError, OSError) as exc:
        print("\nProses generate keyword issue dan wordcloud v3 gagal.")
        print(str(exc))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
