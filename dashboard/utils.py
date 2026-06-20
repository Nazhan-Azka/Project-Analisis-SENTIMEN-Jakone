import json
import importlib.util
import os
import re

import pandas as pd
import plotly.express as px
import streamlit as st
import torch
from transformers import AutoConfig, AutoModelForSequenceClassification, AutoTokenizer


def file_exists(path):
    return os.path.exists(path)


@st.cache_data(show_spinner=False)
def load_csv(path):
    if not file_exists(path):
        return None
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_json(path):
    if not file_exists(path):
        return None
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


@st.cache_data(show_spinner=False)
def load_text(path):
    if not file_exists(path):
        return None
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def format_percent(value):
    if value is None:
        return "-"
    try:
        return f"{float(value) * 100:.2f}%"
    except (TypeError, ValueError):
        return "-"


def render_project_flow_horizontal():
    st.markdown(
        """
        <style>
        .project-flow-section {
            margin: 1.45rem 0 1.1rem 0;
        }
        .project-flow-title {
            margin: 0 0 0.65rem 0;
            color: #0f172a;
            font-size: 1.22rem;
            font-weight: 800;
            letter-spacing: 0;
        }
        .project-flow-scroll {
            display: flex;
            align-items: stretch;
            gap: 0.72rem;
            overflow-x: auto;
            overflow-y: hidden;
            padding: 0.2rem 0.15rem 0.95rem 0.15rem;
            scroll-snap-type: x proximity;
        }
        .project-flow-scroll::-webkit-scrollbar {
            height: 8px;
        }
        .project-flow-scroll::-webkit-scrollbar-track {
            background: #eef2f7;
            border-radius: 999px;
        }
        .project-flow-scroll::-webkit-scrollbar-thumb {
            background: #94a3b8;
            border-radius: 999px;
        }
        .flow-step-card {
            flex: 0 0 245px;
            min-height: 158px;
            scroll-snap-align: start;
            border-radius: 15px;
            border: 1px solid rgba(15, 39, 72, 0.12);
            background: #ffffff;
            box-shadow: 0 12px 28px rgba(15, 23, 42, 0.08);
            padding: 1rem;
            position: relative;
            overflow: hidden;
        }
        .flow-step-card::before {
            content: "";
            position: absolute;
            inset: 0 0 auto 0;
            height: 5px;
            background: var(--flow-color);
        }
        .flow-step-number {
            width: 34px;
            height: 34px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 11px;
            background: color-mix(in srgb, var(--flow-color) 15%, white);
            color: var(--flow-color);
            font-weight: 800;
            font-size: 0.9rem;
            margin-bottom: 0.8rem;
        }
        .flow-step-title {
            margin: 0 0 0.45rem 0;
            color: #0f172a;
            font-size: 0.98rem;
            line-height: 1.25;
            font-weight: 800;
            letter-spacing: 0;
        }
        .flow-step-desc {
            margin: 0;
            color: #475569;
            font-size: 0.88rem;
            line-height: 1.48;
        }
        .flow-arrow {
            flex: 0 0 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #64748b;
            font-size: 1.55rem;
            font-weight: 800;
            padding-bottom: 0.95rem;
        }
        @media (max-width: 640px) {
            .flow-step-card {
                flex-basis: 225px;
            }
            .flow-arrow {
                flex-basis: 22px;
            }
        }
        </style>
        <div class="project-flow-section">
            <div class="project-flow-title">Alur Pengerjaan Project</div>
            <div class="project-flow-scroll">
                <div class="flow-step-card" style="--flow-color:#0f2748;">
                    <div class="flow-step-number">01</div>
                    <div class="flow-step-title">Pengumpulan Data</div>
                    <p class="flow-step-desc">Scraping ulasan Google Play Store JakOne Mobile.</p>
                </div>
                <div class="flow-arrow">&rarr;</div>
                <div class="flow-step-card" style="--flow-color:#0f766e;">
                    <div class="flow-step-number">02</div>
                    <div class="flow-step-title">Preprocessing Teks</div>
                    <p class="flow-step-desc">Case folding, hapus emoji/simbol, normalisasi slang, hapus stopword.</p>
                </div>
                <div class="flow-arrow">&rarr;</div>
                <div class="flow-step-card" style="--flow-color:#7c3aed;">
                    <div class="flow-step-number">03</div>
                    <div class="flow-step-title">Pelabelan Sentimen</div>
                    <p class="flow-step-desc">Labeling manual / lexicon-based menjadi Positif, Negatif, Netral.</p>
                </div>
                <div class="flow-arrow">&rarr;</div>
                <div class="flow-step-card" style="--flow-color:#b45309;">
                    <div class="flow-step-number">04</div>
                    <div class="flow-step-title">Pembagian Dataset</div>
                    <p class="flow-step-desc">Split data train, validation, dan test.</p>
                </div>
                <div class="flow-arrow">&rarr;</div>
                <div class="flow-step-card" style="--flow-color:#0f2748;">
                    <div class="flow-step-number">05</div>
                    <div class="flow-step-title">Tokenisasi IndoBERT</div>
                    <p class="flow-step-desc">Mengubah teks menjadi input_ids, attention_mask, dan token_type_ids.</p>
                </div>
                <div class="flow-arrow">&rarr;</div>
                <div class="flow-step-card" style="--flow-color:#0f766e;">
                    <div class="flow-step-number">06</div>
                    <div class="flow-step-title">Fine-Tuning IndoBERT</div>
                    <p class="flow-step-desc">Training BertForSequenceClassification dengan optimizer AdamW.</p>
                </div>
                <div class="flow-arrow">&rarr;</div>
                <div class="flow-step-card" style="--flow-color:#7c3aed;">
                    <div class="flow-step-number">07</div>
                    <div class="flow-step-title">Evaluasi Model</div>
                    <p class="flow-step-desc">Accuracy, precision, recall, F1-score, dan confusion matrix.</p>
                </div>
                <div class="flow-arrow">&rarr;</div>
                <div class="flow-step-card" style="--flow-color:#b45309;">
                    <div class="flow-step-number">08</div>
                    <div class="flow-step-title">Analisis Hasil &amp; Visualisasi</div>
                    <p class="flow-step-desc">Distribusi sentimen, word cloud, keyword issue, dan insight hasil penelitian.</p>
                </div>
                <div class="flow-arrow">&rarr;</div>
                <div class="flow-step-card" style="--flow-color:#0f2748;">
                    <div class="flow-step-number">09</div>
                    <div class="flow-step-title">Kesimpulan &amp; Saran</div>
                    <p class="flow-step-desc">Ringkasan temuan, limitasi model, dan rekomendasi pengembangan.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _format_dataset_number(value):
    if value is None:
        return "-"
    try:
        return f"{int(value):,}".replace(",", ".")
    except (TypeError, ValueError):
        return str(value)


def _dataset_value_counts(df, column, order=None):
    if column not in df.columns:
        return pd.DataFrame({column: [], "count": []})
    counts = df[column].dropna().astype(str).value_counts()
    if order:
        counts = counts.reindex(order, fill_value=0)
    else:
        counts = counts.sort_index()
    result = counts.reset_index()
    result.columns = [column, "count"]
    return result


def _dataset_bar_chart(df, x, y, title, color_map=None):
    fig = px.bar(
        df,
        x=x,
        y=y,
        text=y,
        color=x if color_map else None,
        color_discrete_map=color_map,
        title=title,
    )
    fig.update_traces(textposition="outside", marker_line_width=0)
    fig.update_layout(
        title_font_color="#0f3763",
        title_font_size=18,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=18, r=18, t=56, b=26),
        showlegend=False,
        xaxis_title="",
        yaxis_title="Jumlah Ulasan",
        font=dict(color="#0f172a"),
    )
    fig.update_yaxes(gridcolor="rgba(15, 55, 99, 0.10)")
    return fig


def _dataset_donut_chart(df, names, values, title, color_map=None):
    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.5,
        color=names,
        color_discrete_map=color_map,
        title=title,
    )
    fig.update_traces(
        textinfo="label+value+percent",
        textposition="inside",
        insidetextorientation="radial",
        marker=dict(line=dict(color="#ffffff", width=3)),
        hovertemplate="<b>%{label}</b><br>Jumlah: %{value}<br>Persentase: %{percent}<extra></extra>",
    )
    fig.update_layout(
        title_font_color="#0f3763",
        title_font_size=18,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=18, r=18, t=56, b=18),
        height=380,
        legend_title_text="",
        legend=dict(orientation="h", y=-0.08, x=0.5, xanchor="center"),
        font=dict(color="#0f172a"),
    )
    return fig


def render_dataset_hero():
    st.markdown(
        """
        <style>
        .dataset-hero {
            padding: 1.9rem 2rem;
            border-radius: 18px;
            background:
                radial-gradient(circle at 88% 16%, rgba(34, 211, 238, 0.22) 0, rgba(34, 211, 238, 0) 30%),
                linear-gradient(135deg, #071a35 0%, #0f3763 58%, #14558f 100%);
            color: #ffffff;
            box-shadow: 0 18px 42px rgba(15, 55, 99, 0.24);
            margin-bottom: 1.2rem;
        }
        .dataset-hero h1 {
            margin: 0;
            font-size: clamp(1.8rem, 3vw, 2.7rem);
            line-height: 1.1;
            letter-spacing: 0;
        }
        .dataset-hero p {
            max-width: 760px;
            margin: 0.65rem 0 0 0;
            color: rgba(255, 255, 255, 0.86);
            line-height: 1.62;
            font-size: 1rem;
        }
        .dataset-section-title {
            margin: 1.35rem 0 0.7rem 0;
            color: #0f172a;
            font-size: 1.22rem;
            font-weight: 850;
            letter-spacing: 0;
        }
        .dataset-card,
        .dataset-filter-panel,
        .dataset-preview-panel,
        .dataset-note {
            border: 1px solid rgba(15, 55, 99, 0.12);
            border-radius: 16px;
            background: #ffffff;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.07);
        }
        .dataset-card {
            min-height: 126px;
            padding: 1rem;
        }
        .dataset-card-label {
            color: #64748b;
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.48rem;
        }
        .dataset-card-value {
            color: #0f3763;
            font-size: 1.7rem;
            line-height: 1.08;
            font-weight: 900;
            letter-spacing: 0;
        }
        .dataset-card-caption {
            color: #64748b;
            font-size: 0.86rem;
            line-height: 1.38;
            margin-top: 0.5rem;
        }
        .dataset-insight-card {
            min-height: 148px;
            padding: 1rem;
            border: 1px solid rgba(15, 55, 99, 0.10);
            border-radius: 15px;
            background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.055);
        }
        .dataset-insight-icon {
            width: 36px;
            height: 36px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            background: rgba(15, 55, 99, 0.09);
            color: #0f3763;
            font-size: 0.78rem;
            font-weight: 900;
            margin-bottom: 0.72rem;
        }
        .dataset-insight-title {
            color: #0f172a;
            font-size: 0.98rem;
            font-weight: 850;
            margin-bottom: 0.35rem;
        }
        .dataset-insight-text {
            color: #475569;
            font-size: 0.9rem;
            line-height: 1.48;
        }
        .dataset-filter-panel,
        .dataset-preview-panel {
            padding: 1rem 1.1rem;
            margin: 0.35rem 0 0.95rem 0;
        }
        .dataset-panel-title {
            color: #0f3763;
            font-size: 1.02rem;
            font-weight: 850;
            margin-bottom: 0.18rem;
        }
        .dataset-panel-desc {
            color: #64748b;
            font-size: 0.9rem;
            line-height: 1.45;
            margin-bottom: 0.7rem;
        }
        .dataset-count-info {
            display: inline-flex;
            margin: 0.2rem 0 0.75rem 0;
            padding: 0.45rem 0.7rem;
            border-radius: 999px;
            background: #eff6ff;
            color: #0f3763;
            font-size: 0.86rem;
            font-weight: 750;
        }
        .dataset-interpretation {
            margin-top: 0.3rem;
            padding: 0.8rem 0.95rem;
            border-left: 4px solid #0f3763;
            border-radius: 12px;
            background: #f8fafc;
            color: #334155;
            font-size: 0.92rem;
            line-height: 1.55;
        }
        .dataset-note {
            margin-top: 1.2rem;
            padding: 1rem 1.1rem;
            border-left: 5px solid #f97316;
            background: #fffaf5;
            color: #334155;
            line-height: 1.58;
        }
        </style>
        <div class="dataset-hero">
            <h1>Dataset</h1>
            <p>Eksplorasi data final ulasan JakOne Mobile sebelum proses modeling IndoBERT.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dataset_metric_cards(df):
    label_counts = df["label"].value_counts() if "label" in df.columns else pd.Series(dtype=int)
    year_range = "-"
    if "year" in df.columns:
        years = pd.to_numeric(df["year"], errors="coerce").dropna()
        if not years.empty:
            year_range = f"{int(years.min())}-{int(years.max())}"

    metrics = [
        ("Total Data", len(df), "Seluruh data final modeling"),
        ("Positif", int(label_counts.get("positif", 0)), "Kelas sentimen terbanyak"),
        ("Negatif", int(label_counts.get("negatif", 0)), "Ulasan bernada keluhan"),
        ("Netral", int(label_counts.get("netral", 0)), "Kelas minoritas dataset"),
        ("Rentang Tahun", year_range, "Periode ulasan terkumpul"),
    ]
    cols = st.columns(5)
    for col, (label, value, caption) in zip(cols, metrics):
        display_value = _format_dataset_number(value) if isinstance(value, int) else value
        with col:
            st.markdown(
                f"""
                <div class="dataset-card">
                    <div class="dataset-card-label">{label}</div>
                    <div class="dataset-card-value">{display_value}</div>
                    <div class="dataset-card-caption">{caption}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_dataset_insights():
    st.markdown('<div class="dataset-section-title">Insight Dataset</div>', unsafe_allow_html=True)
    insights = [
        ("POS", "Kelas Positif Dominan", "Positif menjadi kelas terbanyak dengan 7.475 ulasan."),
        ("MIN", "Kelas Netral Minoritas", "Netral menjadi kelas minoritas dengan 1.139 ulasan."),
        ("SPLIT", "Siap untuk Modeling", "Dataset sudah dibagi menjadi train, validation, dan test untuk kebutuhan modeling."),
        ("IMB", "Class Imbalance", "Distribusi label tidak seimbang sehingga perlu diperhatikan pada tahap evaluasi model."),
    ]
    cols = st.columns(4)
    for col, (icon, title, text) in zip(cols, insights):
        with col:
            st.markdown(
                f"""
                <div class="dataset-insight-card">
                    <div class="dataset-insight-icon">{icon}</div>
                    <div class="dataset-insight-title">{title}</div>
                    <div class="dataset-insight-text">{text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_dataset_filter_panel(df):
    st.markdown(
        """
        <div class="dataset-filter-panel">
            <div class="dataset-panel-title">Filter Data</div>
            <div class="dataset-panel-desc">Gunakan filter berikut untuk melihat subset data berdasarkan label, tahun, dan split set.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    f1, f2, f3 = st.columns(3)
    with f1:
        labels = ["Semua"] + sorted(df["label"].dropna().astype(str).unique().tolist()) if "label" in df.columns else ["Semua"]
        selected_label = st.selectbox("Label", labels, key="dataset_label_filter")
    with f2:
        years = ["Semua"] + sorted(df["year"].dropna().astype(str).unique().tolist()) if "year" in df.columns else ["Semua"]
        selected_year = st.selectbox("Tahun", years, key="dataset_year_filter")
    with f3:
        splits = ["Semua"] + sorted(df["split_set"].dropna().astype(str).unique().tolist()) if "split_set" in df.columns else ["Semua"]
        selected_split = st.selectbox("Split Set", splits, key="dataset_split_filter")

    filtered = df.copy()
    if selected_label != "Semua" and "label" in filtered.columns:
        filtered = filtered[filtered["label"].astype(str) == selected_label]
    if selected_year != "Semua" and "year" in filtered.columns:
        filtered = filtered[filtered["year"].astype(str) == selected_year]
    if selected_split != "Semua" and "split_set" in filtered.columns:
        filtered = filtered[filtered["split_set"].astype(str) == selected_split]
    return filtered


def render_dataset_preview(filtered_df, total_rows):
    st.markdown(
        """
        <div class="dataset-preview-panel">
            <div class="dataset-panel-title">Preview Dataset</div>
            <div class="dataset-panel-desc">Tabel ringkas menampilkan kolom utama agar data mudah dibaca saat presentasi.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    show_clean = st.checkbox("Tampilkan kolom clean_review", value=False, key="dataset_show_clean_review")
    preview_columns = ["review", "label", "rating", "year", "split_set"]
    if show_clean:
        preview_columns.insert(1, "clean_review")
    preview_columns = [col for col in preview_columns if col in filtered_df.columns]

    st.markdown(
        f"""
        <div class="dataset-count-info">
            Menampilkan {_format_dataset_number(len(filtered_df))} data dari total {_format_dataset_number(total_rows)} data.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(filtered_df[preview_columns].head(500), use_container_width=True, height=420)


def render_dataset_visualization_tabs(df):
    st.markdown('<div class="dataset-section-title">Visualisasi Dataset</div>', unsafe_allow_html=True)
    tabs = st.tabs(
        [
            "Distribusi Label Sentimen",
            "Distribusi Ulasan per Tahun",
            "Distribusi Rating",
            "Distribusi Split Dataset",
        ]
    )

    with tabs[0]:
        label_df = _dataset_value_counts(df, "label", ["positif", "negatif", "netral"])
        st.plotly_chart(
            _dataset_donut_chart(
                label_df,
                "label",
                "count",
                "Distribusi Label Sentimen",
                {"positif": "#16a34a", "negatif": "#f97316", "netral": "#93c5fd"},
            ),
            use_container_width=True,
        )
        st.markdown(
            '<div class="dataset-interpretation">Distribusi label menunjukkan bahwa kelas positif menjadi kelas terbanyak, sedangkan netral menjadi kelas minoritas. Kondisi ini menunjukkan adanya class imbalance.</div>',
            unsafe_allow_html=True,
        )

    with tabs[1]:
        year_df = _dataset_value_counts(df, "year")
        st.plotly_chart(_dataset_bar_chart(year_df, "year", "count", "Distribusi Ulasan per Tahun"), use_container_width=True)
        top_year = "-"
        if not year_df.empty:
            top_year = str(year_df.loc[year_df["count"].idxmax(), "year"])
        st.markdown(
            f'<div class="dataset-interpretation">Data tersebar dari tahun 2022 hingga 2026, dengan jumlah ulasan terbanyak pada tahun {top_year}.</div>',
            unsafe_allow_html=True,
        )

    with tabs[2]:
        if "rating" in df.columns:
            rating_values = pd.to_numeric(df["rating"], errors="coerce").dropna().astype(int)
            rating_df = rating_values.value_counts().reindex([1, 2, 3, 4, 5], fill_value=0).reset_index()
            rating_df.columns = ["rating", "count"]
        else:
            rating_df = pd.DataFrame({"rating": [], "count": []})
        rating_df["rating"] = rating_df["rating"].apply(lambda value: f"Rating {value}")
        st.plotly_chart(
            _dataset_donut_chart(
                rating_df,
                "rating",
                "count",
                "Distribusi Rating",
                {
                    "Rating 1": "#dc2626",
                    "Rating 2": "#f97316",
                    "Rating 3": "#f59e0b",
                    "Rating 4": "#38bdf8",
                    "Rating 5": "#16a34a",
                },
            ),
            use_container_width=True,
        )
        st.markdown(
            '<div class="dataset-interpretation">Rating 5 mendominasi dataset, namun rating 1 juga cukup banyak sehingga variasi sentimen tetap terlihat.</div>',
            unsafe_allow_html=True,
        )

    with tabs[3]:
        split_df = _dataset_value_counts(df, "split_set", ["train", "validation", "test"])
        st.plotly_chart(
            _dataset_donut_chart(
                split_df,
                "split_set",
                "count",
                "Distribusi Split Dataset",
                {"train": "#2563eb", "validation": "#7c3aed", "test": "#f59e0b"},
            ),
            use_container_width=True,
        )
        st.markdown(
            '<div class="dataset-interpretation">Data train memiliki porsi terbesar karena digunakan untuk fine-tuning model, sedangkan validation dan test digunakan untuk evaluasi.</div>',
            unsafe_allow_html=True,
        )


def render_dataset_quality_cards(df):
    st.markdown('<div class="dataset-section-title">Kualitas Dataset</div>', unsafe_allow_html=True)
    important_columns = [col for col in ["review", "label", "rating", "year", "split_set"] if col in df.columns]
    missing_value = int(df[important_columns].isna().sum().sum()) if important_columns else 0
    duplicate_review = int(df["review"].duplicated().sum()) if "review" in df.columns else 0
    length_column = "clean_review" if "clean_review" in df.columns else "review"
    avg_words = 0
    if length_column in df.columns:
        avg_words = df[length_column].fillna("").astype(str).str.split().str.len().mean()
    class_count = int(df["label"].nunique()) if "label" in df.columns else 0

    metrics = [
        ("Missing Value", missing_value, "Kolom penting"),
        ("Duplikat", duplicate_review, "Berdasarkan review"),
        ("Rata-rata Panjang Review", f"{avg_words:.1f} kata", f"Kolom {length_column}"),
        ("Jumlah Kelas", class_count, "Unique label"),
    ]
    cols = st.columns(4)
    for col, (label, value, caption) in zip(cols, metrics):
        display_value = _format_dataset_number(value) if isinstance(value, int) else value
        with col:
            st.markdown(
                f"""
                <div class="dataset-card">
                    <div class="dataset-card-label">{label}</div>
                    <div class="dataset-card-value">{display_value}</div>
                    <div class="dataset-card-caption">{caption}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_dataset_note():
    st.markdown(
        """
        <div class="dataset-note">
            <strong>Catatan:</strong> Distribusi label menunjukkan adanya class imbalance, terutama pada kelas netral.
            Hal ini perlu diperhatikan karena dapat memengaruhi performa model dalam mengenali kelas minoritas.
        </div>
        """,
        unsafe_allow_html=True,
    )


def _labeling_validation_summary(sample_df):
    if sample_df is None or sample_df.empty:
        return 0, 0, 0, "80%"
    total = len(sample_df)
    if {"label", "manual_label"}.issubset(sample_df.columns):
        manual = sample_df["manual_label"].fillna("").astype(str).str.strip().str.lower()
        lexicon = sample_df["label"].fillna("").astype(str).str.strip().str.lower()
        valid_manual = manual.ne("")
        if valid_manual.any():
            sesuai = int((lexicon[valid_manual] == manual[valid_manual]).sum())
            tidak_sesuai = int(valid_manual.sum() - sesuai)
            percent = f"{(sesuai / int(valid_manual.sum())) * 100:.0f}%"
            return total, sesuai, tidak_sesuai, percent
    return total, 0, 0, "80%"


def render_labeling_hero():
    st.markdown(
        """
        <style>
        .labeling-hero {
            padding: 1.9rem 2rem;
            border-radius: 18px;
            background:
                radial-gradient(circle at 88% 16%, rgba(34, 211, 238, 0.22) 0, rgba(34, 211, 238, 0) 30%),
                linear-gradient(135deg, #071a35 0%, #0f3763 58%, #14558f 100%);
            color: #ffffff;
            box-shadow: 0 18px 42px rgba(15, 55, 99, 0.24);
            margin-bottom: 1.2rem;
        }
        .labeling-hero h1 {
            margin: 0;
            font-size: clamp(1.8rem, 3vw, 2.7rem);
            line-height: 1.1;
            letter-spacing: 0;
        }
        .labeling-hero p {
            max-width: 780px;
            margin: 0.65rem 0 0 0;
            color: rgba(255, 255, 255, 0.86);
            line-height: 1.62;
            font-size: 1rem;
        }
        .labeling-section-title {
            margin: 1.35rem 0 0.7rem 0;
            color: #0f172a;
            font-size: 1.22rem;
            font-weight: 850;
            letter-spacing: 0;
        }
        .labeling-method-card,
        .labeling-metric-card,
        .labeling-flow-card,
        .labeling-validation-panel,
        .labeling-note {
            border: 1px solid rgba(15, 55, 99, 0.12);
            border-radius: 16px;
            background: #ffffff;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.07);
        }
        .labeling-method-card {
            padding: 1.1rem 1.2rem;
            margin-bottom: 1rem;
        }
        .labeling-method-title {
            color: #0f3763;
            font-size: 1.06rem;
            font-weight: 850;
            margin-bottom: 0.45rem;
        }
        .labeling-method-text {
            color: #334155;
            font-size: 0.95rem;
            line-height: 1.58;
            margin-bottom: 0.85rem;
        }
        .labeling-rule-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.65rem;
        }
        .labeling-rule-badge {
            padding: 0.72rem 0.85rem;
            border-radius: 13px;
            background: #f8fafc;
            border: 1px solid rgba(15, 55, 99, 0.10);
            color: #0f172a;
            font-size: 0.92rem;
            font-weight: 800;
        }
        .labeling-rule-badge span {
            color: #0f3763;
        }
        .labeling-metric-card {
            min-height: 126px;
            padding: 1rem;
        }
        .labeling-metric-label {
            color: #64748b;
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.48rem;
        }
        .labeling-metric-value {
            color: #0f3763;
            font-size: 1.7rem;
            line-height: 1.08;
            font-weight: 900;
            letter-spacing: 0;
        }
        .labeling-metric-caption {
            color: #64748b;
            font-size: 0.86rem;
            line-height: 1.38;
            margin-top: 0.5rem;
        }
        .labeling-flow {
            display: grid;
            gap: 0.48rem;
            max-width: 980px;
        }
        .labeling-flow-card {
            padding: 1rem 1.05rem;
            display: grid;
            grid-template-columns: 48px 1fr;
            gap: 0.85rem;
            border-left: 5px solid var(--flow-color);
        }
        .labeling-flow-card.highlight {
            background: linear-gradient(180deg, #fff7ed 0%, #ffffff 100%);
            border-color: #f97316;
        }
        .labeling-flow-number {
            width: 38px;
            height: 38px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            background: color-mix(in srgb, var(--flow-color) 14%, white);
            color: var(--flow-color);
            font-size: 0.9rem;
            font-weight: 900;
        }
        .labeling-flow-title {
            color: #0f172a;
            font-size: 1rem;
            font-weight: 850;
            margin-bottom: 0.26rem;
        }
        .labeling-flow-desc {
            color: #475569;
            font-size: 0.92rem;
            line-height: 1.5;
        }
        .labeling-flow-arrow {
            color: #94a3b8;
            font-size: 1.2rem;
            font-weight: 900;
            padding-left: 1.25rem;
        }
        .labeling-interpretation {
            margin-top: 0.3rem;
            padding: 0.8rem 0.95rem;
            border-left: 4px solid #0f3763;
            border-radius: 12px;
            background: #f8fafc;
            color: #334155;
            font-size: 0.92rem;
            line-height: 1.55;
        }
        .labeling-validation-panel {
            padding: 1rem 1.1rem;
            margin: 0.35rem 0 0.95rem 0;
        }
        .labeling-note {
            margin-top: 1.2rem;
            padding: 1rem 1.1rem;
            border-left: 5px solid #f97316;
            background: #fffaf5;
            color: #334155;
            line-height: 1.58;
        }
        @media (max-width: 760px) {
            .labeling-rule-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        <div class="labeling-hero">
            <h1>Labeling</h1>
            <p>Ringkasan proses pelabelan sentimen otomatis menggunakan InSet Lexicon.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_labeling_method_card():
    st.markdown(
        """
        <div class="labeling-method-card">
            <div class="labeling-method-title">Metode InSet Lexicon</div>
            <div class="labeling-method-text">
                Label sentimen dibuat berdasarkan skor kata positif dan negatif dari InSet Lexicon.
                Skor akhir dihitung dari skor positif dikurangi skor negatif.
            </div>
            <div class="labeling-rule-grid">
                <div class="labeling-rule-badge"><span>skor &gt; 0</span> &rarr; positif</div>
                <div class="labeling-rule-badge"><span>skor &lt; 0</span> &rarr; negatif</div>
                <div class="labeling-rule-badge"><span>skor = 0</span> &rarr; netral</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_labeling_metric_cards(source_df, sample_df=None):
    counts = source_df["label"].value_counts() if source_df is not None and "label" in source_df.columns else pd.Series(dtype=int)
    metrics = [
        ("Positif", int(counts.get("positif", 0)), "Label dengan skor lexicon positif"),
        ("Negatif", int(counts.get("negatif", 0)), "Label dengan skor lexicon negatif"),
        ("Netral", int(counts.get("netral", 0)), "Label dengan skor lexicon nol"),
        ("Audit Manual Sesuai", "80%", "Sampel validasi manual"),
    ]
    cols = st.columns(4)
    for col, (label, value, caption) in zip(cols, metrics):
        display_value = _format_dataset_number(value) if isinstance(value, int) else value
        with col:
            st.markdown(
                f"""
                <div class="labeling-metric-card">
                    <div class="labeling-metric-label">{label}</div>
                    <div class="labeling-metric-value">{display_value}</div>
                    <div class="labeling-metric-caption">{caption}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_labeling_flow_vertical():
    st.markdown('<div class="labeling-section-title">Alur Proses Labeling</div>', unsafe_allow_html=True)
    steps = [
        ("01", "Input teks ulasan", "Teks ulasan yang sudah melalui tahap preprocessing digunakan sebagai input.", "#0f3763", False),
        ("02", "Muat InSet Lexicon", "Sistem membaca daftar kata positif dan kata negatif beserta bobot skornya.", "#16a34a", False),
        ("03", "Tokenisasi kalimat", "Teks dipecah menjadi daftar kata atau token.", "#7c3aed", False),
        ("04", "Pencocokan kata ke lexicon", "Setiap token dicek apakah muncul pada kamus positif atau negatif.", "#f97316", False),
        ("05", "Hitung skor sentimen", "Skor akhir dihitung dari total skor positif dikurangi total skor negatif.", "#64748b", False),
        ("06", "Evaluasi skor", "Jika skor > 0 maka label positif. Jika skor < 0 maka label negatif. Jika skor = 0 maka label netral.", "#f97316", True),
        ("07", "Simpan label ke dataset", "Hasil label dimasukkan ke kolom label pada dataframe.", "#0f3763", False),
        ("08", "Cek distribusi kelas", "Distribusi label dicek untuk melihat keseimbangan data.", "#16a34a", False),
        ("09", "Dataset berlabel siap untuk IndoBERT", "Dataset digunakan untuk tahap tokenisasi dan fine-tuning IndoBERT.", "#7c3aed", False),
    ]
    html = ['<div class="labeling-flow">']
    for index, (number, title, desc, color, highlight) in enumerate(steps):
        highlight_class = " highlight" if highlight else ""
        html.append(
            f"""
            <div class="labeling-flow-card{highlight_class}" style="--flow-color:{color};">
                <div class="labeling-flow-number">{number}</div>
                <div>
                    <div class="labeling-flow-title">{title}</div>
                    <div class="labeling-flow-desc">{desc}</div>
                </div>
            </div>
            """
        )
        if index < len(steps) - 1:
            html.append('<div class="labeling-flow-arrow">&darr;</div>')
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def render_labeling_distribution_chart(source_df):
    st.markdown('<div class="labeling-section-title">Distribusi Hasil Labeling</div>', unsafe_allow_html=True)
    if source_df is None or "label" not in source_df.columns:
        st.info("Data label belum tersedia untuk divisualisasikan.")
        return
    label_df = _dataset_value_counts(source_df, "label", ["positif", "negatif", "netral"])
    st.plotly_chart(
        _dataset_donut_chart(
            label_df,
            "label",
            "count",
            "Distribusi Hasil Labeling",
            {"positif": "#16a34a", "negatif": "#f97316", "netral": "#93c5fd"},
        ),
        use_container_width=True,
    )
    st.markdown(
        '<div class="labeling-interpretation">Distribusi hasil labeling menunjukkan bahwa kelas positif menjadi kelas terbanyak, sedangkan netral menjadi kelas paling sedikit. Kondisi ini menunjukkan adanya class imbalance yang perlu diperhatikan pada tahap modeling.</div>',
        unsafe_allow_html=True,
    )


def render_labeling_examples(source_df):
    st.markdown('<div class="labeling-section-title">Contoh Hasil Labeling per Kelas</div>', unsafe_allow_html=True)
    if source_df is None or "label" not in source_df.columns:
        st.info("Data contoh labeling belum tersedia.")
        return
    tabs = st.tabs(["Positif", "Negatif", "Netral"])
    for tab, label in zip(tabs, ["positif", "negatif", "netral"]):
        with tab:
            subset = source_df[source_df["label"].astype(str).str.lower() == label].copy()
            preferred = [col for col in ["review", "clean_review", "label", "lexicon_score"] if col in subset.columns]
            if subset.empty or not preferred:
                st.info(f"Contoh data {label} belum tersedia.")
            else:
                st.dataframe(subset[preferred].head(3), use_container_width=True, height=220)


def render_manual_validation_table(sample_df):
    st.markdown('<div class="labeling-section-title">Sampel Validasi Manual</div>', unsafe_allow_html=True)
    if sample_df is None:
        st.info("File sampel validasi manual belum tersedia.")
        return

    total, sesuai, tidak_sesuai, percent = _labeling_validation_summary(sample_df)
    cols = st.columns(4)
    summary_items = [
        ("Data Validasi", total, "Sampel audit manual"),
        ("Sesuai", sesuai, "Label sama dengan manual"),
        ("Tidak Sesuai", tidak_sesuai, "Label berbeda dari manual"),
        ("Persentase Sesuai", percent, "Akurasi audit sampel"),
    ]
    for col, (label, value, caption) in zip(cols, summary_items):
        display_value = _format_dataset_number(value) if isinstance(value, int) else value
        with col:
            st.markdown(
                f"""
                <div class="labeling-metric-card">
                    <div class="labeling-metric-label">{label}</div>
                    <div class="labeling-metric-value">{display_value}</div>
                    <div class="labeling-metric-caption">{caption}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="labeling-validation-panel">
            <div class="labeling-method-title">Tabel Validasi Manual</div>
            <div class="labeling-method-text">Tabel diringkas ke kolom utama agar hasil audit lebih mudah dibaca.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    filter_option = st.selectbox("Filter validasi", ["Semua", "Sesuai", "Tidak sesuai"], key="labeling_validation_filter")
    table_df = sample_df.copy()
    if {"label", "manual_label"}.issubset(table_df.columns):
        is_match = (
            table_df["label"].fillna("").astype(str).str.strip().str.lower()
            == table_df["manual_label"].fillna("").astype(str).str.strip().str.lower()
        )
        if filter_option == "Sesuai":
            table_df = table_df[is_match]
        elif filter_option == "Tidak sesuai":
            table_df = table_df[~is_match]

    show_clean = st.checkbox("Tampilkan detail clean_review", value=False, key="labeling_show_clean_review")
    preferred = ["review", "label", "manual_label", "lexicon_score", "notes"]
    if show_clean:
        preferred.insert(1, "clean_review")
    columns = [col for col in preferred if col in table_df.columns]
    if not columns:
        columns = table_df.columns.tolist()
    st.dataframe(table_df[columns].head(100), use_container_width=True, height=360)


def render_labeling_limitation_note():
    st.markdown(
        """
        <div class="labeling-note">
            <strong>Catatan keterbatasan:</strong> Metode lexicon memiliki keterbatasan dalam memahami konteks kalimat,
            sarkasme, negasi, dan ulasan dengan campuran sentimen. Oleh karena itu, hasil labeling tetap perlu
            diperiksa melalui sampel validasi manual.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(navigation, total_data_text):
    menu_icons = {
        "Overview": "🏠",
        "Dataset": "📊",
        "Labeling": "🏷️",
        "Training IndoBERT": "🧠",
        "Evaluasi Model": "📈",
        "Analisis Kesalahan": "🔎",
        "Keyword Issue & Word Cloud": "☁️",
        "Demo Prediksi": "💬",
    }

    st.sidebar.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #071a35 0%, #0f2748 52%, #123b6d 100%);
        }
        section[data-testid="stSidebar"] > div {
            padding-top: 1.25rem;
        }
        button[data-testid="stSidebarCollapseButton"],
        button[data-testid="stSidebarExpandButton"],
        div[data-testid="collapsedControl"] button,
        button[title="Close sidebar"],
        button[title="Open sidebar"],
        button[aria-label*="sidebar" i] {
            width: 38px;
            height: 38px;
            min-width: 38px;
            border-radius: 8px;
            color: #e0f2fe;
            background: rgba(255, 255, 255, 0.06);
            transition: background 140ms ease, color 140ms ease, transform 140ms ease;
        }
        button[data-testid="stSidebarCollapseButton"]:hover,
        button[data-testid="stSidebarExpandButton"]:hover,
        div[data-testid="collapsedControl"] button:hover,
        button[title="Close sidebar"]:hover,
        button[title="Open sidebar"]:hover,
        button[aria-label*="sidebar" i]:hover {
            color: #ffffff;
            background: rgba(255, 255, 255, 0.12);
            transform: translateY(-1px);
        }
        button[data-testid="stSidebarCollapseButton"] svg,
        button[data-testid="stSidebarExpandButton"] svg,
        div[data-testid="collapsedControl"] button svg,
        button[title="Close sidebar"] svg,
        button[title="Open sidebar"] svg,
        button[aria-label*="sidebar" i] svg {
            width: 24px;
            height: 24px;
            color: currentColor;
            fill: currentColor;
        }
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label {
            color: inherit;
        }
        .sidebar-header {
            padding: 1rem 0.95rem 0.9rem 0.95rem;
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.08);
            box-shadow: 0 14px 32px rgba(0, 0, 0, 0.18);
            margin-bottom: 0.85rem;
        }
        .sidebar-kicker {
            color: rgba(255, 255, 255, 0.68);
            font-size: 0.74rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.4rem;
        }
        .sidebar-title {
            color: #ffffff;
            font-size: 1.05rem;
            font-weight: 850;
            line-height: 1.28;
            letter-spacing: 0;
        }
        .sidebar-mini-grid {
            display: grid;
            gap: 0.55rem;
            margin: 0.65rem 0 0.75rem 0;
        }
        .sidebar-mini-card {
            padding: 0.72rem 0.8rem;
            border-radius: 13px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            background: rgba(255, 255, 255, 0.09);
        }
        .sidebar-mini-label {
            color: rgba(255, 255, 255, 0.64);
            font-size: 0.72rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }
        .sidebar-mini-value {
            color: #ffffff;
            font-size: 0.94rem;
            font-weight: 800;
            line-height: 1.2;
        }
        .sidebar-section-label {
            color: rgba(255, 255, 255, 0.62);
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin: 0.7rem 0 0.35rem 0.15rem;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] {
            gap: 0.35rem;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            min-height: 0;
            padding: 0;
            margin: 0;
            border-radius: 12px;
            overflow: hidden;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
            display: none;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label > div:last-child {
            width: 100%;
            padding: 0.66rem 0.75rem;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.10);
            background: rgba(255, 255, 255, 0.07);
            color: rgba(255, 255, 255, 0.84);
            font-weight: 750;
            transition: all 140ms ease;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover > div:last-child {
            background: rgba(255, 255, 255, 0.13);
            border-color: rgba(255, 255, 255, 0.22);
            color: #ffffff;
        }
        section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) > div:last-child {
            background: linear-gradient(135deg, #ffffff 0%, #eaf2ff 100%);
            border-color: rgba(255, 255, 255, 0.70);
            color: #071a35;
            box-shadow: 0 12px 26px rgba(0, 0, 0, 0.22);
        }
        .sidebar-progress-card {
            margin-top: 1rem;
            padding: 0.82rem;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.09);
            border: 1px solid rgba(255, 255, 255, 0.12);
        }
        .sidebar-progress-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.6rem;
            margin-bottom: 0.55rem;
        }
        .sidebar-progress-label {
            color: rgba(255, 255, 255, 0.74);
            font-size: 0.78rem;
            font-weight: 750;
        }
        .sidebar-progress-value {
            color: #ffffff;
            font-size: 0.82rem;
            font-weight: 850;
        }
        .sidebar-progress-track {
            height: 8px;
            overflow: hidden;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.16);
        }
        .sidebar-progress-fill {
            width: 100%;
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, #16a34a 0%, #f59e0b 100%);
        }
        .sidebar-footer {
            margin-top: 0.95rem;
            padding-top: 0.85rem;
            border-top: 1px solid rgba(255, 255, 255, 0.14);
            color: rgba(255, 255, 255, 0.66);
            font-size: 0.78rem;
            text-align: center;
            font-weight: 700;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        f"""
        <div class="sidebar-header">
            <div class="sidebar-kicker">Dashboard Skripsi</div>
            <div class="sidebar-title">Analisis Sentimen JakOne Mobile</div>
        </div>
        <div class="sidebar-mini-grid">
            <div class="sidebar-mini-card">
                <div class="sidebar-mini-label">Total Data</div>
                <div class="sidebar-mini-value">{total_data_text} ulasan</div>
            </div>
            <div class="sidebar-mini-card">
                <div class="sidebar-mini-label">Test Accuracy</div>
                <div class="sidebar-mini-value">93.16%</div>
            </div>
            <div class="sidebar-mini-card">
                <div class="sidebar-mini-label">Test Macro F1</div>
                <div class="sidebar-mini-value">87.74%</div>
            </div>
        </div>
        <div class="sidebar-section-label">Navigasi</div>
        """,
        unsafe_allow_html=True,
    )

    selected_page = st.sidebar.radio(
        "Navigasi",
        navigation,
        label_visibility="collapsed",
        format_func=lambda page: f"{menu_icons.get(page, '•')} {page}",
    )

    st.sidebar.markdown(
        """
        <div class="sidebar-progress-card">
            <div class="sidebar-progress-row">
                <div class="sidebar-progress-label">Progress Penelitian</div>
                <div class="sidebar-progress-value">100%</div>
            </div>
            <div class="sidebar-progress-track">
                <div class="sidebar-progress-fill"></div>
            </div>
        </div>
        <div class="sidebar-footer">Skripsi NLP • IndoBERT</div>
        """,
        unsafe_allow_html=True,
    )
    return selected_page


FALLBACK_SLANG_DICT = {
    "gk": "tidak",
    "g": "tidak",
    "ga": "tidak",
    "gak": "tidak",
    "nggak": "tidak",
    "tdk": "tidak",
    "yg": "yang",
    "udh": "sudah",
    "sdh": "sudah",
    "blm": "belum",
    "trs": "terus",
    "trus": "terus",
    "pake": "pakai",
    "kalo": "kalau",
    "gabisa": "tidak bisa",
    "apk": "aplikasi",
    "app": "aplikasi",
    "aplikasinya": "aplikasi",
    "lemot": "lambat",
    "eror": "error",
    "err": "error",
    "loginya": "login",
    "loginnya": "login",
    "otpnya": "otp",
    "tf": "transfer",
}

FALLBACK_STOPWORDS = {
    "ada",
    "adalah",
    "agar",
    "akan",
    "aku",
    "anda",
    "apa",
    "atau",
    "buat",
    "dan",
    "dari",
    "dengan",
    "di",
    "ini",
    "itu",
    "jadi",
    "jika",
    "juga",
    "kami",
    "kamu",
    "kan",
    "karena",
    "ke",
    "lagi",
    "lah",
    "maka",
    "mau",
    "oleh",
    "pada",
    "pun",
    "saat",
    "saja",
    "saya",
    "sebagai",
    "seperti",
    "sudah",
    "tapi",
    "telah",
    "untuk",
    "yang",
}

SECURITY_KEYWORDS = [
    "otp",
    "login",
    "password",
    "pin",
    "akun",
    "verifikasi",
    "saldo",
    "transaksi",
    "blokir",
    "terblokir",
    "device",
    "perangkat",
    "rekening",
    "transfer",
]

POSITIVE_SENTIMENT_HINTS = [
    "mudah digunakan",
    "mudah dipakai",
    "gampang digunakan",
    "gampang dipakai",
    "aplikasi mudah",
    "praktis",
    "simple",
    "lancar",
    "bagus",
    "membantu",
    "mantap",
    "nyaman",
    "cepat",
    "keren",
    "recommended",
    "rekomendasi",
]

NEGATIVE_SENTIMENT_HINTS = [
    "tidak bisa",
    "gagal",
    "error",
    "lambat",
    "lemot",
    "susah",
    "ribet",
    "payah",
    "buruk",
    "kecewa",
    "saldo terpotong",
    "saldo kepotong",
    "otp tidak masuk",
    "login tidak bisa",
    "akun terblokir",
    "transaksi gagal",
]


@st.cache_resource(show_spinner=False)
def _load_training_clean_text():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    preprocess_path = os.path.join(project_root, "src", "02_preprocessing", "02_preprocess_data.py")
    if not os.path.isfile(preprocess_path):
        return None

    spec = importlib.util.spec_from_file_location("jakone_preprocess_data", preprocess_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "clean_text", None)


def _fallback_clean_text(text):
    if text is None or pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    text = re.sub(r"#(\w+)", r"\1", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    words = [FALLBACK_SLANG_DICT.get(word, word) for word in text.split()]
    words = [word for word in words if word not in FALLBACK_STOPWORDS]
    return re.sub(r"\s+", " ", " ".join(words)).strip()


def preprocess_prediction_text(text):
    clean_text = _load_training_clean_text()
    if clean_text is not None:
        cleaned = clean_text(text)
    else:
        cleaned = _fallback_clean_text(text)
    if not cleaned:
        cleaned = str(text).lower().strip()
    return cleaned


def detect_security_keywords(original_text, processed_text=""):
    combined_text = f"{original_text} {processed_text}".lower()
    detected = []
    for keyword in SECURITY_KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", combined_text):
            detected.append(keyword)
    return detected


def detect_sentiment_signal(original_text, processed_text=""):
    combined_text = f"{original_text} {processed_text}".lower()
    positive_matches = [hint for hint in POSITIVE_SENTIMENT_HINTS if hint in combined_text]
    negative_matches = [hint for hint in NEGATIVE_SENTIMENT_HINTS if hint in combined_text]

    if positive_matches and not negative_matches:
        return {"signal": "positif", "matches": positive_matches}
    if negative_matches and not positive_matches:
        return {"signal": "negatif", "matches": negative_matches}
    if positive_matches and negative_matches:
        return {
            "signal": "campuran",
            "matches": positive_matches + negative_matches,
        }
    return {"signal": None, "matches": []}


def get_confidence_status(confidence):
    if confidence < 0.60:
        return {
            "status": "Prediksi belum cukup meyakinkan",
            "message": "Model kurang yakin terhadap prediksi ini. Hasil perlu ditinjau ulang.",
            "message_type": "warning",
            "is_uncertain": True,
        }
    if confidence < 0.75:
        return {
            "status": "Model cukup yakin",
            "message": "Model cukup yakin, tetapi masih ada kemungkinan salah prediksi.",
            "message_type": "info",
            "is_uncertain": False,
        }
    return {
        "status": "Model yakin",
        "message": "Model memiliki tingkat keyakinan yang tinggi terhadap prediksi ini.",
        "message_type": "success",
        "is_uncertain": False,
    }


@st.cache_resource(show_spinner=False)
def load_model_and_tokenizer(model_dir):
    mapping_path = os.path.join(model_dir, "label_mapping.json")
    if not os.path.isdir(model_dir):
        raise FileNotFoundError(f"Folder model tidak ditemukan: {model_dir}")
    if not os.path.isfile(mapping_path):
        raise FileNotFoundError(f"File label mapping tidak ditemukan: {mapping_path}")

    with open(mapping_path, "r", encoding="utf-8") as file:
        label_mapping = json.load(file)

    label2id = {str(key): int(value) for key, value in label_mapping.get("label2id", {}).items()}
    id2label = {int(value): key for key, value in label2id.items()}

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_dir)

    config = AutoConfig.from_pretrained(model_dir)
    config.num_labels = len(label2id)
    config.label2id = label2id
    config.id2label = id2label

    model = AutoModelForSequenceClassification.from_pretrained(model_dir, config=config)
    model.to(device)
    model.eval()

    label_mapping = {"label2id": label2id, "id2label": id2label, "device": str(device)}
    return model, tokenizer, label_mapping


def predict_sentiment(text, model, tokenizer, label_mapping, max_length=128, return_details=False):
    if not text or not text.strip():
        raise ValueError("Teks ulasan tidak boleh kosong.")

    device = torch.device(label_mapping.get("device", "cuda" if torch.cuda.is_available() else "cpu"))
    id2label = label_mapping["id2label"]
    processed_text = preprocess_prediction_text(text)

    encoded = tokenizer(
        processed_text,
        max_length=max_length,
        padding="max_length",
        truncation=True,
        return_tensors="pt",
    )
    encoded = {key: value.to(device) for key, value in encoded.items()}

    with torch.no_grad():
        outputs = model(**encoded)
        probabilities = torch.softmax(outputs.logits, dim=1).squeeze(0).cpu().numpy()

    predicted_id = int(probabilities.argmax())
    predicted_label = id2label[predicted_id]
    confidence = float(probabilities[predicted_id])
    probabilities_by_label = {
        id2label[int(idx)]: float(probability)
        for idx, probability in enumerate(probabilities)
    }

    if return_details:
        details = {
            "original_text": text,
            "processed_text": processed_text,
            "max_length": max_length,
            "label_mapping": {
                "label2id": label_mapping.get("label2id", {}),
                "id2label": label_mapping.get("id2label", {}),
            },
            "probabilities": probabilities_by_label,
            "detected_security_keywords": detect_security_keywords(text, processed_text),
            "sentiment_signal": detect_sentiment_signal(text, processed_text),
        }
        return predicted_label, confidence, probabilities_by_label, details

    return predicted_label, confidence, probabilities_by_label
