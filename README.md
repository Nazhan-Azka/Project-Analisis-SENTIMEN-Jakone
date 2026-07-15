# Analisis Sentimen JakOne Mobile Menggunakan IndoBERT

## 1. Deskripsi Project

Project ini digunakan untuk menganalisis sentimen ulasan pengguna aplikasi JakOne Mobile dari Google Play Store menggunakan metode IndoBERT. Pipeline project mencakup pengumpulan data, preprocessing teks Bahasa Indonesia, pelabelan sentimen otomatis menggunakan InSet Lexicon, validasi manual sampel label, split dataset, fine-tuning IndoBERT, evaluasi model, serta visualisasi dan analisis hasil.

Project ini disusun untuk mendukung skripsi berjudul **Analisis Sentimen pada Aplikasi JakOne Mobile Menggunakan Metode IndoBERT**.

## 2. Tujuan Penelitian

Tujuan penelitian ini adalah:

- Mengumpulkan data ulasan pengguna aplikasi JakOne Mobile dari Google Play Store.
- Melakukan preprocessing teks Bahasa Indonesia.
- Memberi label sentimen menggunakan InSet Lexicon.
- Melakukan validasi manual terhadap sampel label otomatis.
- Melakukan fine-tuning IndoBERT untuk klasifikasi sentimen.
- Mengevaluasi performa model pada data test.
- Menganalisis isu dominan pada ulasan pengguna aplikasi JakOne Mobile.

## 3. Struktur Folder

```text
data/
  raw/
  processed/
  final/

src/
  01_collect_reviews.py
  02_preprocess_data.py
  03_download_lexicon.py
  03_check_lexicon.py
  04_labeling_inset.py
  06_split_dataset.py
  07_finetune_indobert.py
  08_evaluate_indobert.py
  09_visualization_analysis.py

notebooks/
  01_collect_reviews.ipynb
  02_preprocess_data.ipynb
  03_download_lexicon.ipynb
  03_check_lexicon.ipynb
  04_labeling_inset.ipynb
  06_split_dataset.ipynb
  07_finetune_indobert.ipynb
  08_evaluate_indobert.ipynb
  09_visualization_analysis.ipynb

outputs/
  evaluation/
    indobert_v3_baseline/
    v1/
  figures/
    indobert_v3_baseline/
    v1/

models/
  indobert_v3_baseline/

output_analisis/
  tabel_volume_keluhan_per_tahun.csv
  tabel_rata_rata_rating_per_tahun.csv
  tabel_kata_kunci_per_tahun.csv
  contoh_kutipan_per_tahun.csv
  ringkasan_narasi.txt
  HASIL_LENGKAP_UNTUK_REVIEW.txt

reports/
```

## 4. Alur Pipeline Penelitian

```text
Scraping ulasan Google Play Store
-> Preprocessing teks
-> Download dan validasi InSet Lexicon
-> Labeling sentimen InSet Lexicon
-> Validasi manual 100 sampel
-> Split dataset
-> Fine-tuning IndoBERT
-> Evaluasi model
-> Visualisasi dan analisis hasil
```

## 5. Dataset

Dataset final yang digunakan untuk pemodelan:

```text
data/final/06_jakone_modeling_master_v3.csv
data/final/v1/
```

Ringkasan dataset:

| Informasi        | Nilai                                    |
| ---------------- | ---------------------------------------- |
| Total data akhir | 14.172 ulasan                            |
| Sumber data      | Google Play Store aplikasi JakOne Mobile |
| Rentang tahun    | 2022-2026                                |

Kolom utama yang digunakan:

```text
clean_review
label
split_set
```

Distribusi label hasil InSet Lexicon:

| Label   | Jumlah data |
| ------- | ----------: |
| positif |       7.475 |
| negatif |       5.558 |
| netral  |       1.139 |

## 6. Preprocessing Teks

Preprocessing dilakukan untuk membersihkan teks ulasan sebelum labeling dan pemodelan. Tahap ini menghasilkan kolom `clean_review`.

Proses preprocessing mencakup:

- Case folding.
- Penghapusan URL, mention, emoji, dan simbol tidak penting.
- Normalisasi slang atau singkatan.
- Penghapusan stopword Bahasa Indonesia.
- Penghapusan review kosong.
- Penghapusan duplikasi.

Output tahap preprocessing:

```text
data/processed/jakone_reviews_clean.csv
```

## 7. Pelabelan Sentimen dengan InSet Lexicon

Pelabelan sentimen dilakukan otomatis menggunakan InSet Lexicon berdasarkan skor sentimen pada teks hasil preprocessing.

File lexicon:

```text
data/lexicon/positive.tsv
data/lexicon/negative.tsv
```

Aturan label:

| Skor sentimen | Label   |
| ------------- | ------- |
| skor > 0      | positif |
| skor < 0      | negatif |
| skor = 0      | netral  |

Output tahap labeling:

```text
data/processed/jakone_reviews_labeled.csv
data/processed/lexicon_validation_sample.csv
```

## 8. Validasi Manual Labeling

Validasi manual dilakukan untuk mengecek kualitas label otomatis InSet Lexicon pada 100 sampel audit. Validasi ini digunakan sebagai pengukuran kualitas label, bukan untuk mengubah seluruh dataset.

Ringkasan validasi manual:

| Metrik              | Nilai |
| ------------------- | ----: |
| Jumlah sampel audit |   100 |
| Label sesuai        |    80 |
| Label tidak sesuai  |    20 |
| Tingkat kesesuaian  |   80% |

## 9. Split Dataset

Dataset dibagi menjadi train, validation, dan test menggunakan stratified split agar proporsi label tetap seimbang pada setiap subset.

| Split      | Jumlah data |
| ---------- | ----------: |
| train      |      11.337 |
| validation |       1.417 |
| test       |       1.418 |

Output tahap split:

```text
data/final/06_jakone_modeling_master_v3.csv
outputs/audit/distribusi_split_v3.csv
```

## 10. Fine-Tuning IndoBERT



Model yang digunakan adalah `indobenchmark/indobert-base-p1` dengan arsitektur `BertForSequenceClassification`.

Konfigurasi training:

| Konfigurasi                 | Nilai                              |
| --------------------------- | ---------------------------------- |
| Model                       | indobenchmark/indobert-base-p1     |
| Arsitektur                  | BertForSequenceClassification      |
| Epoch maksimal              | 2                                  |
| Optimizer                   | AdamW default Hugging Face Trainer |
| Learning rate               | 2e-5                               |
| Batch size train            | 8                                  |
| Batch size validation/test  | 8                                  |
| Class weight                | tidak digunakan                    |
| Best epoch                  | 2                                  |
| Validation F1 macro terbaik | 0.868058                           |

Training IndoBERT disarankan dijalankan menggunakan GPU, misalnya Google Colab. Output model tersimpan di:

```text
models/indobert_v3_baseline/
```

Isi folder model:

```text
config.json
label_mapping.json
model.safetensors
tokenizer_config.json
tokenizer.json
```

## 11. Evaluasi Model

Evaluasi dilakukan pada data test saja, yaitu baris dengan `split_set == "test"`.

Ringkasan evaluasi test set:

| Metrik           |    Nilai |
| ---------------- | -------: |
| Jumlah data test |    1.418 |
| Accuracy         | 0.931594 |
| Macro F1         | 0.877363 |

Performa per kelas:

| Label   | Precision |   Recall | F1-score | Support |
| ------- | --------: | -------: | -------: | ------: |
| negatif |  0.878728 | 0.958785 | 0.917012 |     461 |
| netral  |  0.822917 | 0.692982 | 0.752381 |     114 |
| positif |  0.976801 | 0.948992 | 0.962696 |     843 |

Confusion matrix:

| Actual  | Predicted negatif | Predicted netral | Predicted positif |
| ------- | ----------------: | ---------------: | ----------------: |
| negatif |               442 |               10 |                 9 |
| netral  |                25 |               79 |                10 |
| positif |                36 |                7 |               800 |

Output evaluasi:

```text
outputs/evaluation/indobert_v3_baseline/classification_report.csv
outputs/evaluation/indobert_v3_baseline/confusion_matrix.csv
outputs/evaluation/indobert_v3_baseline/test_metrics.json
outputs/evaluation/indobert_v3_baseline/test_predictions.csv
outputs/evaluation/indobert_v3_baseline/final_analysis_summary_v3.txt
```

## 12. Visualisasi dan Analisis Hasil

Tahap ini membuat visualisasi distribusi data, kurva training, confusion matrix final, metrik per kelas, analisis salah prediksi, analisis keyword issue, word cloud, dan ringkasan analisis untuk Bab 4.

Ringkasan analisis akhir:

| Informasi                             | Nilai                               |
| ------------------------------------- | ----------------------------------- |
| Prediksi benar test                   | 1.321                               |
| Prediksi salah test                   | 97                                  |
| Kesalahan terbanyak                   | positif -> negatif sebanyak 36 data |
| Keyword paling dominan                | transaksi dengan 1.881 kemunculan   |
| Keyword dominan pada sentimen negatif | transfer dengan 924 kemunculan      |
| Kelas performa terbaik                | positif                             |
| Kelas performa terlemah               | netral                              |

Interpretasi singkat:

- Model IndoBERT sudah cukup baik secara keseluruhan.
- Kelas positif dan negatif memiliki performa tinggi.
- Kelas netral masih menjadi kelemahan utama.
- Kemungkinan penyebab kelemahan kelas netral adalah jumlah data netral yang sedikit, teks netral lebih ambigu, dan noise dari labeling lexicon.

### Analisis Tambahan Tren Keluhan 2022-2024

Selain evaluasi model IndoBERT, project ini juga dilengkapi analisis deskriptif khusus untuk melihat tren volume keluhan pengguna JakOne Mobile pada periode 2022-2024. Analisis ini menggunakan dataset:

```text
docs/Analisis Latar Belakang/jakone_reviews_2022_2024.csv
```

Analisis tambahan mencakup:

- Jumlah review per tahun.
- Jumlah dan persentase review rating 1-2 sebagai kategori keluhan.
- Jumlah dan persentase review rating 4-5 sebagai pembanding kategori puas.
- Rata-rata dan median rating per tahun.
- Kata kunci keluhan rating 1-2 yang paling sering muncul per tahun.
- Contoh kutipan ilustratif rating 1 per tahun tanpa menampilkan `userName` dan `reviewId`.
- Grafik tren keluhan, tren rata-rata rating, dan kata kunci dominan.

Ringkasan hasil analisis keluhan:

| Tahun | Total review | Rating 1-2 | Persen rating 1-2 | Rating 4-5 | Persen rating 4-5 | Rata-rata rating |
| ----- | -----------: | ---------: | ----------------: | ---------: | ----------------: | ---------------: |
| 2022  |        3.467 |        320 |             9,23% |      3.069 |            88,52% |            4,589 |
| 2023  |        4.358 |      1.778 |            40,80% |      2.315 |            53,12% |            3,280 |
| 2024  |        2.785 |        864 |            31,02% |      1.790 |            64,27% |            3,692 |

Temuan utama:

- Persentase keluhan rating 1-2 meningkat dari 9,23% pada 2022 menjadi 31,02% pada 2024.
- Puncak proporsi keluhan terjadi pada 2023, yaitu 40,80% dari total review tahun tersebut.
- Rata-rata rating turun dari 4,589 pada 2022 menjadi 3,692 pada 2024, meskipun sempat membaik dari 2023 ke 2024.
- Kata kunci keluhan yang konsisten muncul meliputi `tidak`, `mau`, `masuk`, `malah`, `padahal`, `update`, `tapi`, `buka`, `lama`, `terus`, `login`, dan `otp`.
- Pada 2024, kata `saldo` masuk sebagai salah satu kata kunci dominan, sehingga dapat menjadi perhatian dalam pembahasan isu layanan/transaksi.

Output analisis tambahan tersimpan di:

```text
output_analisis/tabel_volume_keluhan_per_tahun.csv
output_analisis/tabel_rata_rata_rating_per_tahun.csv
output_analisis/tabel_kata_kunci_per_tahun.csv
output_analisis/contoh_kutipan_per_tahun.csv
output_analisis/ringkasan_narasi.txt
output_analisis/HASIL_LENGKAP_UNTUK_REVIEW.txt
output_analisis/grafik_volume_keluhan_per_tahun.png
output_analisis/grafik_tren_rata_rata_rating.png
output_analisis/grafik_kata_kunci_2022.png
output_analisis/grafik_kata_kunci_2023.png
output_analisis/grafik_kata_kunci_2024.png
```

Script yang digunakan:

```text
analisis_jakone_reviews.py
gabungkan_hasil_review.py
```

## 13. Cara Menjalankan Project

Install dependensi:

```bash
pip install -r requirements.txt
```

Jalankan pipeline:

```bash
python src/01_collect_reviews.py
python src/02_preprocess_data.py
python src/03_download_lexicon.py
python src/03_check_lexicon.py
python src/04_labeling_inset.py
python src/05_analyze_manual_validation.py
python src/06_split_dataset.py
python src/07_finetune_indobert.py
python src/08_evaluate_indobert.py
python src/09_visualization_analysis.py
```

Jalankan analisis tambahan tren keluhan 2022-2024:

```bash
python analisis_jakone_reviews.py
python gabungkan_hasil_review.py
```

Catatan:

- Jika dataset dan model sudah tersedia, tidak perlu menjalankan semua tahap dari awal.
- Fine-tuning IndoBERT sebaiknya dijalankan di GPU.
- Evaluasi model juga lebih cepat jika dijalankan di GPU.
- Output model v3 tersimpan di `models/indobert_v3_baseline/`.
- Artefak eksperimen lama disimpan sebagai arsip di folder `v1`.
- Pada workspace ini, file referensi `outputs/evaluation/manual_validation_summary.txt` dan `outputs/evaluation/manual_validation_summary.csv` tidak tersedia, sehingga ringkasan validasi manual ditulis berdasarkan hasil audit manual yang sudah diberikan.

## 14. Output Penting

```text
data/raw/jakone_reviews_raw.csv
data/processed/jakone_reviews_clean.csv
data/processed/jakone_reviews_labeled.csv
data/processed/lexicon_validation_sample.csv
data/final/06_jakone_modeling_master_v3.csv

models/indobert_v3_baseline/
outputs/modeling/indobert_v3_baseline/training_log.json
outputs/evaluation/indobert_v3_baseline/classification_report.csv
outputs/evaluation/indobert_v3_baseline/confusion_matrix.csv
outputs/evaluation/indobert_v3_baseline/test_metrics.json
outputs/evaluation/indobert_v3_baseline/test_predictions.csv
outputs/evaluation/indobert_v3_baseline/final_analysis_summary_v3.txt
outputs/analysis/indobert_v3_baseline/keyword_issue_summary_v3.csv
outputs/analysis/indobert_v3_baseline/keyword_issue_by_label_v3.csv
outputs/figures/indobert_v3_baseline/confusion_matrix_v3.png
outputs/figures/indobert_v3_baseline/wordcloud_*.png
outputs/evaluation/v1/
outputs/figures/v1/
data/final/v1/

output_analisis/tabel_volume_keluhan_per_tahun.csv
output_analisis/tabel_rata_rata_rating_per_tahun.csv
output_analisis/tabel_kata_kunci_per_tahun.csv
output_analisis/contoh_kutipan_per_tahun.csv
output_analisis/ringkasan_narasi.txt
output_analisis/HASIL_LENGKAP_UNTUK_REVIEW.txt
output_analisis/*.png
```

## Dashboard Streamlit

Dashboard Streamlit tersedia untuk menampilkan hasil penelitian dan menjalankan demo prediksi sentimen menggunakan model IndoBERT yang sudah dilatih.

Jalankan dashboard dengan command:

```bash
streamlit run dashboard/app.py
```

Dashboard menampilkan:

- Overview hasil penelitian.
- Dataset dan distribusi label, tahun, rating, serta split dataset.
- Proses labeling sentimen dengan InSet Lexicon.
- Hasil training IndoBERT.
- Evaluasi model pada data test.
- Analisis kesalahan prediksi.
- Keyword issue dan word cloud.
- Demo prediksi sentimen ulasan baru.

Dashboard hanya membaca dataset, model, dan output pipeline yang sudah tersedia. Dashboard tidak melakukan training ulang, evaluasi ulang, scraping ulang, preprocessing ulang, labeling ulang, atau split ulang.

## 15. Catatan Keterbatasan

- Label awal dibuat otomatis menggunakan InSet Lexicon sehingga masih memungkinkan terdapat noise.
- Hasil audit manual pada 100 sampel menunjukkan tingkat kesesuaian sebesar 80%.
- Kelas netral memiliki jumlah data paling sedikit sehingga performanya lebih rendah dibanding kelas positif dan negatif.
- Pendekatan lexicon-based tidak selalu mampu memahami konteks, typo, sarkasme, atau istilah domain mobile banking.
- Model IndoBERT menunjukkan performa baik secara umum, tetapi kelas netral masih menjadi kelemahan utama.

## 16. Kaitan dengan Penulisan Skripsi

Bagian pengumpulan data, preprocessing, labeling InSet Lexicon, validasi manual, split dataset, dan fine-tuning IndoBERT dapat digunakan sebagai bahan penulisan **Bab 3 Metodologi Penelitian**.

Bagian hasil training, evaluasi test, confusion matrix, visualisasi, analisis salah prediksi, dan analisis keyword issue dapat digunakan sebagai bahan penulisan **Bab 4 Hasil dan Pembahasan**.
