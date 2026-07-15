from __future__ import annotations

import re
import sys
import string
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


TAHUN_ANALISIS = [2022, 2023, 2024]
OUTPUT_DIR = Path("output_analisis")


def cari_file_input() -> Path:
    kandidat = [
        Path("jakone_reviews_2022_2024.csv"),
        Path("docs") / "Analisis Latar Belakang" / "jakone_reviews_2022_2024.csv",
    ]
    for path in kandidat:
        if path.exists():
            return path
    raise FileNotFoundError(
        "File jakone_reviews_2022_2024.csv tidak ditemukan di root repo "
        "atau docs/Analisis Latar Belakang/."
    )


def baca_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    kolom_wajib = {
        "userName",
        "tanggal",
        "tahun",
        "rating",
        "ulasan",
        "thumbsUp",
        "versiApp",
        "balasanBank",
        "tanggalBalasan",
        "reviewId",
    }
    kolom_hilang = sorted(kolom_wajib - set(df.columns))
    if kolom_hilang:
        raise ValueError(f"Kolom wajib tidak ditemukan: {', '.join(kolom_hilang)}")

    df = df.copy()
    df["tahun"] = pd.to_numeric(df["tahun"], errors="coerce").astype("Int64")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["thumbsUp"] = pd.to_numeric(df["thumbsUp"], errors="coerce").fillna(0).astype(int)
    df["ulasan"] = df["ulasan"].fillna("").astype(str)
    df = df[df["tahun"].isin(TAHUN_ANALISIS)].copy()
    return df


def hitung_volume_keluhan(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for tahun in TAHUN_ANALISIS:
        dft = df[df["tahun"] == tahun]
        total = len(dft)
        jumlah_keluhan = int(dft["rating"].isin([1, 2]).sum())
        jumlah_puas = int(dft["rating"].isin([4, 5]).sum())
        rows.append(
            {
                "tahun": tahun,
                "total_review": total,
                "jumlah_rating_1_2": jumlah_keluhan,
                "persen_rating_1_2": round((jumlah_keluhan / total * 100) if total else 0, 2),
                "jumlah_rating_4_5": jumlah_puas,
                "persen_rating_4_5": round((jumlah_puas / total * 100) if total else 0, 2),
            }
        )
    return pd.DataFrame(rows)


def hitung_rating_tahunan(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    ringkasan = (
        df.groupby("tahun")["rating"]
        .agg(rata_rata_rating="mean", median_rating="median")
        .reindex(TAHUN_ANALISIS)
        .reset_index()
    )
    ringkasan["rata_rata_rating"] = ringkasan["rata_rata_rating"].round(3)
    ringkasan["median_rating"] = ringkasan["median_rating"].round(3)

    awal = ringkasan.loc[ringkasan["tahun"] == 2022, "rata_rata_rating"].iloc[0]
    akhir = ringkasan.loc[ringkasan["tahun"] == 2024, "rata_rata_rating"].iloc[0]
    selisih = akhir - awal
    if pd.isna(selisih):
        tren = "tidak dapat ditentukan"
    elif abs(selisih) < 0.05:
        tren = "stabil"
    elif selisih > 0:
        tren = "naik"
    else:
        tren = "turun"

    ringkasan["tren_2022_2024"] = tren
    return ringkasan, tren


STOPWORDS = {
    "yang",
    "dan",
    "di",
    "ke",
    "dari",
    "ini",
    "itu",
    "saya",
    "aplikasi",
    "jakone",
    "mobile",
    "bank",
    "dki",
    "untuk",
    "ada",
    "ya",
    "nya",
    "dengan",
    "pada",
    "juga",
    "saja",
    "atau",
    "akan",
    "sudah",
    "masih",
    "bisa",
    "kalau",
    "jadi",
    "banget",
    "kok",
    "gak",
    "ga",
    "kan",
    "aja",
    "lagi",
    "the",
    "a",
    "an",
    "is",
    "to",
    "of",
    "in",
    "on",
    "for",
    "and",
    "good",
}


def bersihkan_teks(teks: str) -> list[str]:
    teks = teks.lower()
    teks = re.sub(r"https?://\S+|www\.\S+", " ", teks)
    teks = re.sub(r"@\w+", " ", teks)
    teks = teks.encode("ascii", "ignore").decode("ascii")
    teks = teks.translate(str.maketrans("", "", string.punctuation))
    teks = re.sub(r"\d+", " ", teks)
    teks = re.sub(r"\s+", " ", teks).strip()
    token = [kata for kata in teks.split() if len(kata) > 2 and kata not in STOPWORDS]
    return token


def hitung_kata_kunci(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[int, Counter]]:
    df_keluhan = df[df["rating"].isin([1, 2])].copy()
    counter_per_tahun: dict[int, Counter] = {}
    top_per_tahun: dict[int, list[tuple[str, int]]] = {}

    for tahun in TAHUN_ANALISIS:
        counter = Counter()
        for ulasan in df_keluhan.loc[df_keluhan["tahun"] == tahun, "ulasan"]:
            counter.update(bersihkan_teks(ulasan))
        counter_per_tahun[tahun] = counter
        top_per_tahun[tahun] = counter.most_common(15)

    semua_kata = sorted({kata for top in top_per_tahun.values() for kata, _ in top})
    rows = []
    for kata in semua_kata:
        row = {"kata_kunci": kata}
        jumlah_tahun_muncul = 0
        for tahun in TAHUN_ANALISIS:
            top_kata = [item[0] for item in top_per_tahun[tahun]]
            freq = counter_per_tahun[tahun][kata]
            row[f"frekuensi_{tahun}"] = freq
            row[f"rank_{tahun}"] = top_kata.index(kata) + 1 if kata in top_kata else ""
            row[f"top15_{tahun}"] = kata in top_kata
            if freq > 0:
                jumlah_tahun_muncul += 1
        row["muncul_di_semua_tahun"] = jumlah_tahun_muncul == len(TAHUN_ANALISIS)
        row["total_frekuensi"] = sum(counter_per_tahun[tahun][kata] for tahun in TAHUN_ANALISIS)
        rows.append(row)

    hasil = pd.DataFrame(rows).sort_values(
        by=["muncul_di_semua_tahun", "total_frekuensi", "kata_kunci"],
        ascending=[False, False, True],
    )
    return hasil, counter_per_tahun


def ambil_kutipan(df: pd.DataFrame) -> pd.DataFrame:
    pola_keluhan = re.compile(
        r"\b(?:error|gagal|otp|login|loading|salah|lemot|ribet|susah|tidak|ga|gak|"
        r"nggak|masalah|kecewa|terkunci|time\s*out|muter|blur|jelek|aneh|"
        r"verifikasi|saldo|transfer|masuk|daftar)\b",
        flags=re.IGNORECASE,
    )
    pola_pujian = re.compile(
        r"\b(?:keren|mudah|cepat|bagus|sukses|mantap|good|terbaik)\b",
        flags=re.IGNORECASE,
    )
    rows = []
    for tahun in TAHUN_ANALISIS:
        kandidat = df[(df["tahun"] == tahun) & (df["rating"] == 1)].copy()
        kandidat["panjang_ulasan"] = kandidat["ulasan"].str.len()
        kandidat["mengandung_keluhan"] = kandidat["ulasan"].str.contains(pola_keluhan, na=False)
        kandidat["mengandung_pujian"] = kandidat["ulasan"].str.contains(pola_pujian, na=False)
        utama = kandidat[
            kandidat["panjang_ulasan"].between(30, 150, inclusive="both")
            & (kandidat["thumbsUp"] > 0)
            & (kandidat["mengandung_keluhan"])
        ].copy()
        if len(utama) < 3:
            fallback = kandidat[
                kandidat["panjang_ulasan"].between(30, 150, inclusive="both")
                & (kandidat["mengandung_keluhan"])
            ].copy()
            utama = pd.concat([utama, fallback], ignore_index=True).drop_duplicates(subset=["ulasan"])

        if len(utama) < 3:
            utama = pd.concat([utama, kandidat], ignore_index=True).drop_duplicates(subset=["ulasan"])

        utama["skor_representatif"] = (
            utama["thumbsUp"].fillna(0) * 20
            + utama["mengandung_keluhan"].astype(int) * 100
            - utama["mengandung_pujian"].astype(int) * 80
            - (utama["panjang_ulasan"] - 90).abs()
        )
        pilihan = utama.sort_values(
            by=["skor_representatif", "thumbsUp", "panjang_ulasan"],
            ascending=[False, False, True],
        ).head(3)
        rows.append(pilihan[["tahun", "rating", "ulasan", "thumbsUp"]])
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def setup_plot() -> None:
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update(
        {
            "figure.dpi": 120,
            "savefig.dpi": 180,
            "font.size": 10,
            "axes.titlesize": 13,
            "axes.labelsize": 10,
            "axes.titleweight": "bold",
            "axes.edgecolor": "#D1D5DB",
            "grid.color": "#E5E7EB",
        }
    )


def buat_grafik_volume(tabel: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    warna = "#C2410C"
    bars = ax.bar(tabel["tahun"].astype(str), tabel["jumlah_rating_1_2"], color=warna)
    ax.set_title("Volume Review Keluhan Rating 1-2 per Tahun")
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Jumlah review rating 1-2")
    ax.bar_label(
        bars,
        labels=[f"{p:.2f}%" for p in tabel["persen_rating_1_2"]],
        padding=4,
        fontsize=9,
    )
    ax.set_ylim(0, max(tabel["jumlah_rating_1_2"].max() * 1.18, 1))
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "grafik_volume_keluhan_per_tahun.png", bbox_inches="tight")
    plt.close(fig)


def buat_grafik_rating(tabel: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(
        tabel["tahun"].astype(str),
        tabel["rata_rata_rating"],
        marker="o",
        linewidth=2.5,
        color="#2563EB",
    )
    for _, row in tabel.iterrows():
        ax.annotate(
            f"{row['rata_rata_rating']:.3f}",
            (str(int(row["tahun"])), row["rata_rata_rating"]),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=9,
        )
    ax.set_title("Tren Rata-rata Rating per Tahun")
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Rata-rata rating")
    ax.set_ylim(1, 5)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "grafik_tren_rata_rata_rating.png", bbox_inches="tight")
    plt.close(fig)


def buat_grafik_kata_kunci(counter_per_tahun: dict[int, Counter]) -> None:
    for tahun in TAHUN_ANALISIS:
        top10 = counter_per_tahun[tahun].most_common(10)
        kata = [item[0] for item in top10]
        frekuensi = [item[1] for item in top10]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(kata[::-1], frekuensi[::-1], color="#0F766E")
        ax.set_title(f"Top 10 Kata Kunci Keluhan Rating 1-2 Tahun {tahun}")
        ax.set_xlabel("Frekuensi")
        ax.set_ylabel("Kata kunci")
        for i, value in enumerate(frekuensi[::-1]):
            ax.text(value + max(frekuensi) * 0.01, i, str(value), va="center", fontsize=9)
        ax.set_xlim(0, max(frekuensi) * 1.15 if frekuensi else 1)
        fig.tight_layout()
        fig.savefig(OUTPUT_DIR / f"grafik_kata_kunci_{tahun}.png", bbox_inches="tight")
        plt.close(fig)


def susun_ringkasan(
    volume: pd.DataFrame,
    rating: pd.DataFrame,
    tren_rating: str,
    kata_kunci: pd.DataFrame,
) -> str:
    v2022 = volume[volume["tahun"] == 2022].iloc[0]
    v2023 = volume[volume["tahun"] == 2023].iloc[0]
    v2024 = volume[volume["tahun"] == 2024].iloc[0]
    arah_keluhan = (
        "naik"
        if v2024["persen_rating_1_2"] > v2022["persen_rating_1_2"]
        else "turun"
        if v2024["persen_rating_1_2"] < v2022["persen_rating_1_2"]
        else "stabil"
    )

    r2022 = rating[rating["tahun"] == 2022].iloc[0]
    r2023 = rating[rating["tahun"] == 2023].iloc[0]
    r2024 = rating[rating["tahun"] == 2024].iloc[0]

    konsisten = kata_kunci[kata_kunci["muncul_di_semua_tahun"] == True]["kata_kunci"].head(10).tolist()
    if konsisten:
        teks_konsisten = ", ".join(konsisten)
    else:
        teks_konsisten = "tidak ada kata kunci top-15 yang muncul di semua tahun"

    pola_tahun = []
    for tahun in TAHUN_ANALISIS:
        kol_freq = f"frekuensi_{tahun}"
        kol_rank = f"rank_{tahun}"
        top = (
            kata_kunci[kata_kunci[kol_rank] != ""]
            .sort_values(by=kol_rank)
            .head(5)[["kata_kunci", kol_freq]]
        )
        pola_tahun.append(
            f"{tahun}: "
            + ", ".join(f"{row.kata_kunci} ({int(getattr(row, kol_freq))})" for row in top.itertuples())
        )

    ringkasan = [
        (
            "Volume keluhan rating 1-2 dari 2022 ke 2024 menunjukkan tren "
            f"{arah_keluhan}. Pada 2022 terdapat {int(v2022['jumlah_rating_1_2'])} "
            f"keluhan dari {int(v2022['total_review'])} review "
            f"({v2022['persen_rating_1_2']:.2f}%). Pada 2023 jumlahnya menjadi "
            f"{int(v2023['jumlah_rating_1_2'])} dari {int(v2023['total_review'])} review "
            f"({v2023['persen_rating_1_2']:.2f}%), dan pada 2024 menjadi "
            f"{int(v2024['jumlah_rating_1_2'])} dari {int(v2024['total_review'])} review "
            f"({v2024['persen_rating_1_2']:.2f}%). Sebagai pembanding, review puas "
            f"rating 4-5 berada pada {v2022['persen_rating_4_5']:.2f}% pada 2022, "
            f"{v2023['persen_rating_4_5']:.2f}% pada 2023, dan "
            f"{v2024['persen_rating_4_5']:.2f}% pada 2024."
        ),
        (
            "Rata-rata rating tahunan bergerak "
            f"{tren_rating} dari 2022 ke 2024. Nilai mean rating adalah "
            f"{r2022['rata_rata_rating']:.3f} pada 2022, {r2023['rata_rata_rating']:.3f} "
            f"pada 2023, dan {r2024['rata_rata_rating']:.3f} pada 2024. Median rating "
            f"masing-masing tahun adalah {r2022['median_rating']:.3f}, "
            f"{r2023['median_rating']:.3f}, dan {r2024['median_rating']:.3f}."
        ),
        (
            "Pada review keluhan rating 1-2, kata kunci yang konsisten muncul di seluruh "
            f"periode adalah {teks_konsisten}. Kata-kata ini menunjukkan isu yang berulang "
            "dalam pengalaman pengguna, terutama terkait kendala teknis, akses, atau proses "
            "transaksi jika kata tersebut berkaitan dengan fungsi aplikasi."
        ),
        (
            "Pola kata kunci paling menonjol per tahun adalah "
            + "; ".join(pola_tahun)
            + ". Perbandingan ini dapat digunakan untuk melihat apakah masalah tertentu "
            "bertahan sepanjang waktu atau lebih dominan pada tahun tertentu."
        ),
    ]
    return "\n\n".join(ringkasan)


def print_csv(path: Path) -> None:
    print(f"\n===== {path.as_posix()} =====")
    print(pd.read_csv(path, keep_default_na=False).to_string(index=False))


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    OUTPUT_DIR.mkdir(exist_ok=True)
    setup_plot()

    input_path = cari_file_input()
    df = baca_data(input_path)

    tabel_volume = hitung_volume_keluhan(df)
    tabel_rating, tren_rating = hitung_rating_tahunan(df)
    tabel_kata_kunci, counter_per_tahun = hitung_kata_kunci(df)
    tabel_kutipan = ambil_kutipan(df)

    path_volume = OUTPUT_DIR / "tabel_volume_keluhan_per_tahun.csv"
    path_rating = OUTPUT_DIR / "tabel_rata_rata_rating_per_tahun.csv"
    path_kata_kunci = OUTPUT_DIR / "tabel_kata_kunci_per_tahun.csv"
    path_kutipan = OUTPUT_DIR / "contoh_kutipan_per_tahun.csv"

    tabel_volume.to_csv(path_volume, index=False, encoding="utf-8-sig")
    tabel_rating.to_csv(path_rating, index=False, encoding="utf-8-sig")
    tabel_kata_kunci.to_csv(path_kata_kunci, index=False, encoding="utf-8-sig")
    tabel_kutipan.to_csv(path_kutipan, index=False, encoding="utf-8-sig")

    buat_grafik_volume(tabel_volume)
    buat_grafik_rating(tabel_rating)
    buat_grafik_kata_kunci(counter_per_tahun)

    ringkasan = susun_ringkasan(tabel_volume, tabel_rating, tren_rating, tabel_kata_kunci)
    (OUTPUT_DIR / "ringkasan_narasi.txt").write_text(ringkasan, encoding="utf-8")

    print("\nRINGKASAN NARASI\n")
    print(ringkasan)
    print("\nCSV RINGKASAN")
    for path in [path_volume, path_rating, path_kata_kunci, path_kutipan]:
        print_csv(path)


if __name__ == "__main__":
    main()
