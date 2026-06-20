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
  figures/
  model_indobert_jakone/

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
data/final/jakone_modeling_master.csv
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
data/final/jakone_modeling_master.csv
outputs/evaluation/split_distribution_summary.csv
```

## 10. Fine-Tuning IndoBERT

Model yang digunakan adalah `indobenchmark/indobert-base-p2` dengan arsitektur `BertForSequenceClassification`.

Konfigurasi training:

| Konfigurasi                 | Nilai                           |
| --------------------------- | ------------------------------- |
| Model                       | indobenchmark/indobert-base-p2  |
| Arsitektur                  | BertForSequenceClassification   |
| Epoch maksimal              | 5                               |
| Optimizer                   | AdamW                           |
| Learning rate               | 2e-5                            |
| Batch size train            | 16                              |
| Batch size validation/test  | 32                              |
| Class weight                | digunakan                       |
| Early stopping              | berdasarkan validation F1 macro |
| Best epoch                  | 5                               |
| Validation F1 macro terbaik | 0.848772                        |

Training IndoBERT disarankan dijalankan menggunakan GPU, misalnya Google Colab. Output model tersimpan di:

```text
outputs/model_indobert_jakone/
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
| Accuracy         | 0.894922 |
| Macro F1         | 0.819212 |

Performa per kelas:

| Label   | Precision |   Recall | F1-score | Support |
| ------- | --------: | -------: | -------: | ------: |
| negatif |  0.900178 | 0.908273 | 0.904208 |     556 |
| netral  |  0.636364 | 0.614035 | 0.625000 |     114 |
| positif |  0.929050 | 0.927807 | 0.928428 |     748 |

Confusion matrix:

| Actual  | Predicted negatif | Predicted netral | Predicted positif |
| ------- | ----------------: | ---------------: | ----------------: |
| negatif |               505 |               16 |                35 |
| netral  |                26 |               70 |                18 |
| positif |                30 |               24 |               694 |

Output evaluasi:

```text
outputs/evaluation/test_classification_report.txt
outputs/evaluation/test_classification_report.csv
outputs/evaluation/test_confusion_matrix.csv
outputs/evaluation/test_metrics_summary.json
outputs/evaluation/test_predictions.csv
```

## 12. Visualisasi dan Analisis Hasil

Tahap ini membuat visualisasi distribusi data, kurva training, confusion matrix final, metrik per kelas, analisis salah prediksi, analisis keyword issue, word cloud, dan ringkasan analisis untuk Bab 4.

Ringkasan analisis akhir:

| Informasi                             | Nilai                               |
| ------------------------------------- | ----------------------------------- |
| Prediksi benar test                   | 1.269                               |
| Prediksi salah test                   | 149                                 |
| Kesalahan terbanyak                   | negatif -> positif sebanyak 35 data |
| Keyword paling dominan                | transaksi dengan 1.881 kemunculan   |
| Keyword dominan pada sentimen negatif | transfer dengan 961 kemunculan      |
| Kelas performa terbaik                | positif                             |
| Kelas performa terlemah               | netral                              |

Interpretasi singkat:

- Model IndoBERT sudah cukup baik secara keseluruhan.
- Kelas positif dan negatif memiliki performa tinggi.
- Kelas netral masih menjadi kelemahan utama.
- Kemungkinan penyebab kelemahan kelas netral adalah jumlah data netral yang sedikit, teks netral lebih ambigu, dan noise dari labeling lexicon.

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

Catatan:

- Jika dataset dan model sudah tersedia, tidak perlu menjalankan semua tahap dari awal.
- Fine-tuning IndoBERT sebaiknya dijalankan di GPU.
- Evaluasi model juga lebih cepat jika dijalankan di GPU.
- Output model tersimpan di `outputs/model_indobert_jakone/`.
- Pada workspace ini, file referensi `outputs/evaluation/manual_validation_summary.txt` dan `outputs/evaluation/manual_validation_summary.csv` tidak tersedia, sehingga ringkasan validasi manual ditulis berdasarkan hasil audit manual yang sudah diberikan.

## 14. Output Penting

```text
data/raw/jakone_reviews_raw.csv
data/processed/jakone_reviews_clean.csv
data/processed/jakone_reviews_labeled.csv
data/processed/lexicon_validation_sample.csv
data/final/jakone_modeling_master.csv

outputs/model_indobert_jakone/
outputs/evaluation/training_log.csv
outputs/evaluation/test_classification_report.txt
outputs/evaluation/test_classification_report.csv
outputs/evaluation/test_confusion_matrix.csv
outputs/evaluation/test_metrics_summary.json
outputs/evaluation/test_predictions.csv
outputs/evaluation/final_analysis_summary.txt
outputs/evaluation/misclassified_predictions.csv
outputs/evaluation/keyword_issue_summary.csv
outputs/evaluation/keyword_issue_by_label.csv
outputs/figures/
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
