from pathlib import Path
from time import sleep

import pandas as pd
from google_play_scraper import Sort, app, reviews


APP_ID = "com.dev.jakone.mbanking"
TARGET_REVIEWS = 140000
START_YEAR = 2022
END_YEAR = 2026
OUTPUT_PATH = "data/raw/jakone_reviews_raw.csv"

LANGUAGE = "id"
COUNTRY = "id"
BATCH_SIZE = 200
REQUEST_DELAY_SECONDS = 1
MAX_RETRIES = 3

OUTPUT_COLUMNS = [
    "review_id",
    "review",
    "rating",
    "review_date",
    "app_version",
    "thumbs_up_count",
    "year",
]


def validate_app_metadata():
    """Memastikan package name valid sebelum mengambil ulasan."""
    try:
        metadata = app(APP_ID, lang=LANGUAGE, country=COUNTRY)
    except Exception as exc:
        print("\nStatus metadata aplikasi: GAGAL")
        print(f"Package name yang digunakan: {APP_ID}")
        print(f"Error saat mengambil metadata aplikasi: {exc}")
        print("Proses dihentikan karena metadata aplikasi tidak dapat divalidasi.")
        return None

    print("\nStatus metadata aplikasi: BERHASIL")
    print(f"Nama aplikasi: {metadata.get('title', '-')}")
    print(f"Developer: {metadata.get('developer', '-')}")
    print(f"Rating aplikasi: {metadata.get('score', '-')}")
    print(f"Jumlah review: {metadata.get('reviews', '-')}")
    print(f"Package name yang digunakan: {metadata.get('appId', APP_ID)}")
    return metadata


def fetch_reviews():
    """Mengambil ulasan Google Play secara bertahap menggunakan continuation token."""
    all_reviews = []
    continuation_token = None
    batch_number = 1

    while len(all_reviews) < TARGET_REVIEWS:
        remaining = TARGET_REVIEWS - len(all_reviews)
        batch_count = min(BATCH_SIZE, remaining)

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                batch, continuation_token = reviews(
                    APP_ID,
                    lang=LANGUAGE,
                    country=COUNTRY,
                    sort=Sort.NEWEST,
                    count=batch_count,
                    continuation_token=continuation_token,
                )
                break
            except Exception as exc:
                print(
                    f"Gagal mengambil batch {batch_number} "
                    f"(percobaan {attempt}/{MAX_RETRIES}): {exc}"
                )
                if attempt == MAX_RETRIES:
                    print("Pengambilan data dihentikan. Menyimpan data yang sudah terkumpul.")
                    return all_reviews
                sleep(REQUEST_DELAY_SECONDS * attempt)

        if not batch:
            if batch_number == 1:
                print("Batch pertama kosong. Kemungkinan penyebab:")
                print("- package name salah")
                print("- aplikasi tidak tersedia di region tersebut")
                print("- Google Play membatasi akses sementara")
                print("- tidak ada review yang bisa diambil oleh library")
            else:
                print("Tidak ada ulasan tambahan dari Google Play Store.")
            break

        all_reviews.extend(batch)
        print(f"Batch {batch_number}: total ulasan terkumpul = {len(all_reviews)}")
        batch_number += 1

        if continuation_token is None:
            print("Continuation token habis. Semua ulasan yang tersedia sudah diambil.")
            break

        sleep(REQUEST_DELAY_SECONDS)

    return all_reviews


def prepare_reviews(raw_reviews):
    """Menyesuaikan kolom, memfilter tahun, dan menghapus duplikasi review."""
    df = pd.DataFrame(raw_reviews)
    total_before_year_filter = len(df)

    if df.empty:
        empty_df = pd.DataFrame(columns=OUTPUT_COLUMNS)
        return empty_df, total_before_year_filter, 0, 0

    rename_columns = {
        "reviewId": "review_id",
        "content": "review",
        "score": "rating",
        "at": "review_date",
        "reviewCreatedVersion": "app_version",
        "thumbsUpCount": "thumbs_up_count",
    }
    df = df.rename(columns=rename_columns)

    for column in OUTPUT_COLUMNS:
        if column not in df.columns and column != "year":
            df[column] = pd.NA

    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
    df["year"] = df["review_date"].dt.year
    df["app_version"] = df["app_version"].fillna("")
    df["review"] = df["review"].fillna("")

    df = df[OUTPUT_COLUMNS]
    df = df[df["year"].between(START_YEAR, END_YEAR, inclusive="both")]
    total_after_year_filter = len(df)

    df = df.drop_duplicates(subset="review_id", keep="first")
    total_after_deduplication = len(df)
    df = df.sort_values("review_date", ascending=False).reset_index(drop=True)

    return (
        df,
        total_before_year_filter,
        total_after_year_filter,
        total_after_deduplication,
    )


def print_summary(
    df,
    total_before_year_filter,
    total_after_year_filter,
    total_after_deduplication,
):
    print("\nRingkasan Pengumpulan Data")
    print(f"Jumlah data sebelum filter tahun: {total_before_year_filter}")
    print(f"Jumlah data setelah filter tahun: {total_after_year_filter}")
    print(f"Jumlah data setelah hapus duplikasi: {total_after_deduplication}")

    print("\nDistribusi data per tahun:")
    if df.empty:
        print("Tidak ada data pada rentang tahun yang ditentukan.")
    else:
        print(df["year"].value_counts().sort_index())

    print("\n5 baris pertama:")
    print(df.head())


def main():
    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)

    print("Mulai pengumpulan data ulasan JakOne Mobile dari Google Play Store.")
    print(f"APP_ID: {APP_ID}")
    print(f"Target ulasan: {TARGET_REVIEWS}")
    print(f"Rentang tahun: {START_YEAR}-{END_YEAR}")

    metadata = validate_app_metadata()
    if metadata is None:
        return

    raw_reviews = fetch_reviews()
    (
        df_reviews,
        total_before_year_filter,
        total_after_year_filter,
        total_after_deduplication,
    ) = prepare_reviews(raw_reviews)

    df_reviews.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"\nData disimpan ke: {OUTPUT_PATH}")

    print_summary(
        df_reviews,
        total_before_year_filter,
        total_after_year_filter,
        total_after_deduplication,
    )


if __name__ == "__main__":
    main()
