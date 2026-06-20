# Checklist Gap Struktur BAB 2

Dokumen ini membandingkan struktur BAB 2 rencana dengan isi BAB 2 hasil ekstraksi di `docs/Skripsi/Rapih/02_BAB_2/extracted/bab2_review.md`.

Judul acuan: **Analisis Sentimen Ulasan Pengguna Aplikasi JakOne Mobile Menggunakan IndoBERT**.

Catatan konteks: aspek keamanan bukan fokus utama judul. Isu seperti OTP, login, akun, verifikasi, transaksi, password, kendala akses, dan error aplikasi hanya diposisikan sebagai keyword issue atau analisis pendukung.

## Tabel Gap Struktur

| No | Subbab Rencana | Status | Kondisi di BAB 2 Saat Ini | Yang Perlu Dikerjakan | Prioritas |
|---|---|---|---|---|---|
| 1 | 2.1 Penelitian Terdahulu | Perlu Dipindahkan | Sudah ada sebagai `2.13 Penelitian Terdahulu` setelah evaluasi model. Berisi tabel lima penelitian terdahulu. | Pindahkan ke awal menjadi `2.1 Penelitian Terdahulu`. Verifikasi semua referensi, nama penulis, tahun, metode, dan hasil metrik. | Wajib |
| 2 | 2.2 Mobile Banking | Belum Ada | Belum ada subbab khusus Mobile Banking. Konteks perbankan digital hanya muncul di bagian JakOne Mobile dan latar objek. | Tambahkan teori mobile banking sebagai konteks domain sebelum JakOne Mobile. Bahas singkat layanan, transaksi digital, dan relevansi ulasan pengguna. | Wajib |
| 3 | 2.3 JakOne Mobile | Sudah Ada | Sudah ada sebagai `2.3 JakOne Mobile`. Membahas aplikasi Bank DKI, fitur layanan, dan alasan objek penelitian. | Sesuaikan nomor subbab menjadi `2.3`. Perkuat sedikit dengan sumber resmi jika tersedia. | Wajib |
| 4 | 2.4 Ulasan Pengguna Aplikasi | Ada Tapi Perlu Diperkuat | Sudah ada sebagai `2.2 Ulasan Pengguna`. Membahas ulasan Google Play Store, rating, komentar, dan scraping. | Ubah judul menjadi `Ulasan Pengguna Aplikasi`. Perkuat hubungan dengan aplikasi mobile dan data review Google Play Store. | Wajib |
| 5 | 2.5 Analisis Sentimen | Sudah Ada | Sudah ada sebagai `2.1 Analisis Sentimen`. Sudah membahas definisi, kelas positif/negatif/netral, dan penerapan pada JakOne Mobile. | Pindahkan urutan ke `2.5`. Rapikan beberapa kalimat dan pastikan definisi sentimen netral jelas. | Wajib |
| 6 | 2.6 Text Mining dan Natural Language Processing | Ada Tapi Perlu Diperkuat | Sudah ada sebagai `2.4 Natural Language Processing`, tetapi belum membahas Text Mining secara eksplisit. | Ubah menjadi `Text Mining dan Natural Language Processing`. Tambahkan hubungan text mining dengan ekstraksi pola dari ulasan pengguna. | Wajib |
| 7 | 2.7 Preprocessing Teks | Ada Tapi Perlu Diperkuat | Sudah ada sebagai `2.5 Text Preprocessing`. Membahas case folding, penghapusan karakter, tokenisasi, stopword, dan normalisasi. | Ubah judul menjadi `Preprocessing Teks`. Perkuat untuk konteks Bahasa Indonesia, slang, typo, emoji, duplikasi, dan teks kosong. | Wajib |
| 8 | 2.8 Pelabelan Sentimen Berbasis Lexicon | Sudah Ada | Sudah ada sebagai `2.6 Pelabelan Sentimen Berbasis Lexicon`. Membahas skor kata positif/negatif dan label awal. | Pindahkan ke nomor `2.8`. Rapikan kalimat "diterapkan untuk secara otomatis". | Wajib |
| 9 | 2.9 InSet Lexicon | Sudah Ada | Sudah ada sebagai `2.7 InSet Lexicon`. Membahas InSet untuk Bahasa Indonesia dan penggunaannya pada label otomatis. | Pindahkan ke nomor `2.9`. Verifikasi referensi Fachrina dan Purwarianti serta detail versi InSet. | Wajib |
| 10 | 2.10 Validasi dan Perbaikan Label | Belum Ada | Belum ada subbab khusus. BAB 2 baru menyebut label dari lexicon digunakan untuk data latih, belum membahas validasi/perbaikan label. | Tambahkan subbab tentang kebutuhan validasi label, label noise, konteks, negasi, sarkasme, dan perbaikan label sebelum modeling. | Wajib |
| 11 | 2.11 Klasifikasi Teks | Sudah Ada | Sudah ada sebagai `2.8 Klasifikasi Teks`. Membahas kategori teks, machine learning, deep learning, dan klasifikasi sentimen. | Pindahkan ke nomor `2.11`. Rapikan typo seperti `ketegori` dan `mengcangkup`. | Wajib |
| 12 | 2.12 Deep Learning untuk NLP | Ada Tapi Perlu Diperkuat | Sudah ada sebagai `2.9 Machine Learning dan Deep Learning`, tetapi masih umum dan belum fokus pada NLP. | Ubah menjadi `Deep Learning untuk NLP`. Ringkas machine learning umum dan tekankan deep learning untuk pemrosesan teks. | Wajib |
| 13 | 2.13 Transformer | Belum Ada | Belum ada subbab khusus Transformer. Transformer hanya disebut sekilas di NLP, deep learning, dan BERT. | Tambahkan teori Transformer, self-attention, dan hubungannya sebagai dasar BERT/IndoBERT. | Wajib |
| 14 | 2.14 BERT | Sudah Ada | Sudah ada sebagai `2.10 BERT`. Membahas bidirectional context, MLM, NSP, dan fine-tuning. | Pindahkan ke nomor `2.14`. Pastikan hubungan BERT dengan Transformer jelas setelah subbab Transformer ditambahkan. | Wajib |
| 15 | 2.15 IndoBERT | Sudah Ada | Sudah ada sebagai `2.11 IndoBERT`. Membahas IndoBERT, IndoNLU, Bahasa Indonesia, dan penerapan pada sentimen JakOne Mobile. | Pindahkan ke nomor `2.15`. Verifikasi referensi Wilie et al. atau Koto et al. | Wajib |
| 16 | 2.16 Fine-tuning IndoBERT | Ada Tapi Perlu Diperkuat | Fine-tuning sudah disebut di subbab IndoBERT dan Kerangka Pemikiran, tetapi belum ada subbab khusus. | Tambahkan subbab khusus fine-tuning IndoBERT untuk klasifikasi sentimen tiga kelas. Jelaskan pre-trained model, dataset berlabel, dan classifier. | Wajib |
| 17 | 2.17 Pembagian Dataset Train, Validation, dan Test | Belum Ada | Belum ada subbab khusus. Kerangka pemikiran hanya menyebut data latih dan data uji, belum validation. | Tambahkan teori split train/validation/test dan stratified split agar sesuai pipeline project. | Wajib |
| 18 | 2.18 Evaluasi Model Klasifikasi | Sudah Ada | Sudah ada sebagai `2.12 Evaluasi Model Klasifikasi`. Membahas accuracy, precision, recall, F1-score, macro average, dan confusion matrix. | Pindahkan ke nomor `2.18`. Pecah metrik menjadi subsubbab sesuai struktur rencana. | Wajib |
| 19 | 2.18.1 Confusion Matrix | Ada Tapi Perlu Diperkuat | Confusion matrix sudah disebut dalam paragraf evaluasi, tetapi belum ada subsubbab dan belum dijelaskan detail. | Tambahkan subsubbab khusus, jelaskan fungsi matriks untuk melihat benar/salah prediksi per kelas. | Wajib |
| 20 | 2.18.2 Accuracy | Ada Tapi Perlu Diperkuat | Accuracy sudah didefinisikan singkat di subbab evaluasi. | Tambahkan subsubbab dan rumus atau penjelasan yang lebih formal. | Wajib |
| 21 | 2.18.3 Precision | Ada Tapi Perlu Diperkuat | Precision sudah didefinisikan singkat, tetapi masih memakai konteks "prediksi positif" yang perlu disesuaikan untuk multi-kelas. | Tambahkan subsubbab dan jelaskan precision per kelas serta macro average. | Wajib |
| 22 | 2.18.4 Recall | Ada Tapi Perlu Diperkuat | Recall sudah didefinisikan singkat, tetapi belum dijelaskan untuk multi-kelas sentimen. | Tambahkan subsubbab dan jelaskan recall per kelas. | Wajib |
| 23 | 2.18.5 F1-Score | Ada Tapi Perlu Diperkuat | F1-score sudah dijelaskan sebagai rata-rata harmonik precision dan recall. | Tambahkan subsubbab dan rumus. Jelaskan relevansi saat precision dan recall perlu diseimbangkan. | Wajib |
| 24 | 2.18.6 Macro F1 | Ada Tapi Perlu Diperkuat | Macro average sudah disebut, tetapi belum menjadi subsubbab khusus dan belum dikaitkan kuat dengan ketidakseimbangan kelas. | Tambahkan subsubbab Macro F1 dan kaitkan dengan evaluasi kelas positif, negatif, dan netral. | Wajib |
| 25 | 2.19 Class Imbalance | Belum Ada | Belum ada subbab khusus. BAB 2 belum membahas distribusi kelas tidak seimbang dan dampaknya pada model. | Tambahkan teori class imbalance dan dampaknya terhadap kelas minoritas, terutama mengapa macro F1 penting. | Wajib |
| 26 | 2.20 Visualisasi dan Dashboard Hasil Analisis | Belum Ada | Belum ada subbab visualisasi atau dashboard. | Tambahkan singkat sebagai pendukung penyajian hasil, seperti distribusi label, confusion matrix, training curve, word cloud, dan dashboard. | Sebaiknya |
| 27 | 2.21 Keyword Issue sebagai Analisis Pendukung | Belum Ada | Belum ada subbab keyword issue. BAB 2 belum membahas analisis kata kunci dominan. | Tambahkan sebagai analisis pendukung, bukan fokus utama. Tekankan bahwa isu keamanan hanya contoh keyword issue. | Tambahan |
| 28 | 2.22 Kerangka Pemikiran | Ada Tapi Perlu Diperkuat | Sudah ada sebagai `2.14 Kerangka Pemikiran`. Alur mencakup scraping, preprocessing, InSet, split, fine-tuning, evaluasi. Namun masih menyebut data latih dan data uji saja. | Pindahkan ke nomor `2.22`. Perbarui alur agar menyebut train, validation, test, validasi/perbaikan label, dashboard, dan keyword issue sebagai pendukung. | Wajib |

## Ringkasan

### 1. Subbab yang Sudah Aman

- 2.3 JakOne Mobile
- 2.5 Analisis Sentimen
- 2.8 Pelabelan Sentimen Berbasis Lexicon
- 2.9 InSet Lexicon
- 2.11 Klasifikasi Teks
- 2.14 BERT
- 2.15 IndoBERT
- 2.18 Evaluasi Model Klasifikasi

Subbab di atas sudah ada dan relatif sesuai. Revisi utamanya adalah pemindahan nomor, perapihan bahasa, dan verifikasi referensi.

### 2. Subbab yang Wajib Ditambahkan

- 2.2 Mobile Banking
- 2.10 Validasi dan Perbaikan Label
- 2.13 Transformer
- 2.17 Pembagian Dataset Train, Validation, dan Test
- 2.19 Class Imbalance

Subbab ini belum ada dalam BAB 2 hasil ekstraksi dan penting untuk menjelaskan pipeline project.

### 3. Subbab yang Perlu Diperkuat

- 2.4 Ulasan Pengguna Aplikasi
- 2.6 Text Mining dan Natural Language Processing
- 2.7 Preprocessing Teks
- 2.12 Deep Learning untuk NLP
- 2.16 Fine-tuning IndoBERT
- 2.18.1 Confusion Matrix
- 2.18.2 Accuracy
- 2.18.3 Precision
- 2.18.4 Recall
- 2.18.5 F1-Score
- 2.18.6 Macro F1
- 2.22 Kerangka Pemikiran

Bagian ini sudah muncul secara langsung atau tidak langsung, tetapi belum cukup kuat atau belum mengikuti struktur rencana.

### 4. Subbab yang Cukup Menjadi Tambahan Saja

- 2.20 Visualisasi dan Dashboard Hasil Analisis
- 2.21 Keyword Issue sebagai Analisis Pendukung

Keduanya penting untuk menyambungkan BAB 2 dengan fitur project dan dashboard, tetapi tidak perlu dibuat terlalu panjang. Keyword issue harus diposisikan sebagai analisis pendukung, bukan fokus utama penelitian.

### 5. Urutan Revisi yang Disarankan

1. Rapikan struktur dan penomoran subbab sesuai rencana baru.
2. Pindahkan `Penelitian Terdahulu` dari posisi lama `2.13` menjadi `2.1`.
3. Tambahkan subbab wajib yang belum ada: Mobile Banking, Validasi Label, Transformer, Split Dataset, dan Class Imbalance.
4. Pecah `Evaluasi Model Klasifikasi` menjadi subsubbab Confusion Matrix, Accuracy, Precision, Recall, F1-Score, dan Macro F1.
5. Perkuat Fine-tuning IndoBERT dan Kerangka Pemikiran agar sesuai pipeline project.
6. Tambahkan Visualisasi Dashboard dan Keyword Issue secara ringkas sebagai pendukung.
7. Hapus atau pindahkan pembahasan `Python` dari BAB 2 jika tidak diwajibkan; lebih tepat diletakkan di BAB 3 sebagai perangkat penelitian.

### 6. Referensi yang Perlu Diverifikasi atau Ditambahkan

- Referensi analisis sentimen: pastikan Liu (2022) benar dan sesuai sumber yang dipakai.
- Referensi ulasan pengguna aplikasi dan Google Play Store: verifikasi Wibirama et al. (2023) atau tambahkan sumber yang kuat.
- Referensi mobile banking: perlu ditambahkan karena subbab belum ada.
- Referensi NLP/text mining: verifikasi Jurafsky dan Martin (2023), atau gunakan sumber yang sesuai format kampus.
- Referensi InSet Lexicon: verifikasi Fachrina dan Purwarianti (2017).
- Referensi Transformer: tambahkan Vaswani et al. (2017), *Attention Is All You Need*.
- Referensi BERT: verifikasi Devlin et al. (2019), *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*.
- Referensi IndoBERT/IndoNLU: verifikasi Wilie et al. (2020) atau Koto et al. (2020), sesuaikan dengan sumber model IndoBERT yang digunakan.
- Referensi evaluasi klasifikasi: verifikasi Sokolova dan Lapalme, terutama tahun yang tertulis di BAB 2.
- Referensi class imbalance: tambahkan sumber tentang imbalanced classification atau evaluasi macro F1.
- Referensi penelitian terdahulu dalam tabel: verifikasi Saputra et al. (2024), Wibirama et al. (2023), Nugroho et al. (2022), Pramana et al. (2025), dan Hidayah et al. (2025), termasuk judul, metode, dan hasil metrik.

## Rekap Status

- Sudah Ada: 8 subbab/komponen
- Ada Tapi Perlu Diperkuat: 12 subbab/komponen
- Belum Ada: 7 subbab/komponen
- Perlu Dipindahkan: 1 subbab/komponen
- Perlu Dirapikan: tercakup dalam catatan perapihan penomoran, typo, dan subbab Python yang tidak masuk struktur rencana

