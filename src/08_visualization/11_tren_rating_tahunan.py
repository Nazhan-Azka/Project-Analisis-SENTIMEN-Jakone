from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATASET_PATH = Path("data/raw/jakone_reviews_raw.csv")
OUTPUT_DIR = Path("outputs/figures/tren_rating_2022_2026")
START_YEAR = 2022
END_YEAR = 2026

DATE_COLUMN_CANDIDATES = ["review_date", "at", "date", "tanggal"]
RATING_COLUMN_CANDIDATES = ["rating", "score"]


def find_column(df: pd.DataFrame, candidates: list[str], column_type: str) -> str:
    for column in candidates:
        if column in df.columns:
            return column
    raise ValueError(
        f"Kolom {column_type} tidak ditemukan. Kandidat yang dicari: "
        f"{', '.join(candidates)}"
    )


def load_dataset(path: Path) -> tuple[pd.DataFrame, str, str]:
    if not path.exists():
        raise FileNotFoundError(f"File dataset tidak ditemukan: {path}")

    df = pd.read_csv(path)
    date_column = find_column(df, DATE_COLUMN_CANDIDATES, "tanggal ulasan")
    rating_column = find_column(df, RATING_COLUMN_CANDIDATES, "rating/score")

    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column], errors="coerce")
    df[rating_column] = pd.to_numeric(df[rating_column], errors="coerce")
    df = df.dropna(subset=[date_column, rating_column])
    df["tahun"] = df[date_column].dt.year
    df = df[df["tahun"].between(START_YEAR, END_YEAR, inclusive="both")]

    return df, date_column, rating_column


def summarize_by_year(df: pd.DataFrame, rating_column: str) -> pd.DataFrame:
    years = pd.Index(range(START_YEAR, END_YEAR + 1), name="tahun")

    summary = (
        df.groupby("tahun")
        .agg(
            rata_rata_rating=(rating_column, "mean"),
            jumlah_data=(rating_column, "size"),
            jumlah_rating_rendah=(rating_column, lambda x: x.isin([1, 2]).sum()),
        )
        .reindex(years)
    )

    summary["persentase_rating_rendah"] = (
        summary["jumlah_rating_rendah"] / summary["jumlah_data"] * 100
    )
    summary["rata_rata_rating"] = summary["rata_rata_rating"].round(3)
    summary["persentase_rating_rendah"] = summary["persentase_rating_rendah"].round(2)

    count_columns = ["jumlah_data", "jumlah_rating_rendah"]
    summary[count_columns] = summary[count_columns].astype("Int64")
    return summary.reset_index()


def annotate_point(ax, x_value: int, y_value: float, label: str) -> None:
    ax.annotate(
        label,
        xy=(x_value, y_value),
        xytext=(0, 14),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        color="#b91c1c",
        fontweight="bold",
    )


def plot_average_rating(summary: pd.DataFrame, output_path: Path) -> None:
    critical_row = summary.dropna(subset=["rata_rata_rating"]).sort_values(
        "rata_rata_rating", ascending=True
    ).head(1)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(
        summary["tahun"],
        summary["rata_rata_rating"],
        marker="o",
        linewidth=2.2,
        color="#2563eb",
        label="Rata-rata rating",
    )

    if not critical_row.empty:
        year = int(critical_row["tahun"].iloc[0])
        value = float(critical_row["rata_rata_rating"].iloc[0])
        ax.scatter(year, value, color="#dc2626", s=90, zorder=5, label="Rating terendah")
        annotate_point(ax, year, value, f"Terendah: {year}")

    ax.set_title("Rata-rata Rating Ulasan JakOne Mobile per Tahun")
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Rata-rata rating")
    ax.set_xticks(range(START_YEAR, END_YEAR + 1))
    ax.set_ylim(1, 5)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_low_rating_percentage(summary: pd.DataFrame, output_path: Path) -> None:
    critical_row = summary.dropna(subset=["persentase_rating_rendah"]).sort_values(
        "persentase_rating_rendah", ascending=False
    ).head(1)
    critical_year = None if critical_row.empty else int(critical_row["tahun"].iloc[0])

    bar_colors = [
        "#dc2626" if year == critical_year else "#10b981"
        for year in summary["tahun"]
    ]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(
        summary["tahun"],
        summary["persentase_rating_rendah"],
        color=bar_colors,
        width=0.65,
        label="Persentase rating 1-2",
    )

    if not critical_row.empty:
        year = int(critical_row["tahun"].iloc[0])
        value = float(critical_row["persentase_rating_rendah"].iloc[0])
        annotate_point(ax, year, value, f"Tertinggi: {year}")

    ax.set_title("Persentase Ulasan Rating Rendah JakOne Mobile per Tahun")
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Persentase rating 1-2 (%)")
    ax.set_xticks(range(START_YEAR, END_YEAR + 1))
    ax.set_ylim(0, max(10, summary["persentase_rating_rendah"].max(skipna=True) * 1.18))
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df, date_column, rating_column = load_dataset(DATASET_PATH)
    summary = summarize_by_year(df, rating_column)

    rating_chart_path = OUTPUT_DIR / "rating_per_tahun.png"
    low_rating_chart_path = OUTPUT_DIR / "rating_rendah_per_tahun.png"
    summary_path = OUTPUT_DIR / "ringkasan_rating_per_tahun.csv"

    plot_average_rating(summary, rating_chart_path)
    plot_low_rating_percentage(summary, low_rating_chart_path)
    summary.to_csv(summary_path, index=False, encoding="utf-8-sig")

    print("\nDataset yang digunakan:")
    print(f"- Path file CSV : {DATASET_PATH}")
    print(f"- Kolom tanggal : {date_column}")
    print(f"- Kolom rating  : {rating_column}")
    print(f"- Rentang tahun : {START_YEAR}-{END_YEAR}")

    print("\nTabel validasi tren rating per tahun:")
    print(summary.to_string(index=False))

    print("\nJumlah total ulasan per tahun:")
    print(summary[["tahun", "jumlah_data"]].to_string(index=False))

    print("\nFile output:")
    print(f"- {rating_chart_path}")
    print(f"- {low_rating_chart_path}")
    print(f"- {summary_path}")


if __name__ == "__main__":
    main()
