import logging
from pathlib import Path

import numpy as np
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
LEXICON_DIR = ROOT_DIR / "data" / "lexicon"
AUDIT_DIR = ROOT_DIR / "outputs" / "audit"

POSITIVE_PATH = LEXICON_DIR / "positive.tsv"
NEGATIVE_PATH = LEXICON_DIR / "negative.tsv"

POSITIVE_CLEANED_PATH = LEXICON_DIR / "positive_cleaned.tsv"
NEGATIVE_CLEANED_PATH = LEXICON_DIR / "negative_cleaned.tsv"
CUSTOM_POSITIVE_PATH = LEXICON_DIR / "custom_positive.tsv"
CUSTOM_NEGATIVE_PATH = LEXICON_DIR / "custom_negative.tsv"
FINAL_POSITIVE_PATH = LEXICON_DIR / "lexicon_final_positive.tsv"
FINAL_NEGATIVE_PATH = LEXICON_DIR / "lexicon_final_negative.tsv"
REPORT_PATH = AUDIT_DIR / "lexicon_revision_report.txt"


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


NEGATIVE_REMOVE_TERMS = {
    "aplikasi", "data", "daftar", "informasi", "lengkap", "cepat", "buka",
    "belanja", "cari", "bagus", "enak", "mudah", "gampang", "lancar",
    "membantu", "menarik", "suka", "bayar", "beli", "tambah", "lebih",
    "biar", "mohon", "kasih", "fresh", "standar", "pulsa", "bulan",
    "terkait", "pihak", "ikut", "entah", "potongan", "nemu", "bangett",
    "mager", "kayak", "lumayan", "mata", "coba", "usaha", "transaksi",
    "respon", "akses", "promo", "proses", "lekas", "balas", "kaya",
    "tangan", "campur",
}

POSITIVE_REMOVE_TERMS = {
    "mulu", "kebanyakan", "suntuk", "hilang", "melelahkan", "nasabah",
    "paket", "terbaru", "perubahan", "menurut", "andil", "amat", "punya",
    "ayo", "wkwkwk", "deposito", "tinggal", "rumah", "terdekat", "buka",
    "lekas", "balas", "campur", "tangan", "entah", "kaya", "ikut", "pihak",
    "terkait",
}

KEEP_POSITIVE_ONLY = {
    "mudah", "enak", "gampang", "lancar", "suka", "ramah", "membantu",
    "memuaskan", "bagus", "menarik", "lengkap", "cepat", "kasih", "nyaman",
    "mantap", "berguna", "bermanfaat", "praktis", "simpel", "terbaik",
    "sukses", "senang", "gembira", "tangguh", "andal", "energik",
}

KEEP_NEGATIVE_ONLY = {
    "gagal", "error", "masalah", "ribet", "salah", "hilang", "susah",
    "lambat", "kekurangan", "buruk", "jelek", "parah", "lemah",
    "menyusahkan",
}

REMOVE_FROM_BOTH = {
    "bayar", "beli", "buka", "daftar", "biar", "mohon", "lebih", "tambah",
    "fresh", "lekas", "balas", "campur", "tangan", "proses", "akses",
}

CUSTOM_POSITIVE = [
    ("recommended", 4),
    ("rekomen", 4),
    ("rekomend", 4),
    ("keren", 4),
    ("mantapppp", 5),
    ("mantap banget", 5),
    ("bagud", 3),
    ("baguss", 3),
    ("bagus banget", 4),
    ("userfriendly", 4),
    ("user friendly", 4),
    ("kece", 3),
    ("canggih", 4),
    ("oke banget", 4),
    ("top banget", 5),
    ("worth it", 4),
    ("helpful", 4),
    ("good", 4),
    ("best", 4),
    ("simple", 3),
    ("jempolan", 4),
    ("sempurna", 5),
    ("luar biasa", 5),
    ("memudahkan", 4),
    ("mempermudah", 4),
    ("responsif", 4),
    ("cepat banget", 4),
    ("mudah banget", 4),
    ("lengkap banget", 4),
    ("aman", 3),
    ("terpercaya", 4),
    ("andalan", 4),
    ("favorit", 3),
    ("sip", 3),
    ("sipp", 3),
    ("sippp", 3),
    ("oke", 3),
    ("okelah", 3),
    ("mantul", 4),
    ("gokil", 3),
    ("keren banget", 5),
    ("asik", 3),
    ("asikk", 3),
    ("nyaman banget", 4),
    ("lancar banget", 4),
    ("yeay", 3),
    ("yeesss", 3),
    ("alhamdulillah", 3),
    ("terima kasih jakone", 4),
    ("puas", 4),
    ("memuaskan banget", 5),
]

CUSTOM_NEGATIVE = [
    ("maintenance", -4),
    ("gangguan", -4),
    ("gagal login", -5),
    ("login gagal", -5),
    ("otp gagal", -5),
    ("gagal otp", -5),
    ("ngebug", -4),
    ("bug", -3),
    ("glitch", -4),
    ("dipersulit", -4),
    ("ga bisa", -3),
    ("gak bisa", -3),
    ("tidak bisa login", -5),
    ("susah banget", -4),
    ("lambat banget", -4),
    ("lemot banget", -4),
    ("eror terus", -5),
    ("error terus", -5),
    ("sering crash", -5),
    ("force close", -5),
    ("server down", -5),
    ("loading lama", -3),
    ("tidak responsif", -4),
    ("tidak bisa", -3),
    ("gabisa", -3),
    ("gaboleh", -3),
    ("ribet banget", -4),
    ("susah digunakan", -4),
    ("tidak jelas", -3),
    ("tidak berguna", -4),
    ("tidak membantu", -4),
    ("mengecewakan", -4),
    ("kecewa", -4),
    ("kecewaa", -4),
    ("kecewaaa", -4),
    ("buruk banget", -5),
    ("jelek banget", -5),
    ("parah banget", -5),
    ("menyebalkan", -4),
    ("menyebalkan banget", -5),
    ("tidak aman", -5),
    ("data hilang", -5),
    ("saldo hilang", -5),
    ("uang hilang", -5),
    ("ditipu", -5),
    ("penipuan", -5),
    ("lama banget", -4),
    ("lambat sekali", -4),
    ("tidak update", -3),
    ("banyak bug", -4),
    ("banyak gangguan", -5),
    ("sering gangguan", -5),
    ("tidak stabil", -4),
    ("aplikasi crash", -5),
    ("tidak bisa transfer", -5),
    ("transfer gagal", -5),
    ("verifikasi gagal", -4),
    ("wajah tidak terdeteksi", -4),
]


def read_lexicon(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t")
    df["word"] = df["word"].astype(str).str.strip().str.lower()
    df["weight"] = pd.to_numeric(df["weight"], errors="raise")
    return df.dropna(subset=["word"]).loc[lambda x: x["word"] != ""].copy()


def write_lexicon(df: pd.DataFrame, path: Path) -> None:
    output = df[["word", "weight"]].copy()
    output.to_csv(path, sep="\t", index=False)
    logger.info("Wrote %s (%s rows)", path.relative_to(ROOT_DIR), len(output))


def remove_terms(df: pd.DataFrame, terms: set[str]) -> tuple[pd.DataFrame, int]:
    mask = df["word"].isin(terms)
    return df.loc[~mask].copy(), int(mask.sum())


def deduplicate_by_dominance(df: pd.DataFrame) -> pd.DataFrame:
    ranked = df.assign(_abs_weight=df["weight"].abs())
    ranked = ranked.sort_values(["word", "_abs_weight", "weight"], ascending=[True, False, False])
    return ranked.drop_duplicates("word", keep="first").drop(columns="_abs_weight").reset_index(drop=True)


def resolve_final_conflicts(pos_df: pd.DataFrame, neg_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, int]:
    pos_unique = deduplicate_by_dominance(pos_df)
    neg_unique = deduplicate_by_dominance(neg_df)

    pos_map = pos_unique.set_index("word")["weight"].to_dict()
    neg_map = neg_unique.set_index("word")["weight"].to_dict()
    shared_words = sorted(set(pos_map) & set(neg_map))

    for word in shared_words:
        pos_weight = pos_map[word]
        neg_weight = neg_map[word]
        if abs(pos_weight) >= abs(neg_weight):
            neg_map.pop(word)
        else:
            pos_map.pop(word)

    final_pos = pd.DataFrame(sorted(pos_map.items()), columns=["word", "weight"])
    final_neg = pd.DataFrame(sorted(neg_map.items()), columns=["word", "weight"])
    return final_pos, final_neg, len(shared_words)


def normalize_weight(df: pd.DataFrame) -> pd.DataFrame:
    normalized = df.copy()
    normalized["weight"] = np.round(normalized["weight"].astype(float) / 5.0, 4)
    return normalized


def main() -> None:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    positive = read_lexicon(POSITIVE_PATH)
    negative = read_lexicon(NEGATIVE_PATH)
    positive_before = len(positive)
    negative_before = len(negative)

    all_ambiguous_terms = KEEP_POSITIVE_ONLY | KEEP_NEGATIVE_ONLY | REMOVE_FROM_BOTH
    ambiguous_in_both_before = (set(positive["word"]) & set(negative["word"]) & all_ambiguous_terms)

    negative_cleaned, negative_removed_initial = remove_terms(negative, NEGATIVE_REMOVE_TERMS)
    positive_cleaned, positive_removed_initial = remove_terms(positive, POSITIVE_REMOVE_TERMS)

    negative_cleaned, negative_removed_keep_positive = remove_terms(negative_cleaned, KEEP_POSITIVE_ONLY)
    positive_cleaned, positive_removed_keep_negative = remove_terms(positive_cleaned, KEEP_NEGATIVE_ONLY)

    negative_cleaned, negative_removed_context = remove_terms(negative_cleaned, REMOVE_FROM_BOTH)
    positive_cleaned, positive_removed_context = remove_terms(positive_cleaned, REMOVE_FROM_BOTH)

    negative_removed_total = (
        negative_removed_initial + negative_removed_keep_positive + negative_removed_context
    )
    positive_removed_total = (
        positive_removed_initial + positive_removed_keep_negative + positive_removed_context
    )

    write_lexicon(positive_cleaned, POSITIVE_CLEANED_PATH)
    write_lexicon(negative_cleaned, NEGATIVE_CLEANED_PATH)

    custom_positive = pd.DataFrame(CUSTOM_POSITIVE, columns=["word", "weight"])
    custom_negative = pd.DataFrame(CUSTOM_NEGATIVE, columns=["word", "weight"])
    write_lexicon(custom_positive, CUSTOM_POSITIVE_PATH)
    write_lexicon(custom_negative, CUSTOM_NEGATIVE_PATH)

    combined_positive = pd.concat([positive_cleaned, custom_positive], ignore_index=True)
    combined_negative = pd.concat([negative_cleaned, custom_negative], ignore_index=True)
    final_positive, final_negative, final_conflicts_resolved = resolve_final_conflicts(
        combined_positive, combined_negative
    )

    write_lexicon(normalize_weight(final_positive), FINAL_POSITIVE_PATH)
    write_lexicon(normalize_weight(final_negative), FINAL_NEGATIVE_PATH)

    custom_added_total = len(custom_positive) + len(custom_negative)
    ambiguous_resolved_total = len(ambiguous_in_both_before)

    report = "\n".join(
        [
            "Laporan Revisi Lexicon InSet + Custom Domain JakOne Mobile",
            "Judul: Analisis Sentimen pada Aplikasi JakOne Mobile Menggunakan Metode IndoBERT",
            "",
            "Ringkasan jumlah kata:",
            f"- Positif sebelum revisi: {positive_before}",
            f"- Positif sesudah cleaning: {len(positive_cleaned)}",
            f"- Positif final sesudah custom, deduplikasi, konflik, normalisasi: {len(final_positive)}",
            f"- Negatif sebelum revisi: {negative_before}",
            f"- Negatif sesudah cleaning: {len(negative_cleaned)}",
            f"- Negatif final sesudah custom, deduplikasi, konflik, normalisasi: {len(final_negative)}",
            "",
            "Penghapusan kata:",
            f"- Kata positif yang dihapus: {positive_removed_total}",
            f"- Kata negatif yang dihapus: {negative_removed_total}",
            "",
            "Custom lexicon:",
            f"- Custom positif ditambahkan: {len(custom_positive)}",
            f"- Custom negatif ditambahkan: {len(custom_negative)}",
            f"- Total custom ditambahkan: {custom_added_total}",
            "",
            "Penyelesaian kata ambigu:",
            f"- Kata ambigu dari daftar audit yang ditemukan di kedua lexicon awal: {ambiguous_resolved_total}",
            f"- Konflik kata positif-negatif yang diselesaikan saat final merge: {final_conflicts_resolved}",
            "",
            "Output:",
            f"- {POSITIVE_CLEANED_PATH.relative_to(ROOT_DIR)}",
            f"- {NEGATIVE_CLEANED_PATH.relative_to(ROOT_DIR)}",
            f"- {CUSTOM_POSITIVE_PATH.relative_to(ROOT_DIR)}",
            f"- {CUSTOM_NEGATIVE_PATH.relative_to(ROOT_DIR)}",
            f"- {FINAL_POSITIVE_PATH.relative_to(ROOT_DIR)}",
            f"- {FINAL_NEGATIVE_PATH.relative_to(ROOT_DIR)}",
        ]
    )
    REPORT_PATH.write_text(report + "\n", encoding="utf-8")
    logger.info("Wrote %s", REPORT_PATH.relative_to(ROOT_DIR))

    print("Ringkasan revisi lexicon")
    print(f"Negatif: dihapus {negative_removed_total}, tersisa {len(negative_cleaned)}")
    print(f"Positif: dihapus {positive_removed_total}, tersisa {len(positive_cleaned)}")
    print(f"Total kata positif final: {len(final_positive)}")
    print(f"Total kata negatif final: {len(final_negative)}")
    print(f"Laporan: {REPORT_PATH.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
