import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

from utils import (  # noqa: E402
    file_exists,
    format_percent,
    load_csv,
    load_json,
    load_model_and_tokenizer,
    load_text,
    get_confidence_status,
    predict_sentiment,
    render_dataset_filter_panel,
    render_dataset_hero,
    render_dataset_insights,
    render_dataset_metric_cards,
    render_dataset_note,
    render_dataset_preview,
    render_dataset_quality_cards,
    render_dataset_visualization_tabs,
    render_labeling_distribution_chart,
    render_labeling_examples,
    render_labeling_flow_vertical,
    render_labeling_hero,
    render_labeling_limitation_note,
    render_labeling_method_card,
    render_labeling_metric_cards,
    render_manual_validation_table,
    render_project_flow_horizontal,
    render_sidebar,
)


st.set_page_config(page_title="Dashboard Sentimen JakOne Mobile", layout="wide")


DATASET_PATH = "data/final/06_jakone_modeling_master_v3.csv"
LABELED_PATH = "data/processed/jakone_reviews_labeled_v3.csv"
VALIDATION_SAMPLE_PATH = "data/processed/lexicon_validation_sample.csv"
VALIDATION_V3_PATH = "outputs/audit/validasi_v1_vs_v3.csv"
TRAINING_LOG_PATH = "outputs/modeling/indobert_v3_baseline/training_log.json"
VALIDATION_METRICS_PATH = "outputs/modeling/indobert_v3_baseline/validation_metrics.json"
REPORT_PATH = "outputs/evaluation/indobert_v3_baseline/classification_report.csv"
CONFUSION_MATRIX_PATH = "outputs/evaluation/indobert_v3_baseline/confusion_matrix.csv"
METRICS_PATH = "outputs/evaluation/indobert_v3_baseline/test_metrics.json"
PREDICTIONS_PATH = "outputs/evaluation/indobert_v3_baseline/test_predictions.csv"
KEYWORD_SUMMARY_PATH = "outputs/analysis/indobert_v3_baseline/keyword_issue_summary_v3.csv"
KEYWORD_BY_LABEL_PATH = "outputs/analysis/indobert_v3_baseline/keyword_issue_by_label_v3.csv"
FINAL_SUMMARY_PATH = "outputs/evaluation/final_analysis_summary.txt"
MODEL_DIR = "models/indobert_v3_baseline"
LEXICON_POSITIVE_PATH = "data/lexicon/active/lexicon_v3_positive.tsv"
LEXICON_NEGATIVE_PATH = "data/lexicon/active/lexicon_v3_negative.tsv"
ASPECT_TERMS_PATH = "data/lexicon/active/kata_aspek_domain.txt"
WORDCLOUD_PATHS = {
    "Positif": "outputs/figures/indobert_v3_baseline/wordcloud_positif_v3.png",
    "Negatif": "outputs/figures/indobert_v3_baseline/wordcloud_negatif_v3.png",
    "Netral": "outputs/figures/indobert_v3_baseline/wordcloud_netral_v3.png",
}

LABEL_ORDER = ["negatif", "netral", "positif"]
LABEL_DISPLAY_ORDER = ["positif", "negatif", "netral"]
NAVIGATION = [
    "Overview",
    "Dataset",
    "Labeling",
    "Training IndoBERT",
    "Evaluasi Model",
    "Keyword Issue & Word Cloud",
    "Demo Prediksi",
]


def apply_css():
    st.markdown(
        """
        <style>
        :root {
            --navy: #071a35;
            --navy-soft: #123b6d;
            --blue: #2563eb;
            --cyan: #22d3ee;
            --ink: #0f172a;
            --muted: #64748b;
            --surface: #ffffff;
            --surface-soft: #f8fafc;
            --border: rgba(15, 39, 72, 0.12);
        }
        .main-title {
            padding: 1.25rem 1.5rem;
            border-radius: 10px;
            background: linear-gradient(135deg, #0f2748 0%, #173b68 100%);
            color: white;
            margin-bottom: 1.25rem;
        }
        .main-title h1 {
            margin: 0;
            font-size: 2rem;
            letter-spacing: 0;
        }
        .main-title p {
            margin: 0.4rem 0 0 0;
            opacity: 0.92;
        }
        .section-box {
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1rem 1.15rem;
            margin: 0.75rem 0 1.25rem 0;
            background: var(--surface);
        }
        .metric-card {
            border: 1px solid var(--border);
            border-left: 5px solid var(--navy-soft);
            border-radius: 10px;
            padding: 0.9rem 1rem;
            min-height: 100px;
        }
        .metric-label {
            font-size: 0.84rem;
            color: #6b7280;
            margin-bottom: 0.25rem;
        }
        .metric-value {
            font-size: 1.35rem;
            font-weight: 700;
            color: var(--navy);
        }
        .overview-hero {
            position: relative;
            overflow: hidden;
            padding: 2rem 2rem 1.75rem 2rem;
            border-radius: 18px;
            background:
                radial-gradient(circle at 92% 12%, rgba(34, 211, 238, 0.28) 0, rgba(34, 211, 238, 0) 28%),
                linear-gradient(135deg, #071a35 0%, #0d2e5f 48%, #155e94 100%);
            color: white;
            box-shadow: 0 22px 55px rgba(7, 26, 53, 0.24);
            margin-bottom: 1.35rem;
        }
        .overview-hero h1 {
            max-width: 900px;
            margin: 0;
            font-size: clamp(1.85rem, 3.2vw, 3rem);
            line-height: 1.1;
            letter-spacing: 0;
        }
        .overview-hero p {
            max-width: 760px;
            margin: 0.85rem 0 0 0;
            color: rgba(255, 255, 255, 0.86);
            font-size: 1rem;
            line-height: 1.65;
        }
        .overview-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            margin-bottom: 0.85rem;
            padding: 0.35rem 0.7rem;
            border: 1px solid rgba(255, 255, 255, 0.22);
            border-radius: 999px;
            color: rgba(255, 255, 255, 0.88);
            background: rgba(255, 255, 255, 0.08);
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .overview-metric-card {
            min-height: 128px;
            padding: 1.05rem 1.05rem 1rem 1.05rem;
            border: 1px solid var(--border);
            border-radius: 14px;
            background:
                linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(248, 250, 252, 0.96));
            box-shadow: 0 14px 34px rgba(15, 23, 42, 0.08);
        }
        .overview-metric-icon {
            width: 34px;
            height: 34px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            margin-bottom: 0.75rem;
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.14), rgba(34, 211, 238, 0.22));
            color: var(--navy);
            font-size: 1.05rem;
        }
        .overview-metric-label {
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.28rem;
        }
        .overview-metric-value {
            color: var(--ink);
            font-size: 1.65rem;
            line-height: 1.15;
            font-weight: 800;
        }
        .overview-metric-note {
            color: var(--muted);
            font-size: 0.84rem;
            margin-top: 0.45rem;
        }
        .insight-card {
            height: 100%;
            padding: 1.1rem 1.15rem;
            border: 1px solid var(--border);
            border-radius: 14px;
            background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
        }
        .insight-card h3 {
            margin: 0 0 0.55rem 0;
            color: var(--navy);
            font-size: 1.05rem;
            letter-spacing: 0;
        }
        .insight-card p {
            margin: 0;
            color: #334155;
            line-height: 1.58;
            font-size: 0.95rem;
        }
        .overview-section-title {
            margin: 1.45rem 0 0.65rem 0;
            color: var(--ink);
            font-size: 1.22rem;
            font-weight: 800;
            letter-spacing: 0;
        }
        .small-note {
            color: #6b7280;
            font-size: 0.9rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def warn_missing(path):
    st.warning(f"File belum tersedia: {path}")


def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def overview_metric_card(label, value, note, icon):
    st.markdown(
        f"""
        <div class="overview-metric-card">
            <div class="overview-metric-icon">{icon}</div>
            <div class="overview-metric-label">{label}</div>
            <div class="overview-metric-value">{value}</div>
            <div class="overview-metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_card(title, body):
    st.markdown(
        f"""
        <div class="insight-card">
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(title, subtitle=None):
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="main-title">
            <h1>{title}</h1>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def load_dataset():
    df = load_csv(DATASET_PATH)
    if df is None:
        warn_missing(DATASET_PATH)
    return df


def load_metrics():
    metrics = load_json(METRICS_PATH)
    if metrics is None:
        warn_missing(METRICS_PATH)
    return metrics


def normalize_dashboard_labels(df):
    if df is None:
        return None
    df = df.copy()
    if "label" not in df.columns and "label_v3" in df.columns:
        df["label"] = df["label_v3"]
    if "lexicon_score" not in df.columns and "lexicon_score_v3" in df.columns:
        df["lexicon_score"] = df["lexicon_score_v3"]
    return df


def load_labeled_dataset():
    df = load_csv(LABELED_PATH)
    if df is None:
        warn_missing(LABELED_PATH)
    return normalize_dashboard_labels(df)


def load_training_log():
    log_rows = load_json(TRAINING_LOG_PATH)
    if log_rows is None:
        warn_missing(TRAINING_LOG_PATH)
        return None
    if isinstance(log_rows, dict):
        log_rows = log_rows.get("log_history", log_rows.get("trainer_state", log_rows))
    training_log = pd.DataFrame(log_rows)
    if training_log.empty:
        return training_log
    alias_map = {
        "loss": "train_loss",
        "eval_loss": "val_loss",
        "eval_accuracy": "val_accuracy",
        "eval_macro_f1": "val_f1_macro",
    }
    for source, alias in alias_map.items():
        if alias not in training_log.columns and source in training_log.columns:
            training_log[alias] = training_log[source]
    return training_log


def safe_numeric_series(df, candidate_columns):
    if df is None or df.empty:
        return pd.Series(dtype=float)
    for col in candidate_columns:
        if col in df.columns:
            series_or_df = df[col]
            if isinstance(series_or_df, pd.DataFrame):
                series_or_df = series_or_df.iloc[:, 0]
            series = pd.to_numeric(series_or_df, errors="coerce").dropna()
            if not series.empty:
                return series
    return pd.Series(dtype=float)


def safe_last_numeric(df, candidate_columns):
    series = safe_numeric_series(df, candidate_columns)
    if series.empty:
        return None
    return float(series.iloc[-1])


def safe_best_numeric(df, candidate_columns):
    series = safe_numeric_series(df, candidate_columns)
    if series.empty:
        return None
    return float(series.max())


def get_best_training_values(training_log):
    if training_log is None or training_log.empty:
        return None
    values = {}
    f1_series = safe_numeric_series(training_log, ["val_f1_macro", "eval_macro_f1"])
    if not f1_series.empty:
        best_idx = f1_series.idxmax()
        values["best_val_f1_macro"] = float(f1_series.loc[best_idx])
        epoch_series = safe_numeric_series(training_log.loc[[best_idx]], ["epoch"])
        if not epoch_series.empty:
            values["best_epoch"] = float(epoch_series.iloc[-1])

    metric_candidates = {
        "last_train_loss": ["train_loss", "loss"],
        "last_val_loss": ["val_loss", "eval_loss"],
        "best_eval_accuracy": ["eval_accuracy", "val_accuracy"],
        "best_eval_macro_f1": ["eval_macro_f1", "val_f1_macro"],
        "best_eval_weighted_f1": ["eval_weighted_f1"],
        "last_epoch": ["epoch"],
    }
    for key, columns in metric_candidates.items():
        value = safe_last_numeric(training_log, columns)
        if value is not None:
            values[key] = value

    for key, columns in {
        "best_eval_accuracy": ["eval_accuracy", "val_accuracy"],
        "best_eval_macro_f1": ["eval_macro_f1", "val_f1_macro"],
        "best_eval_weighted_f1": ["eval_weighted_f1"],
    }.items():
        value = safe_best_numeric(training_log, columns)
        if value is not None:
            values[key] = value
    return values


def format_decimal(value, digits=6):
    if value is None:
        return "N/A"
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return "N/A"


def numeric_column(df, column):
    if df is None or column not in df.columns:
        return pd.Series(index=df.index if df is not None else None, dtype=float)
    series_or_df = df[column]
    if isinstance(series_or_df, pd.DataFrame):
        series_or_df = series_or_df.iloc[:, 0]
    return pd.to_numeric(series_or_df, errors="coerce")


def build_training_curve_logs(training_log):
    if training_log is None or training_log.empty:
        empty = pd.DataFrame()
        return empty, empty

    train_log = pd.DataFrame(
        {
            "step": numeric_column(training_log, "step"),
            "epoch": numeric_column(training_log, "epoch"),
            "loss": numeric_column(training_log, "loss"),
        }
    )
    train_log = train_log.dropna(subset=["step", "loss"]).sort_values("step")
    train_log = train_log.drop_duplicates(subset=["step"], keep="last")

    eval_log = pd.DataFrame(
        {
            "step": numeric_column(training_log, "step"),
            "epoch": numeric_column(training_log, "epoch"),
            "eval_loss": numeric_column(training_log, "eval_loss"),
            "eval_accuracy": numeric_column(training_log, "eval_accuracy"),
            "eval_macro_f1": numeric_column(training_log, "eval_macro_f1"),
        }
    )
    metric_columns = ["eval_loss", "eval_accuracy", "eval_macro_f1"]
    eval_log = eval_log.dropna(subset=metric_columns, how="all")
    if "epoch" in eval_log.columns and eval_log["epoch"].notna().any():
        eval_log = eval_log.sort_values(["epoch", "step"], na_position="last")
        eval_log = eval_log.drop_duplicates(subset=["epoch"], keep="last")
    elif "step" in eval_log.columns and eval_log["step"].notna().any():
        eval_log = eval_log.sort_values("step")
        eval_log = eval_log.drop_duplicates(subset=["step"], keep="last")
    return train_log, eval_log


def format_number(value):
    if value is None:
        return "-"
    try:
        return f"{int(value):,}".replace(",", ".")
    except (TypeError, ValueError):
        return str(value)


def clean_confusion_matrix(cm_df):
    cm = cm_df.copy()
    cm.index = [str(item).replace("actual_", "") for item in cm.index]
    cm.columns = [str(item).replace("predicted_", "") for item in cm.columns]
    return cm.reindex(index=LABEL_ORDER, columns=LABEL_ORDER).fillna(0).astype(int)


def plot_bar(df, x, y, title, color=None):
    fig = px.bar(df, x=x, y=y, title=title, text=y, color=color)
    fig.update_layout(
        title_font_color="#0f2748",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=55, b=30),
    )
    fig.update_traces(textposition="outside")
    return fig


def plot_donut(df, names, values, title, color_map=None):
    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title,
        hole=0.58,
        color=names,
        color_discrete_map=color_map,
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(line=dict(color="#ffffff", width=3)),
    )
    fig.update_layout(
        title_font_color="#0f2748",
        title_font_size=18,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=16, r=16, t=56, b=18),
        legend_title_text="",
        legend=dict(orientation="h", y=-0.05, x=0.5, xanchor="center"),
    )
    return fig


def render_overview():
    df = load_dataset()
    metrics = load_metrics()
    training_log = load_training_log()
    summary_text = load_text(FINAL_SUMMARY_PATH)

    total_data = len(df) if df is not None else None
    training_values = get_best_training_values(training_log)

    st.markdown(
        """
        <div class="overview-hero">
            <div class="overview-eyebrow">Dashboard Skripsi</div>
            <h1>Analisis Sentimen JakOne Mobile Menggunakan IndoBERT</h1>
            <p>
                Ringkasan penelitian untuk membaca pola sentimen pengguna, performa model,
                dan isu utama aplikasi JakOne Mobile secara cepat dan mudah.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        overview_metric_card("Total Data", format_number(total_data), "Ulasan dalam dataset final", "DB")
    with col2:
        overview_metric_card(
            "Accuracy Test",
            format_percent(metrics.get("accuracy") if metrics else None),
            "Akurasi pada data test",
            "%",
        )
    with col3:
        overview_metric_card(
            "Macro F1 Test",
            format_percent(metrics.get("macro_f1") if metrics else None),
            "Rata-rata F1 seluruh kelas",
            "F1",
        )
    with col4:
        best_f1 = training_values.get("best_val_f1_macro") if training_values else None
        overview_metric_card("Best Validation F1", format_percent(best_f1), "Model terbaik saat training", "VAL")

    st.markdown('<div class="overview-section-title">Insight Utama</div>', unsafe_allow_html=True)
    insight_cols = st.columns(3)
    with insight_cols[0]:
        insight_card(
            "Performa Model",
            "IndoBERT menunjukkan performa baik pada kelas positif dan negatif sehingga cukup kuat untuk membaca kecenderungan sentimen utama.",
        )
    with insight_cols[1]:
        insight_card(
            "Tantangan Kelas Netral",
            "Kelas netral masih menjadi area paling menantang karena jumlah data lebih sedikit dan ekspresi ulasan cenderung lebih ambigu.",
        )
    with insight_cols[2]:
        insight_card(
            "Fokus Analisis",
            "Dashboard menekankan evaluasi model, pola kesalahan, keyword issue, dan demo prediksi agar hasil penelitian mudah dipresentasikan.",
        )

    render_project_flow_horizontal()

    st.markdown('<div class="overview-section-title">Distribusi Ringkas</div>', unsafe_allow_html=True)
    chart_col1, chart_col2 = st.columns(2)
    if df is not None and "label" in df.columns:
        label_df = df["label"].value_counts().reindex(LABEL_DISPLAY_ORDER, fill_value=0).reset_index()
        label_df.columns = ["label", "count"]
        chart_col1.plotly_chart(
            plot_donut(
                label_df,
                "label",
                "count",
                "Distribusi Label Sentimen",
                {
                    "positif": "#16a34a",
                    "negatif": "#dc2626",
                    "netral": "#64748b",
                },
            ),
            use_container_width=True,
        )
    if df is not None and "split_set" in df.columns:
        split_df = df["split_set"].value_counts().reindex(["train", "val", "test"], fill_value=0).reset_index()
        split_df.columns = ["split_set", "count"]
        chart_col2.plotly_chart(
            plot_donut(
                split_df,
                "split_set",
                "count",
                "Distribusi Split Dataset",
                {
                    "train": "#2563eb",
                    "val": "#0f766e",
                    "test": "#f59e0b",
                },
            ),
            use_container_width=True,
        )

    if summary_text:
        with st.expander("Lihat ringkasan analisis akhir lengkap"):
            st.text(summary_text)
    else:
        warn_missing(FINAL_SUMMARY_PATH)


def render_dataset():
    df = load_dataset()
    if df is None:
        return

    render_dataset_hero()
    render_dataset_metric_cards(df)
    render_dataset_insights()
    filtered = render_dataset_filter_panel(df)
    render_dataset_preview(filtered, len(df))
    render_dataset_visualization_tabs(df)
    render_dataset_quality_cards(df)
    render_dataset_note()


def render_labeling():
    labeled_df = load_labeled_dataset()
    sample_df = load_csv(VALIDATION_SAMPLE_PATH)
    source_df = labeled_df if labeled_df is not None else load_dataset()

    render_labeling_hero()
    render_labeling_method_card()

    if source_df is None or "label" not in source_df.columns:
        warn_missing(LABELED_PATH)
    else:
        render_labeling_metric_cards(source_df, sample_df)
        render_labeling_flow_vertical()
        render_labeling_distribution_chart(source_df)
        render_labeling_examples(source_df)

    render_manual_validation_table(sample_df)
    if sample_df is None:
        warn_missing(VALIDATION_SAMPLE_PATH)
    elif not {"manual_label", "notes"}.issubset(sample_df.columns):
        st.info("Kolom manual_label dan notes tidak ditemukan pada file sampel validasi.")
    render_labeling_limitation_note()


def render_training():
    page_header("Training IndoBERT", "Ringkasan fine-tuning model IndoBERT.")
    training_log = load_training_log()
    validation_metrics = load_json(VALIDATION_METRICS_PATH)
    if training_log is None:
        return

    values = get_best_training_values(training_log) or {}
    cols = st.columns(5)
    items = [
        ("Model", "IndoBERT"),
        ("Best Epoch", format_decimal(values.get("best_epoch"), digits=2)),
        ("Best Val F1 Macro", format_percent(values.get("best_val_f1_macro"))),
        ("Train Loss Terakhir", format_decimal(values.get("last_train_loss"))),
        ("Val Loss Terakhir", format_decimal(values.get("last_val_loss"))),
    ]
    for col, (label, value) in zip(cols, items):
        with col:
            metric_card(label, value)

    if validation_metrics:
        vcols = st.columns(3)
        with vcols[0]:
            metric_card("Validation Accuracy Final", format_percent(validation_metrics.get("eval_accuracy")))
        with vcols[1]:
            metric_card("Validation Macro F1 Final", format_percent(validation_metrics.get("eval_macro_f1")))
        with vcols[2]:
            metric_card("Validation Weighted F1 Final", format_percent(validation_metrics.get("eval_weighted_f1")))

    st.markdown("### Training Log")
    st.dataframe(training_log, use_container_width=True)

    st.markdown("### Kurva Training")
    train_log, eval_log = build_training_curve_logs(training_log)

    loss_col1, loss_col2 = st.columns(2)
    with loss_col1:
        if train_log.empty:
            st.warning("Training loss tidak tersedia pada training_log.json.")
        else:
            train_loss_fig = px.line(
                train_log,
                x="step",
                y="loss",
                markers=True,
                title="Training Loss per Step",
                labels={"step": "Step", "loss": "Training Loss"},
            )
            st.plotly_chart(train_loss_fig, use_container_width=True)

    with loss_col2:
        validation_loss = eval_log.dropna(subset=["eval_loss"]) if not eval_log.empty else pd.DataFrame()
        if validation_loss.empty:
            st.warning("Validation loss tidak tersedia pada training_log.json.")
        else:
            val_loss_fig = px.line(
                validation_loss,
                x="epoch",
                y="eval_loss",
                markers=True,
                title="Validation Loss per Epoch",
                labels={"epoch": "Epoch", "eval_loss": "Validation Loss"},
            )
            st.plotly_chart(val_loss_fig, use_container_width=True)

    metric_col1, metric_col2 = st.columns(2)
    with metric_col1:
        validation_accuracy = eval_log.dropna(subset=["eval_accuracy"]) if not eval_log.empty else pd.DataFrame()
        if validation_accuracy.empty:
            st.warning("Validation accuracy tidak tersedia pada training_log.json.")
        else:
            acc_fig = px.line(
                validation_accuracy,
                x="epoch",
                y="eval_accuracy",
                markers=True,
                title="Validation Accuracy per Epoch",
                labels={"epoch": "Epoch", "eval_accuracy": "Validation Accuracy"},
            )
            acc_fig.update_yaxes(range=[0, 1])
            st.plotly_chart(acc_fig, use_container_width=True)

    with metric_col2:
        validation_f1 = eval_log.dropna(subset=["eval_macro_f1"]) if not eval_log.empty else pd.DataFrame()
        if validation_f1.empty:
            st.warning("Validation macro F1 tidak tersedia pada training_log.json.")
        else:
            f1_fig = px.line(
                validation_f1,
                x="epoch",
                y="eval_macro_f1",
                markers=True,
                title="Validation Macro F1 per Epoch",
                labels={"epoch": "Epoch", "eval_macro_f1": "Validation Macro F1"},
            )
            f1_fig.update_yaxes(range=[0, 1])
            st.plotly_chart(f1_fig, use_container_width=True)

    if not eval_log.empty and len(eval_log) <= 2:
        st.caption("Catatan: validation metrics hanya memiliki sedikit titik karena baseline dilatih selama 2 epoch.")

    st.info("Dashboard menggunakan hasil IndoBERT v3 baseline. Baseline pertama menggunakan USE_CLASS_WEIGHT = False.")


def render_evaluation():
    page_header("Evaluasi Model", "Hasil evaluasi model IndoBERT pada data test.")
    metrics = load_metrics()
    report_df = load_csv(REPORT_PATH)
    cm_raw = load_csv(CONFUSION_MATRIX_PATH)

    if metrics is None:
        metrics = {}
    cols = st.columns(4)
    metric_items = [
        ("Accuracy", format_percent(metrics.get("accuracy"))),
        ("Macro F1", format_percent(metrics.get("macro_f1"))),
        ("Weighted F1", format_percent(metrics.get("weighted_f1"))),
        ("Data Test", format_number(metrics.get("test_count"))),
    ]
    for col, (label, value) in zip(cols, metric_items):
        with col:
            metric_card(label, value)

    if report_df is None:
        warn_missing(REPORT_PATH)
    else:
        st.markdown("### Classification Report")
        st.dataframe(report_df, use_container_width=True)

        class_df = report_df.rename(columns={report_df.columns[0]: "label"}) if report_df.columns[0] != "label" else report_df.copy()
        if "Unnamed: 0" in class_df.columns:
            class_df = class_df.rename(columns={"Unnamed: 0": "label"})
        class_df = class_df[class_df["label"].isin(LABEL_ORDER)] if "label" in class_df.columns else class_df.loc[LABEL_ORDER].reset_index(names="label")
        metric_cols = [col for col in ["precision", "recall", "f1-score"] if col in class_df.columns]
        if metric_cols:
            melted = class_df.melt(id_vars="label", value_vars=metric_cols, var_name="metric", value_name="score")
            fig = px.bar(melted, x="label", y="score", color="metric", barmode="group", title="Precision, Recall, dan F1-score per Kelas")
            fig.update_yaxes(range=[0, 1])
            st.plotly_chart(fig, use_container_width=True)

    if cm_raw is None:
        warn_missing(CONFUSION_MATRIX_PATH)
    else:
        if "Unnamed: 0" in cm_raw.columns:
            cm_raw = cm_raw.set_index("Unnamed: 0")
        cm = clean_confusion_matrix(cm_raw)
        st.markdown("### Confusion Matrix")
        st.dataframe(cm, use_container_width=True)
        heatmap = px.imshow(
            cm,
            text_auto=True,
            color_continuous_scale="Blues",
            title="Heatmap Confusion Matrix",
            labels=dict(x="Predicted", y="Actual", color="Count"),
        )
        st.plotly_chart(heatmap, use_container_width=True)

    st.success("Highlight: kelas terbaik adalah positif, sedangkan kelas terlemah adalah netral.")


def render_keyword_issue():
    page_header("Keyword Issue & Word Cloud", "Analisis isu dominan berdasarkan keyword dan visualisasi word cloud.")
    tab_keyword, tab_wordcloud = st.tabs(["Keyword Issue", "Word Cloud"])

    with tab_keyword:
        keyword_summary = load_csv(KEYWORD_SUMMARY_PATH)
        keyword_by_label = load_csv(KEYWORD_BY_LABEL_PATH)
        if keyword_summary is None:
            warn_missing(KEYWORD_SUMMARY_PATH)
        else:
            count_column = "total_count" if "total_count" in keyword_summary.columns else "count"
            top_keyword = keyword_summary.sort_values(count_column, ascending=False).iloc[0]
            neg_keyword = None
            if keyword_by_label is not None and not keyword_by_label.empty:
                neg_df = keyword_by_label[keyword_by_label["label"] == "negatif"].sort_values("count", ascending=False)
                if not neg_df.empty:
                    neg_keyword = neg_df.iloc[0]

            c1, c2 = st.columns(2)
            with c1:
                metric_card("Keyword Paling Dominan", f"{top_keyword['keyword']} ({int(top_keyword[count_column])})")
            with c2:
                value = f"{neg_keyword['keyword']} ({int(neg_keyword['count'])})" if neg_keyword is not None else "-"
                metric_card("Keyword Negatif Dominan", value)

            top_df = keyword_summary.sort_values(count_column, ascending=False).head(10)
            st.plotly_chart(plot_bar(top_df, "keyword", count_column, "Top Keyword Keseluruhan"), use_container_width=True)

            if keyword_by_label is None:
                warn_missing(KEYWORD_BY_LABEL_PATH)
            else:
                neg_top = keyword_by_label[keyword_by_label["label"] == "negatif"].sort_values("count", ascending=False).head(10)
                st.plotly_chart(plot_bar(neg_top, "keyword", "count", "Top Keyword pada Sentimen Negatif"), use_container_width=True)
                label_fig = px.bar(
                    keyword_by_label.sort_values("count", ascending=False),
                    x="keyword",
                    y="count",
                    color="label",
                    barmode="group",
                    title="Keyword Issue Berdasarkan Label",
                )
                st.plotly_chart(label_fig, use_container_width=True)

    with tab_wordcloud:
        cols = st.columns(3)
        for col, (label, path) in zip(cols, WORDCLOUD_PATHS.items()):
            with col:
                st.subheader(label)
                if file_exists(path):
                    st.image(path, use_container_width=True)
                else:
                    warn_missing(path)


def render_prediction_demo():
    page_header("Demo Prediksi", "Prediksi sentimen ulasan baru menggunakan model IndoBERT hasil fine-tuning.")
    st.markdown(
        """
        <style>
        .prediction-confidence-card {
            padding: 1rem 1.1rem;
            border-radius: 14px;
            border: 1px solid var(--confidence-border);
            border-left: 5px solid var(--confidence-accent);
            background: var(--confidence-bg);
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
            margin: 0.65rem 0 0.85rem 0;
        }
        .prediction-confidence-status {
            color: var(--confidence-accent);
            font-size: 1.02rem;
            font-weight: 850;
            margin-bottom: 0.25rem;
        }
        .prediction-confidence-message {
            color: #334155;
            font-size: 0.92rem;
            line-height: 1.5;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    text = st.text_area(
        "Masukkan ulasan pengguna JakOne Mobile",
        value="otp tidak masuk dan tidak bisa login",
        height=140,
    )
    st.caption("Prediksi dilakukan menggunakan model IndoBERT hasil fine-tuning pada dataset ulasan JakOne Mobile.")

    if st.button("Prediksi Sentimen", type="primary"):
        if not file_exists(MODEL_DIR):
            warn_missing(MODEL_DIR)
            return
        try:
            with st.spinner("Memuat model dan memprediksi sentimen..."):
                model, tokenizer, label_mapping = load_model_and_tokenizer(MODEL_DIR)
                label, confidence, probabilities, details = predict_sentiment(
                    text,
                    model,
                    tokenizer,
                    label_mapping,
                    max_length=128,
                    return_details=True,
                )
            confidence_status = get_confidence_status(confidence)
            c1, c2 = st.columns(2)
            with c1:
                metric_card("Prediksi sementara" if confidence_status["is_uncertain"] else "Prediksi", label)
            with c2:
                metric_card("Confidence", format_percent(confidence))

            confidence_style = {
                "warning": ("#fff7ed", "rgba(249, 115, 22, 0.26)", "#f97316"),
                "info": ("#eff6ff", "rgba(37, 99, 235, 0.22)", "#2563eb"),
                "success": ("#f0fdf4", "rgba(22, 163, 74, 0.24)", "#16a34a"),
            }[confidence_status["message_type"]]
            st.markdown(
                f"""
                <div class="prediction-confidence-card"
                     style="--confidence-bg:{confidence_style[0]}; --confidence-border:{confidence_style[1]}; --confidence-accent:{confidence_style[2]};">
                    <div class="prediction-confidence-status">{confidence_status["status"]}</div>
                    <div class="prediction-confidence-message">{confidence_status["message"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if confidence_status["message_type"] == "warning":
                st.warning(confidence_status["message"])
            elif confidence_status["message_type"] == "info":
                st.info(confidence_status["message"])
            else:
                st.success(confidence_status["message"])

            detected_keywords = details.get("detected_security_keywords", [])
            if detected_keywords:
                st.info(f"Keyword keamanan terdeteksi: {', '.join(detected_keywords)}")
            sentiment_signal = details.get("sentiment_signal", {})
            signal_label = sentiment_signal.get("signal")
            signal_matches = sentiment_signal.get("matches", [])
            if signal_label and signal_label != "campuran":
                st.info(
                    f"Sinyal {signal_label} terdeteksi dari teks input: {', '.join(signal_matches)}."
                )
                if str(label).lower() != signal_label:
                    st.warning(
                        "Terdapat perbedaan antara prediksi model dan sinyal sentimen berbasis kata kunci. "
                        "Hasil sebaiknya ditinjau ulang."
                    )
            elif signal_label == "campuran":
                st.info(
                    f"Sinyal sentimen campuran terdeteksi dari teks input: {', '.join(signal_matches)}."
                )
            st.caption("Catatan: prediksi kelas netral dapat lebih sulit karena jumlah data netral lebih sedikit dibanding kelas positif dan negatif.")
            st.caption("Prediksi dengan confidence rendah sebaiknya tidak dijadikan keputusan final karena model belum cukup yakin terhadap kelas sentimen.")

            prob_df = pd.DataFrame(
                {"label": list(probabilities.keys()), "probability": list(probabilities.values())}
            )
            prob_df["label"] = pd.Categorical(prob_df["label"], categories=LABEL_ORDER, ordered=True)
            prob_df = prob_df.sort_values("label")
            fig = px.bar(
                prob_df,
                x="label",
                y="probability",
                title="Probabilitas Setiap Kelas",
                text="probability",
                color="label",
                color_discrete_map={
                    "negatif": "#f97316",
                    "netral": "#93c5fd",
                    "positif": "#16a34a",
                },
            )
            fig.update_yaxes(range=[0, 1])
            fig.update_traces(texttemplate="%{text:.2%}", textposition="outside")
            fig.update_layout(
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=55, b=30),
                yaxis_title="Probabilitas",
                xaxis_title="Label",
            )
            st.plotly_chart(fig, use_container_width=True)

            with st.expander("Detail proses prediksi"):
                st.markdown("**Teks asli input user**")
                st.write(details.get("original_text", ""))
                st.markdown("**Teks setelah preprocessing**")
                st.write(details.get("processed_text", ""))
                st.markdown("**Max length tokenisasi**")
                st.write(details.get("max_length", 128))
                st.markdown("**Label mapping yang digunakan**")
                st.json(details.get("label_mapping", {}))
                st.markdown("**Probabilitas setiap kelas**")
                debug_prob_df = prob_df.copy()
                debug_prob_df["probability"] = debug_prob_df["probability"].map(lambda value: f"{value:.4f}")
                st.dataframe(debug_prob_df, use_container_width=True, hide_index=True)
                st.markdown("**Sinyal sentimen berbasis kata kunci**")
                st.json(sentiment_signal)
        except Exception as exc:
            st.error(f"Prediksi gagal: {exc}")


def main():
    apply_css()
    dataset = load_dataset()
    total_data = len(dataset) if dataset is not None else 0
    page = render_sidebar(NAVIGATION, format_number(total_data))

    if page == "Overview":
        render_overview()
    elif page == "Dataset":
        render_dataset()
    elif page == "Labeling":
        render_labeling()
    elif page == "Training IndoBERT":
        render_training()
    elif page == "Evaluasi Model":
        render_evaluation()
    elif page == "Keyword Issue & Word Cloud":
        render_keyword_issue()
    elif page == "Demo Prediksi":
        render_prediction_demo()


if __name__ == "__main__":
    main()
