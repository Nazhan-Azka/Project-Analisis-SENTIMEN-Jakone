from pathlib import Path
import re
import sys

import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


INPUT_PATH = "data/raw/jakone_reviews_raw.csv"
OUTPUT_PATH = "data/processed/jakone_reviews_clean.csv"

INPUT_COLUMNS = [
    "review_id",
    "review",
    "rating",
    "review_date",
    "app_version",
    "thumbs_up_count",
    "year",
]

OUTPUT_COLUMNS = [
    "review_id",
    "review",
    "clean_review",
    "rating",
    "review_date",
    "app_version",
    "thumbs_up_count",
    "year",
]

SLANG_DICT = {
    "gk": "tidak",
    "g": "tidak",
    "ga": "tidak",
    "gak": "tidak",
    "nggak": "tidak",
    "tdk": "tidak",
    "jgn": "jangan",
    "bgt": "banget",
    "bangettt": "banget",
    "bgtu": "begitu",
    "yg": "yang",
    "dgn": "dengan",
    "utk": "untuk",
    "dr": "dari",
    "krn": "karena",
    "karna": "karena",
    "mlh": "malah",
    "tp": "tapi",
    "tpi": "tapi",
    "jd": "jadi",
    "aja": "saja",
    "sm": "sama",
    "sdh": "sudah",
    "udh": "sudah",
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
    "dtang": "datang",
}

PROTECTED_WORDS = {
    "tidak",
    "gagal",
    "belum",
    "jangan",
    "kurang",
    "otp",
    "login",
    "pin",
    "akun",
    "transfer",
    "transaksi",
    "error",
    "saldo",
    "verifikasi",
    "password",
    "rekening",
    "bank",
    "aplikasi",
    "jakone",
    "mobile",
}

BASE_STOPWORDS = {
    "ada",
    "adalah",
    "adanya",
    "agar",
    "akan",
    "akhir",
    "aku",
    "anda",
    "antara",
    "apa",
    "apabila",
    "atau",
    "awal",
    "bagai",
    "bagaimana",
    "bagi",
    "bagian",
    "bahwa",
    "baik",
    "bakal",
    "banyak",
    "baru",
    "begini",
    "begitu",
    "berapa",
    "berbagai",
    "berikut",
    "bersama",
    "berturut",
    "besar",
    "betul",
    "biasa",
    "bila",
    "buat",
    "cara",
    "cukup",
    "cuma",
    "dalam",
    "dan",
    "dapat",
    "dari",
    "daripada",
    "datang",
    "dekat",
    "demi",
    "demikian",
    "dengan",
    "depan",
    "dia",
    "di",
    "diri",
    "dong",
    "dua",
    "dulu",
    "guna",
    "hal",
    "hampir",
    "hanya",
    "harus",
    "hingga",
    "ia",
    "ini",
    "itu",
    "jadi",
    "jika",
    "juga",
    "justru",
    "kala",
    "kalau",
    "kali",
    "kami",
    "kamu",
    "kan",
    "karena",
    "kata",
    "ke",
    "kecil",
    "kembali",
    "kemudian",
    "kepada",
    "ketika",
    "khusus",
    "kini",
    "lagi",
    "lah",
    "lain",
    "lalu",
    "lama",
    "lewat",
    "lima",
    "luar",
    "macam",
    "maka",
    "makin",
    "malah",
    "mampu",
    "mana",
    "masih",
    "masing",
    "mau",
    "maupun",
    "melalui",
    "memang",
    "mereka",
    "meski",
    "mungkin",
    "namun",
    "nanti",
    "oleh",
    "pada",
    "paling",
    "para",
    "per",
    "perlu",
    "pernah",
    "pula",
    "pun",
    "saat",
    "saja",
    "saling",
    "sama",
    "sambil",
    "sampai",
    "sana",
    "sangat",
    "satu",
    "saya",
    "sebab",
    "sebagai",
    "sebagian",
    "sebaik",
    "sebaiknya",
    "sebelum",
    "sebuah",
    "tersebut",
    "sedang",
    "sedikit",
    "segala",
    "sejak",
    "sejenak",
    "sekali",
    "sekalian",
    "sekarang",
    "sekitar",
    "selain",
    "selaku",
    "selalu",
    "seluruh",
    "semakin",
    "sementara",
    "sempat",
    "semua",
    "semula",
    "sendiri",
    "seolah",
    "seperti",
    "sering",
    "serta",
    "siapa",
    "sini",
    "situ",
    "suatu",
    "sudah",
    "supaya",
    "tadi",
    "tanpa",
    "tanya",
    "tapi",
    "telah",
    "tempat",
    "tengah",
    "tentang",
    "tentu",
    "terakhir",
    "terasa",
    "terdapat",
    "terjadi",
    "terlalu",
    "terlihat",
    "terus",
    "tetap",
    "tetapi",
    "tiap",
    "tiga",
    "toh",
    "untuk",
    "usah",
    "usai",
    "waduh",
    "wah",
    "wahai",
    "waktu",
    "walau",
    "yaitu",
    "yakni",
    "yang",
}

STOPWORDS = BASE_STOPWORDS - PROTECTED_WORDS

URL_PATTERN = re.compile(r"https?://\S+|www\.\S+")
MENTION_PATTERN = re.compile(r"@\w+")
HASHTAG_PATTERN = re.compile(r"#(\w+)")
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE,
)
NON_ALNUM_SPACE_PATTERN = re.compile(r"[^a-z0-9\s]")
SPACE_PATTERN = re.compile(r"\s+")


def clean_text(text):
    """Membersihkan satu teks ulasan Bahasa Indonesia."""
    if pd.isna(text):
        return ""

    text = str(text).lower()
    text = URL_PATTERN.sub(" ", text)
    text = MENTION_PATTERN.sub(" ", text)
    text = HASHTAG_PATTERN.sub(r"\1", text)
    text = EMOJI_PATTERN.sub(" ", text)
    text = NON_ALNUM_SPACE_PATTERN.sub(" ", text)
    text = SPACE_PATTERN.sub(" ", text).strip()

    words = [SLANG_DICT.get(word, word) for word in text.split()]
    words = [word for word in words if word not in STOPWORDS]
    return SPACE_PATTERN.sub(" ", " ".join(words)).strip()


def validate_input_file():
    input_file = Path(INPUT_PATH)
    if not input_file.exists():
        raise FileNotFoundError(f"File input tidak ditemukan: {INPUT_PATH}")
    return input_file


def validate_columns(df):
    missing_columns = [column for column in INPUT_COLUMNS if column not in df.columns]
    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"Kolom input tidak lengkap. Kolom yang hilang: {missing_text}")


def remove_empty_reviews(df):
    df = df.copy()
    df["review"] = df["review"].fillna("").astype(str)
    return df[df["review"].str.strip() != ""].copy()


def remove_duplicate_reviews(df):
    df = df.copy().reset_index(drop=True)
    df["_row_order"] = range(len(df))
    review_id_text = df["review_id"].fillna("").astype(str).str.strip()

    df_with_id = df[review_id_text != ""].drop_duplicates(subset="review_id", keep="first")
    df_without_id = df[review_id_text == ""].drop_duplicates(subset="review", keep="first")

    df = pd.concat([df_with_id, df_without_id], ignore_index=True)
    df = df.sort_values("_row_order").drop(columns="_row_order").reset_index(drop=True)
    return df


def preprocess_reviews(df):
    total_initial = len(df)

    df = remove_empty_reviews(df)
    total_after_empty_review = len(df)

    df = remove_duplicate_reviews(df)
    total_after_deduplication = len(df)

    df["clean_review"] = df["review"].apply(clean_text)
    df = df[df["clean_review"].str.strip() != ""].copy()
    total_after_preprocessing = len(df)

    df = df[OUTPUT_COLUMNS].reset_index(drop=True)
    return (
        df,
        total_initial,
        total_after_empty_review,
        total_after_deduplication,
        total_after_preprocessing,
    )


def print_summary(
    df,
    total_initial,
    total_after_empty_review,
    total_after_deduplication,
    total_after_preprocessing,
):
    print("\nRingkasan Preprocessing Data")
    print(f"Jumlah data awal: {total_initial}")
    print(f"Jumlah data setelah hapus review kosong: {total_after_empty_review}")
    print(f"Jumlah data setelah hapus duplikasi: {total_after_deduplication}")
    print(f"Jumlah data setelah preprocessing: {total_after_preprocessing}")

    print("\nContoh 10 data sebelum dan sesudah preprocessing:")
    examples = df[["review", "clean_review"]].head(10)
    print(examples.to_string(index=False))


def main():
    input_file = validate_input_file()
    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)

    print("Mulai preprocessing teks ulasan JakOne Mobile.")
    print(f"Input: {INPUT_PATH}")
    print(f"Output: {OUTPUT_PATH}")

    df_raw = pd.read_csv(input_file)
    validate_columns(df_raw)

    (
        df_clean,
        total_initial,
        total_after_empty_review,
        total_after_deduplication,
        total_after_preprocessing,
    ) = preprocess_reviews(df_raw)

    df_clean.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"\nData hasil preprocessing disimpan ke: {OUTPUT_PATH}")

    print_summary(
        df_clean,
        total_initial,
        total_after_empty_review,
        total_after_deduplication,
        total_after_preprocessing,
    )


if __name__ == "__main__":
    main()
