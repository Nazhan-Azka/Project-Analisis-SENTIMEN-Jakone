import json
import logging
import os
import re
import sys

try:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
except ImportError as exc:
    print("\nDependensi Python belum lengkap untuk visualisasi dan analisis.")
    print(f"Detail: {exc}")
    print("\nInstall dependensi terlebih dahulu, misalnya:")
    print("python -m pip install -r requirements.txt")
    raise SystemExit(1)

try:
    from wordcloud import WordCloud

    WORDCLOUD_AVAILABLE = True
except ImportError:
    WordCloud = None
    WORDCLOUD_AVAILABLE = False


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


DATASET_PATH = "data/final/jakone_modeling_master.csv"
TRAINING_LOG_PATH = "outputs/evaluation/training_log.csv"
CLASSIFICATION_REPORT_PATH = "outputs/evaluation/test_classification_report.csv"
CONFUSION_MATRIX_PATH = "outputs/evaluation/test_confusion_matrix.csv"
METRICS_SUMMARY_PATH = "outputs/evaluation/test_metrics_summary.json"
TEST_PREDICTIONS_PATH = "outputs/evaluation/test_predictions.csv"
SPLIT_SUMMARY_PATH = "outputs/evaluation/split_distribution_summary.csv"

FIGURES_DIR = "outputs/figures"
EVALUATION_DIR = "outputs/evaluation"

LABEL_ORDER = ["negatif", "netral", "positif"]
LABEL_DISTRIBUTION_ORDER = ["positif", "negatif", "netral"]
SPLIT_ORDER = ["train", "validation", "test"]
KEYWORDS = [
    "login",
    "otp",
    "transfer",
    "transaksi",
    "saldo",
    "akun",
    "pin",
    "verifikasi",
    "error",
    "update",
    "maintenance",
    "notifikasi",
    "password",
    "rekening",
    "gagal",
    "lambat",
    "lemot",
    "gangguan",
]

FIGURE_PATHS = {
    "distribution_label_sentiment": "outputs/figures/distribution_label_sentiment.png",
    "distribution_reviews_by_year": "outputs/figures/distribution_reviews_by_year.png",
    "distribution_rating": "outputs/figures/distribution_rating.png",
    "distribution_split_set": "outputs/figures/distribution_split_set.png",
    "training_loss_curve": "outputs/figures/training_loss_curve.png",
    "validation_f1_macro_curve": "outputs/figures/validation_f1_macro_curve.png",
    "validation_accuracy_curve": "outputs/figures/validation_accuracy_curve.png",
    "final_confusion_matrix": "outputs/figures/final_confusion_matrix.png",
    "classification_metrics_per_class": "outputs/figures/classification_metrics_per_class.png",
    "misclassification_by_pair": "outputs/figures/misclassification_by_pair.png",
    "top_keyword_issues": "outputs/figures/top_keyword_issues.png",
    "top_negative_keyword_issues": "outputs/figures/top_negative_keyword_issues.png",
    "wordcloud_positif": "outputs/figures/wordcloud_positif.png",
    "wordcloud_negatif": "outputs/figures/wordcloud_negatif.png",
    "wordcloud_netral": "outputs/figures/wordcloud_netral.png",
}

ANALYSIS_PATHS = {
    "misclassified_predictions": "outputs/evaluation/misclassified_predictions.csv",
    "misclassification_summary": "outputs/evaluation/misclassification_summary.csv",
    "keyword_issue_summary": "outputs/evaluation/keyword_issue_summary.csv",
    "keyword_issue_by_label": "outputs/evaluation/keyword_issue_by_label.csv",
    "final_analysis_summary": "outputs/evaluation/final_analysis_summary.txt",
}

REQUIRED_INPUTS = [
    DATASET_PATH,
    TRAINING_LOG_PATH,
    CLASSIFICATION_REPORT_PATH,
    CONFUSION_MATRIX_PATH,
    METRICS_SUMMARY_PATH,
    TEST_PREDICTIONS_PATH,
    SPLIT_SUMMARY_PATH,
]


logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def prepare_output_dirs():
    """Membuat folder output jika belum tersedia."""
    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(EVALUATION_DIR, exist_ok=True)


def validate_inputs():
    """Mengecek seluruh file input penting sebelum analisis."""
    missing_files = [path for path in REQUIRED_INPUTS if not os.path.isfile(path)]
    if missing_files:
        missing_text = "\n".join(f"- {path}" for path in missing_files)
        raise FileNotFoundError(
            "File input Tahap 9 belum lengkap:\n"
            f"{missing_text}\n"
            "Jalankan tahap sebelumnya terlebih dahulu sebelum membuat visualisasi."
        )


def load_inputs():
    """Membaca dataset dan output evaluasi yang sudah tersedia."""
    logger.info("Membaca dataset final: %s", DATASET_PATH)
    dataset_df = pd.read_csv(DATASET_PATH)
    training_log_df = pd.read_csv(TRAINING_LOG_PATH)
    report_df = pd.read_csv(CLASSIFICATION_REPORT_PATH, index_col=0)
    confusion_matrix_df = pd.read_csv(CONFUSION_MATRIX_PATH, index_col=0)
    predictions_df = pd.read_csv(TEST_PREDICTIONS_PATH)
    split_summary_df = pd.read_csv(SPLIT_SUMMARY_PATH)
    with open(METRICS_SUMMARY_PATH, "r", encoding="utf-8") as file:
        metrics_summary = json.load(file)

    required_dataset_columns = {"clean_review", "label", "split_set"}
    missing_dataset_columns = required_dataset_columns - set(dataset_df.columns)
    if missing_dataset_columns:
        raise ValueError(
            "Kolom wajib tidak ditemukan pada dataset final: "
            + ", ".join(sorted(missing_dataset_columns))
        )

    required_prediction_columns = {"clean_review", "label", "predicted_label", "prediction_correct"}
    missing_prediction_columns = required_prediction_columns - set(predictions_df.columns)
    if missing_prediction_columns:
        raise ValueError(
            "Kolom wajib tidak ditemukan pada test_predictions.csv: "
            + ", ".join(sorted(missing_prediction_columns))
        )

    dataset_df = dataset_df.copy()
    dataset_df["clean_review"] = dataset_df["clean_review"].fillna("").astype(str)
    dataset_df["label"] = dataset_df["label"].fillna("").astype(str).str.strip().str.lower()
    dataset_df["split_set"] = dataset_df["split_set"].fillna("").astype(str).str.strip().str.lower()

    predictions_df = predictions_df.copy()
    predictions_df["clean_review"] = predictions_df["clean_review"].fillna("").astype(str)
    predictions_df["label"] = predictions_df["label"].fillna("").astype(str).str.strip().str.lower()
    predictions_df["predicted_label"] = predictions_df["predicted_label"].fillna("").astype(str).str.strip().str.lower()
    predictions_df["prediction_correct"] = predictions_df["prediction_correct"].astype(str).str.lower().map(
        {"true": True, "false": False}
    )

    return {
        "dataset": dataset_df,
        "training_log": training_log_df,
        "report": report_df,
        "confusion_matrix": confusion_matrix_df,
        "metrics_summary": metrics_summary,
        "predictions": predictions_df,
        "split_summary": split_summary_df,
    }


def save_bar_chart(series, title, xlabel, ylabel, output_path, color="#3B82F6", rotation=0):
    """Membuat bar chart sederhana dari pandas Series."""
    fig, ax = plt.subplots(figsize=(8, 5))
    x_positions = np.arange(len(series))
    bars = ax.bar(x_positions, series.values, color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(series.index.astype(str))
    ax.tick_params(axis="x", rotation=rotation)
    ax.grid(axis="y", linestyle="--", alpha=0.35)

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info("Visualisasi disimpan: %s", output_path)


def create_data_distribution_figures(dataset_df):
    """Membuat visualisasi distribusi label, tahun, rating, dan split dataset."""
    label_counts = dataset_df["label"].value_counts().reindex(LABEL_DISTRIBUTION_ORDER, fill_value=0)
    save_bar_chart(
        label_counts,
        "Distribusi Label Sentimen",
        "Label Sentimen",
        "Jumlah Data",
        FIGURE_PATHS["distribution_label_sentiment"],
        color="#2563EB",
    )

    if "year" in dataset_df.columns:
        year_counts = dataset_df["year"].dropna().astype(int).value_counts().sort_index()
        save_bar_chart(
            year_counts,
            "Distribusi Ulasan per Tahun",
            "Tahun",
            "Jumlah Ulasan",
            FIGURE_PATHS["distribution_reviews_by_year"],
            color="#059669",
        )
    else:
        logger.warning("Kolom year tidak tersedia. Visualisasi distribusi tahun dilewati.")

    if "rating" in dataset_df.columns:
        rating_counts = pd.to_numeric(dataset_df["rating"], errors="coerce").dropna().astype(int)
        rating_counts = rating_counts.value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)
        save_bar_chart(
            rating_counts,
            "Distribusi Rating Ulasan",
            "Rating",
            "Jumlah Ulasan",
            FIGURE_PATHS["distribution_rating"],
            color="#F59E0B",
        )
    else:
        logger.warning("Kolom rating tidak tersedia. Visualisasi distribusi rating dilewati.")

    split_counts = dataset_df["split_set"].value_counts().reindex(SPLIT_ORDER, fill_value=0)
    save_bar_chart(
        split_counts,
        "Distribusi Split Dataset",
        "Split Dataset",
        "Jumlah Data",
        FIGURE_PATHS["distribution_split_set"],
        color="#7C3AED",
    )


def create_training_figures(training_log_df):
    """Membuat visualisasi loss dan metrik validation dari training log."""
    required_loss_columns = {"epoch", "train_loss", "val_loss"}
    if required_loss_columns.issubset(training_log_df.columns):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(training_log_df["epoch"], training_log_df["train_loss"], marker="o", label="Train Loss")
        ax.plot(training_log_df["epoch"], training_log_df["val_loss"], marker="o", label="Validation Loss")
        ax.set_title("Train Loss vs Validation Loss")
        ax.set_xlabel("Epoch")
        ax.set_ylabel("Loss")
        ax.grid(True, linestyle="--", alpha=0.35)
        ax.legend()
        fig.tight_layout()
        fig.savefig(FIGURE_PATHS["training_loss_curve"], dpi=300, bbox_inches="tight")
        plt.close(fig)
        logger.info("Visualisasi disimpan: %s", FIGURE_PATHS["training_loss_curve"])
    else:
        logger.warning("Kolom loss training tidak lengkap. Visualisasi loss dilewati.")

    if {"epoch", "val_f1_macro"}.issubset(training_log_df.columns):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(training_log_df["epoch"], training_log_df["val_f1_macro"], marker="o", color="#DC2626")
        ax.set_title("Validation F1 Macro per Epoch")
        ax.set_xlabel("Epoch")
        ax.set_ylabel("Validation F1 Macro")
        ax.grid(True, linestyle="--", alpha=0.35)
        fig.tight_layout()
        fig.savefig(FIGURE_PATHS["validation_f1_macro_curve"], dpi=300, bbox_inches="tight")
        plt.close(fig)
        logger.info("Visualisasi disimpan: %s", FIGURE_PATHS["validation_f1_macro_curve"])
    else:
        logger.warning("Kolom val_f1_macro tidak tersedia. Visualisasi F1 macro dilewati.")

    if {"epoch", "val_accuracy"}.issubset(training_log_df.columns):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(training_log_df["epoch"], training_log_df["val_accuracy"], marker="o", color="#0891B2")
        ax.set_title("Validation Accuracy per Epoch")
        ax.set_xlabel("Epoch")
        ax.set_ylabel("Validation Accuracy")
        ax.grid(True, linestyle="--", alpha=0.35)
        fig.tight_layout()
        fig.savefig(FIGURE_PATHS["validation_accuracy_curve"], dpi=300, bbox_inches="tight")
        plt.close(fig)
        logger.info("Visualisasi disimpan: %s", FIGURE_PATHS["validation_accuracy_curve"])
    else:
        logger.warning("Kolom val_accuracy tidak tersedia. Visualisasi accuracy dilewati.")


def normalize_confusion_matrix(confusion_matrix_df):
    """Mengubah index/kolom confusion matrix menjadi label bersih."""
    cm = confusion_matrix_df.copy()
    cm.index = [str(index).replace("actual_", "") for index in cm.index]
    cm.columns = [str(column).replace("predicted_", "") for column in cm.columns]
    return cm.reindex(index=LABEL_ORDER, columns=LABEL_ORDER).astype(int)


def create_confusion_matrix_figure(cm_df):
    """Membuat heatmap confusion matrix dengan matplotlib."""
    cm = cm_df.to_numpy()
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
    ax.figure.colorbar(im, ax=ax)
    ax.set(
        xticks=np.arange(len(LABEL_ORDER)),
        yticks=np.arange(len(LABEL_ORDER)),
        xticklabels=LABEL_ORDER,
        yticklabels=LABEL_ORDER,
        xlabel="Label Prediksi",
        ylabel="Label Aktual",
        title="Confusion Matrix Model IndoBERT pada Data Test",
    )

    threshold = cm.max() / 2.0 if cm.max() > 0 else 0
    for row_idx in range(cm.shape[0]):
        for col_idx in range(cm.shape[1]):
            color = "white" if cm[row_idx, col_idx] > threshold else "black"
            ax.text(col_idx, row_idx, f"{cm[row_idx, col_idx]}", ha="center", va="center", color=color)

    fig.tight_layout()
    fig.savefig(FIGURE_PATHS["final_confusion_matrix"], dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info("Visualisasi disimpan: %s", FIGURE_PATHS["final_confusion_matrix"])


def create_classification_metrics_figure(report_df):
    """Membuat grouped bar chart precision, recall, dan F1-score per kelas."""
    class_report = report_df.loc[LABEL_ORDER, ["precision", "recall", "f1-score"]].astype(float)
    x = np.arange(len(LABEL_ORDER))
    width = 0.25

    fig, ax = plt.subplots(figsize=(9, 5))
    metrics = ["precision", "recall", "f1-score"]
    colors = ["#2563EB", "#059669", "#DC2626"]
    for idx, metric in enumerate(metrics):
        values = class_report[metric].to_numpy()
        ax.bar(x + (idx - 1) * width, values, width, label=metric, color=colors[idx])

    ax.set_title("Precision, Recall, dan F1-score per Kelas")
    ax.set_xlabel("Kelas Sentimen")
    ax.set_ylabel("Nilai Metrik")
    ax.set_xticks(x)
    ax.set_xticklabels(LABEL_ORDER)
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURE_PATHS["classification_metrics_per_class"], dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info("Visualisasi disimpan: %s", FIGURE_PATHS["classification_metrics_per_class"])


def analyze_misclassifications(predictions_df):
    """Menyimpan data dan ringkasan salah prediksi."""
    misclassified_df = predictions_df[predictions_df["prediction_correct"] == False].copy()
    misclassified_df.to_csv(ANALYSIS_PATHS["misclassified_predictions"], index=False, encoding="utf-8-sig")
    logger.info("Data salah prediksi disimpan: %s", ANALYSIS_PATHS["misclassified_predictions"])

    if misclassified_df.empty:
        summary_df = pd.DataFrame(columns=["actual_label", "predicted_label", "count"])
    else:
        summary_df = (
            misclassified_df.groupby(["label", "predicted_label"])
            .size()
            .reset_index(name="count")
            .rename(columns={"label": "actual_label"})
            .sort_values("count", ascending=False)
            .reset_index(drop=True)
        )
    summary_df.to_csv(ANALYSIS_PATHS["misclassification_summary"], index=False, encoding="utf-8-sig")
    logger.info("Ringkasan salah prediksi disimpan: %s", ANALYSIS_PATHS["misclassification_summary"])

    if not summary_df.empty:
        pair_labels = summary_df["actual_label"] + " -> " + summary_df["predicted_label"]
        fig, ax = plt.subplots(figsize=(9, 5))
        bars = ax.bar(pair_labels, summary_df["count"], color="#EF4444")
        ax.set_title("Kesalahan Prediksi Berdasarkan Pasangan Aktual-Prediksi")
        ax.set_xlabel("Pasangan Label")
        ax.set_ylabel("Jumlah Salah Prediksi")
        ax.tick_params(axis="x", rotation=30)
        ax.grid(axis="y", linestyle="--", alpha=0.35)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, f"{int(height)}", ha="center", va="bottom")
        fig.tight_layout()
        fig.savefig(FIGURE_PATHS["misclassification_by_pair"], dpi=300, bbox_inches="tight")
        plt.close(fig)
        logger.info("Visualisasi disimpan: %s", FIGURE_PATHS["misclassification_by_pair"])
    else:
        logger.warning("Tidak ada salah prediksi. Visualisasi salah prediksi dilewati.")

    return misclassified_df, summary_df


def count_keyword_occurrences(text_series, keyword):
    """Menghitung total kemunculan keyword sebagai kata utuh sederhana."""
    pattern = re.compile(rf"(?<!\w){re.escape(keyword)}(?!\w)", re.IGNORECASE)
    return int(text_series.fillna("").astype(str).str.count(pattern).sum())


def analyze_keywords(dataset_df):
    """Menghitung keyword issue secara keseluruhan dan berdasarkan label."""
    text_series = dataset_df["clean_review"].fillna("").astype(str).str.lower()
    keyword_rows = []
    for keyword in KEYWORDS:
        keyword_rows.append({"keyword": keyword, "count": count_keyword_occurrences(text_series, keyword)})

    keyword_summary_df = pd.DataFrame(keyword_rows).sort_values("count", ascending=False).reset_index(drop=True)
    keyword_summary_df.to_csv(ANALYSIS_PATHS["keyword_issue_summary"], index=False, encoding="utf-8-sig")
    logger.info("Ringkasan keyword disimpan: %s", ANALYSIS_PATHS["keyword_issue_summary"])

    by_label_rows = []
    for label in LABEL_ORDER:
        label_text = dataset_df.loc[dataset_df["label"] == label, "clean_review"].fillna("").astype(str).str.lower()
        for keyword in KEYWORDS:
            by_label_rows.append(
                {
                    "label": label,
                    "keyword": keyword,
                    "count": count_keyword_occurrences(label_text, keyword),
                }
            )

    keyword_by_label_df = pd.DataFrame(by_label_rows)
    keyword_by_label_df.to_csv(ANALYSIS_PATHS["keyword_issue_by_label"], index=False, encoding="utf-8-sig")
    logger.info("Keyword berdasarkan label disimpan: %s", ANALYSIS_PATHS["keyword_issue_by_label"])

    top_keywords = keyword_summary_df.head(10).set_index("keyword")["count"]
    save_bar_chart(
        top_keywords,
        "Top Keyword Isu Aplikasi JakOne Mobile",
        "Keyword",
        "Jumlah Kemunculan",
        FIGURE_PATHS["top_keyword_issues"],
        color="#0F766E",
        rotation=30,
    )

    negative_keywords = (
        keyword_by_label_df[keyword_by_label_df["label"] == "negatif"]
        .sort_values("count", ascending=False)
        .head(10)
        .set_index("keyword")["count"]
    )
    save_bar_chart(
        negative_keywords,
        "Top Keyword Isu pada Sentimen Negatif",
        "Keyword",
        "Jumlah Kemunculan",
        FIGURE_PATHS["top_negative_keyword_issues"],
        color="#B91C1C",
        rotation=30,
    )

    return keyword_summary_df, keyword_by_label_df


def create_wordclouds(dataset_df):
    """Membuat word cloud per sentimen jika library wordcloud tersedia."""
    created_paths = []
    if not WORDCLOUD_AVAILABLE:
        logger.warning("Library wordcloud tidak tersedia. Pembuatan word cloud dilewati.")
        return created_paths

    for label in ["positif", "negatif", "netral"]:
        text = " ".join(dataset_df.loc[dataset_df["label"] == label, "clean_review"].fillna("").astype(str))
        if not text.strip():
            logger.warning("Tidak ada teks untuk word cloud label %s. Dilewati.", label)
            continue

        wordcloud = WordCloud(
            width=1200,
            height=800,
            background_color="white",
            colormap="viridis",
            max_words=150,
        ).generate(text)

        output_path = FIGURE_PATHS[f"wordcloud_{label}"]
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        ax.set_title(f"Word Cloud Sentimen {label.capitalize()}")
        fig.tight_layout()
        fig.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close(fig)
        created_paths.append(output_path)
        logger.info("Word cloud disimpan: %s", output_path)

    return created_paths


def get_training_summary(training_log_df):
    """Mengambil epoch terbaik dan metrik akhir dari training log."""
    best_idx = training_log_df["val_f1_macro"].astype(float).idxmax()
    best_row = training_log_df.loc[best_idx]
    last_row = training_log_df.iloc[-1]
    return {
        "best_epoch": int(best_row["epoch"]),
        "best_val_f1_macro": float(best_row["val_f1_macro"]),
        "last_train_loss": float(last_row["train_loss"]),
        "last_val_loss": float(last_row["val_loss"]),
    }


def get_confusion_interpretation(cm_df, report_df):
    """Mengambil kelas terkuat, terlemah, dan kesalahan terbanyak."""
    class_f1 = report_df.loc[LABEL_ORDER, "f1-score"].astype(float)
    best_class = class_f1.idxmax()
    weakest_class = class_f1.idxmin()

    mistakes = []
    for actual_label in LABEL_ORDER:
        for predicted_label in LABEL_ORDER:
            if actual_label != predicted_label:
                mistakes.append(
                    {
                        "actual_label": actual_label,
                        "predicted_label": predicted_label,
                        "count": int(cm_df.loc[actual_label, predicted_label]),
                    }
                )
    mistakes_df = pd.DataFrame(mistakes).sort_values("count", ascending=False).reset_index(drop=True)
    top_mistake = mistakes_df.iloc[0].to_dict()
    return best_class, weakest_class, top_mistake


def write_final_analysis_summary(
    dataset_df,
    split_summary_df,
    training_log_df,
    report_df,
    metrics_summary,
    cm_df,
    misclassified_df,
    misclassification_summary_df,
    keyword_summary_df,
    keyword_by_label_df,
):
    """Menulis ringkasan analisis yang dapat digunakan untuk Bab 4."""
    total_data = len(dataset_df)
    label_counts = dataset_df["label"].value_counts().reindex(LABEL_DISTRIBUTION_ORDER, fill_value=0)
    split_counts = dataset_df["split_set"].value_counts().reindex(SPLIT_ORDER, fill_value=0)
    training_summary = get_training_summary(training_log_df)
    best_class, weakest_class, top_mistake = get_confusion_interpretation(cm_df, report_df)

    correct_predictions = int(metrics_summary["test_count"] - len(misclassified_df))
    incorrect_predictions = int(len(misclassified_df))
    top_keyword = keyword_summary_df.iloc[0]
    negative_keyword_df = keyword_by_label_df[keyword_by_label_df["label"] == "negatif"].sort_values("count", ascending=False)
    top_negative_keyword = negative_keyword_df.iloc[0]

    lines = []
    lines.append("Ringkasan Analisis Tahap 9 - Visualisasi dan Analisis Hasil")
    lines.append("=" * 68)
    lines.append("")
    lines.append(f"Jumlah total data: {total_data}")
    lines.append("")
    lines.append("Distribusi label sentimen:")
    for label, count in label_counts.items():
        lines.append(f"- {label}: {int(count)}")
    lines.append("")
    lines.append("Distribusi train/validation/test:")
    for split_name, count in split_counts.items():
        lines.append(f"- {split_name}: {int(count)}")
    lines.append("")
    lines.append("Ringkasan hasil training:")
    lines.append(f"- Epoch terbaik: {training_summary['best_epoch']}")
    lines.append(f"- Validation F1 macro terbaik: {training_summary['best_val_f1_macro']:.6f}")
    lines.append(f"- Train loss terakhir: {training_summary['last_train_loss']:.6f}")
    lines.append(f"- Validation loss terakhir: {training_summary['last_val_loss']:.6f}")
    lines.append("")
    lines.append("Ringkasan hasil test:")
    lines.append(f"- Accuracy: {float(metrics_summary['accuracy']):.6f}")
    lines.append(f"- Macro F1: {float(metrics_summary['macro_f1']):.6f}")
    for label in LABEL_ORDER:
        row = report_df.loc[label]
        lines.append(
            f"- {label}: precision={float(row['precision']):.6f}, "
            f"recall={float(row['recall']):.6f}, f1-score={float(row['f1-score']):.6f}"
        )
    lines.append("")
    lines.append("Interpretasi confusion matrix:")
    lines.append(f"- Kelas yang paling baik dikenali berdasarkan F1-score: {best_class}")
    lines.append(f"- Kelas yang paling lemah berdasarkan F1-score: {weakest_class}")
    lines.append(
        "- Kesalahan terbanyak: "
        f"actual {top_mistake['actual_label']} diprediksi {top_mistake['predicted_label']} "
        f"sebanyak {int(top_mistake['count'])} data"
    )
    lines.append("")
    lines.append("Ringkasan analisis salah prediksi:")
    lines.append(f"- Total prediksi test: {int(metrics_summary['test_count'])}")
    lines.append(f"- Prediksi benar: {correct_predictions}")
    lines.append(f"- Prediksi salah: {incorrect_predictions}")
    if not misclassification_summary_df.empty:
        for _, row in misclassification_summary_df.head(5).iterrows():
            lines.append(
                f"- {row['actual_label']} -> {row['predicted_label']}: {int(row['count'])} data"
            )
    lines.append("")
    lines.append("Ringkasan keyword issue:")
    lines.append(f"- Keyword paling sering muncul: {top_keyword['keyword']} ({int(top_keyword['count'])} kemunculan)")
    lines.append(
        "- Keyword dominan pada sentimen negatif: "
        f"{top_negative_keyword['keyword']} ({int(top_negative_keyword['count'])} kemunculan)"
    )
    lines.append("")
    lines.append("Kesimpulan singkat:")
    lines.append(
        "Model IndoBERT sudah cukup baik secara keseluruhan. Kelas positif dan negatif "
        "memiliki performa tinggi, sedangkan kelas netral masih menjadi kelemahan utama. "
        "Kemungkinan penyebabnya adalah jumlah data netral yang sedikit, ambiguitas teks netral, "
        "dan noise dari proses labeling berbasis lexicon."
    )

    with open(ANALYSIS_PATHS["final_analysis_summary"], "w", encoding="utf-8") as file:
        file.write("\n".join(lines))
    logger.info("Ringkasan analisis final disimpan: %s", ANALYSIS_PATHS["final_analysis_summary"])

    return {
        "total_data": total_data,
        "best_class": best_class,
        "weakest_class": weakest_class,
        "top_keyword": str(top_keyword["keyword"]),
        "top_keyword_count": int(top_keyword["count"]),
        "top_negative_keyword": str(top_negative_keyword["keyword"]),
        "top_negative_keyword_count": int(top_negative_keyword["count"]),
        "incorrect_predictions": incorrect_predictions,
        "correct_predictions": correct_predictions,
        "top_mistake": top_mistake,
    }


def run_visualization_analysis():
    """Menjalankan seluruh proses visualisasi dan analisis Tahap 9."""
    prepare_output_dirs()
    validate_inputs()
    data = load_inputs()

    dataset_df = data["dataset"]
    training_log_df = data["training_log"]
    report_df = data["report"]
    cm_df = normalize_confusion_matrix(data["confusion_matrix"])
    metrics_summary = data["metrics_summary"]
    predictions_df = data["predictions"]
    split_summary_df = data["split_summary"]

    create_data_distribution_figures(dataset_df)
    create_training_figures(training_log_df)
    create_confusion_matrix_figure(cm_df)
    create_classification_metrics_figure(report_df)
    misclassified_df, misclassification_summary_df = analyze_misclassifications(predictions_df)
    keyword_summary_df, keyword_by_label_df = analyze_keywords(dataset_df)
    created_wordcloud_paths = create_wordclouds(dataset_df)
    summary = write_final_analysis_summary(
        dataset_df,
        split_summary_df,
        training_log_df,
        report_df,
        metrics_summary,
        cm_df,
        misclassified_df,
        misclassification_summary_df,
        keyword_summary_df,
        keyword_by_label_df,
    )

    figure_outputs = [
        FIGURE_PATHS["distribution_label_sentiment"],
        FIGURE_PATHS["distribution_reviews_by_year"],
        FIGURE_PATHS["distribution_rating"],
        FIGURE_PATHS["distribution_split_set"],
        FIGURE_PATHS["training_loss_curve"],
        FIGURE_PATHS["validation_f1_macro_curve"],
        FIGURE_PATHS["validation_accuracy_curve"],
        FIGURE_PATHS["final_confusion_matrix"],
        FIGURE_PATHS["classification_metrics_per_class"],
        FIGURE_PATHS["misclassification_by_pair"],
        FIGURE_PATHS["top_keyword_issues"],
        FIGURE_PATHS["top_negative_keyword_issues"],
    ] + created_wordcloud_paths

    analysis_outputs = list(ANALYSIS_PATHS.values())

    print("\nRingkasan Tahap 9 - Visualisasi dan Analisis Hasil")
    print(f"Jumlah total data: {summary['total_data']}")
    print(f"Keyword paling dominan: {summary['top_keyword']} ({summary['top_keyword_count']})")
    print(
        "Keyword dominan pada sentimen negatif: "
        f"{summary['top_negative_keyword']} ({summary['top_negative_keyword_count']})"
    )
    print(f"Kelas performa terbaik: {summary['best_class']}")
    print(f"Kelas performa terlemah: {summary['weakest_class']}")
    print(f"Prediksi benar: {summary['correct_predictions']}")
    print(f"Prediksi salah: {summary['incorrect_predictions']}")
    print(
        "Kesalahan terbanyak: "
        f"{summary['top_mistake']['actual_label']} -> {summary['top_mistake']['predicted_label']} "
        f"({int(summary['top_mistake']['count'])})"
    )
    print("\nFile visualisasi:")
    for path in figure_outputs:
        if os.path.isfile(path):
            print(f"- {path}")
    print("\nFile analisis:")
    for path in analysis_outputs:
        print(f"- {path}")

    return {
        "summary": summary,
        "figure_outputs": [path for path in figure_outputs if os.path.isfile(path)],
        "analysis_outputs": analysis_outputs,
    }


def main():
    try:
        run_visualization_analysis()
    except (FileNotFoundError, ValueError, RuntimeError, OSError) as exc:
        print("\nProses visualisasi dan analisis gagal.")
        print(str(exc))
        print("\nPerbaiki file input atau dependensi terlebih dahulu, lalu jalankan ulang script.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
