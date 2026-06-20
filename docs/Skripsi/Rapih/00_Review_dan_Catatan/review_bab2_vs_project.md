# Review BAB 2 vs Project

## Konteks Penilaian

Judul skripsi yang digunakan sebagai acuan:

**Analisis Sentimen Ulasan Pengguna Aplikasi JakOne Mobile Menggunakan IndoBERT**

Fokus utama penelitian adalah analisis sentimen ulasan pengguna aplikasi JakOne Mobile secara umum, klasifikasi sentimen positif, negatif, dan netral, serta penggunaan IndoBERT sebagai metode utama. Aspek keamanan seperti OTP, login, akun, verifikasi, transaksi, password, kendala akses, dan error aplikasi diposisikan sebagai analisis pendukung atau keyword issue, bukan fokus utama judul.

## Ringkasan Kesesuaian BAB 2

BAB 2 sudah cukup sesuai dengan project karena sudah memuat teori utama tentang analisis sentimen, ulasan pengguna, JakOne Mobile, NLP, preprocessing, lexicon-based labeling, InSet Lexicon, klasifikasi teks, machine learning/deep learning, BERT, IndoBERT, evaluasi model, penelitian terdahulu, dan kerangka pemikiran.

Namun, BAB 2 masih perlu diperkuat agar benar-benar selaras dengan pipeline project. Bagian yang paling perlu ditambahkan adalah Transformer, fine-tuning IndoBERT, split dataset train/validation/test, validasi/perbaikan label, class imbalance, dan visualisasi/dashboard sebagai pendukung hasil. Selain itu, ada masalah struktur penomoran, misalnya subbab `2.2 Pyhton` muncul setelah `2.3 JakOne Mobile`, dan terdapat typo "Pyhton".

## Teori yang Wajib Ada

Teori berikut wajib ada karena langsung menjadi dasar penelitian dan pipeline:

1. Analisis sentimen.
2. Ulasan pengguna aplikasi.
3. Mobile banking.
4. JakOne Mobile.
5. Natural Language Processing atau text mining.
6. Preprocessing teks Bahasa Indonesia.
7. Pelabelan sentimen.
8. Lexicon-based labeling atau InSet Lexicon.
9. Validasi atau perbaikan label.
10. Split dataset train, validation, dan test.
11. Deep learning untuk NLP.
12. Transformer.
13. BERT.
14. IndoBERT.
15. Fine-tuning IndoBERT.
16. Evaluasi klasifikasi.
17. Confusion matrix.
18. Accuracy, precision, recall, F1-score, dan macro F1.
19. Class imbalance.
20. Penelitian terdahulu yang relevan.

Status saat ini: sebagian besar sudah ada, tetapi validasi label, split train/validation/test, Transformer, fine-tuning IndoBERT, dan class imbalance belum kuat atau belum menjadi subbab khusus.

## Teori yang Sebaiknya Ada

Teori berikut sebaiknya ada karena membantu menjelaskan hasil dan implementasi project:

1. Text classification.
2. Tokenisasi pada BERT/IndoBERT.
3. Stratified split.
4. Label noise dari pelabelan lexicon.
5. Macro average vs weighted average.
6. Visualisasi hasil analisis sentimen.
7. Dashboard sebagai media penyajian hasil.
8. Keyword issue atau analisis kata kunci dominan.

Status saat ini: klasifikasi teks dan macro average sudah ada. Visualisasi, dashboard, keyword issue, label noise, tokenisasi, dan stratified split belum cukup dibahas.

## Teori yang Hanya Tambahan

Bagian berikut dapat ditulis singkat karena hanya mendukung, bukan inti teori:

1. Python.
2. Library seperti Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, dan Transformers.
3. Streamlit/dashboard.
4. Word cloud.
5. Keyword issue terkait akses, transaksi, login, OTP, dan keamanan.

Python boleh ada, tetapi tidak perlu terlalu panjang. Lebih baik ditempatkan sebagai "Perangkat dan Pustaka Pendukung" atau dipindahkan ke BAB 3 jika kampus lebih menekankan alat penelitian pada metodologi.

## Teori yang Tidak Perlu Terlalu Panjang

1. Penjelasan umum Python.
2. Sejarah umum machine learning.
3. Penjelasan terlalu luas tentang GPT atau model NLP lain yang tidak digunakan.
4. Aspek keamanan teknis mobile banking.
5. Audit keamanan, penetrasi sistem, forensik digital, atau infrastruktur bank.

Aspek keamanan cukup diposisikan sebagai isu tambahan dalam ulasan pengguna dan keyword issue.

## Materi BAB 2 yang Sudah Sesuai

- Analisis sentimen sudah dijelaskan dan dikaitkan dengan kelas positif, negatif, dan netral.
- Ulasan pengguna sudah dijelaskan sebagai sumber opini dari Google Play Store.
- JakOne Mobile sudah dibahas sebagai objek penelitian.
- NLP sudah dijelaskan sebagai dasar pengolahan bahasa.
- Preprocessing teks sudah ada dan menyebut case folding, penghapusan karakter, tokenisasi, stopword, dan normalisasi.
- Pelabelan berbasis lexicon sudah ada.
- InSet Lexicon sudah dijelaskan.
- Klasifikasi teks sudah dibahas.
- Machine learning dan deep learning sudah dibahas.
- BERT sudah dijelaskan.
- IndoBERT sudah dijelaskan dan dikaitkan dengan Bahasa Indonesia.
- Evaluasi model sudah mencakup accuracy, precision, recall, F1-score, macro average, dan confusion matrix.
- Penelitian terdahulu sudah tersedia dalam tabel.
- Kerangka pemikiran sudah menggambarkan alur umum penelitian.

## Materi BAB 2 yang Belum Ada

- Teori mobile banking sebagai konsep umum sebelum JakOne Mobile.
- Transformer sebagai arsitektur dasar BERT.
- Fine-tuning IndoBERT sebagai proses adaptasi model pre-trained ke tugas klasifikasi sentimen.
- Tokenisasi BERT/IndoBERT, misalnya input_ids, attention_mask, max length.
- Validasi atau perbaikan label setelah lexicon labeling.
- Split dataset train, validation, dan test.
- Stratified split agar distribusi kelas tetap proporsional.
- Class imbalance dan dampaknya terhadap evaluasi, terutama macro F1 dan kelas minoritas.
- Dashboard/visualisasi hasil sebagai pendukung penyajian hasil penelitian.
- Keyword issue sebagai analisis tambahan, bukan fokus utama.

## Materi yang Ada tetapi Masih Kurang Kuat

- Preprocessing perlu dibuat lebih spesifik untuk teks Bahasa Indonesia dan ulasan aplikasi, seperti slang, typo, emoji, duplikasi, dan teks kosong.
- Pelabelan lexicon perlu menyinggung keterbatasan seperti negasi, sarkasme, konteks domain, dan label noise.
- InSet Lexicon perlu dijelaskan sebagai label awal, bukan sumber kebenaran final mutlak.
- Evaluasi model perlu memberi rumus atau penjelasan lebih jelas untuk precision, recall, F1-score, macro F1, dan confusion matrix.
- Kerangka pemikiran masih menyebut data latih dan data uji, tetapi project menggunakan train, validation, dan test.
- Penelitian terdahulu perlu diverifikasi sumbernya dan dibuat lebih kuat dengan sitasi yang benar.

## Materi yang Terlalu Melebar atau Kurang Relevan

- Subbab Python terlalu panjang untuk BAB 2 jika hanya menjelaskan alat. Bagian ini bisa dipersingkat atau dipindahkan ke BAB 3 sebagai tools penelitian.
- Pembahasan GPT dalam NLP cukup disebut sekilas, karena model yang digunakan adalah IndoBERT.
- Pembahasan keamanan jangan terlalu panjang karena bukan fokus utama judul.

## Referensi yang Perlu Diverifikasi

Referensi berikut perlu dicek ulang agar sesuai dengan sumber akademik asli dan format sitasi kampus:

- Liu (2022) untuk definisi analisis sentimen. Perlu dipastikan apakah yang dimaksud adalah buku/paper Bing Liu dan tahunnya tepat.
- Jurafsky dan Martin (2023) untuk definisi NLP. Perlu dipastikan edisi atau versi draft buku yang dipakai.
- Fachrina dan Purwarianti (2017) untuk InSet Lexicon. Perlu dipastikan nama penulis, tahun, judul paper, dan venue.
- Devlin et al. (2019) untuk BERT. Ini referensi inti dan sebaiknya dicantumkan lengkap.
- Wilie et al. (2020) atau Koto et al. (2020) untuk IndoBERT/IndoNLU. Perlu dipastikan mana referensi utama yang dipakai.
- Sokolova dan Lapalme untuk metrik evaluasi. Tahun di BAB 2 tertulis 2022, perlu diverifikasi karena referensi metrik klasifikasi yang umum sering dikutip dari tahun lebih lama.
- Saputra et al. (2024), Wibirama et al. (2023), Nugroho et al. (2022), Pramana et al. (2025), dan Hidayah et al. (2025) pada tabel penelitian terdahulu. Perlu dipastikan paper benar-benar ada, judulnya tepat, dan hasil metriknya sesuai.

Catatan: review ini belum melakukan verifikasi internet atau pemeriksaan isi `DAFTAR PUSTAKA.docx`; daftar di atas didasarkan pada isi BAB 2 hasil ekstraksi.

## Saran Urutan Subbab BAB 2 yang Lebih Rapi

1. 2.1 Analisis Sentimen
2. 2.2 Ulasan Pengguna Aplikasi
3. 2.3 Mobile Banking
4. 2.4 JakOne Mobile
5. 2.5 Text Mining dan Natural Language Processing
6. 2.6 Text Preprocessing Bahasa Indonesia
7. 2.7 Pelabelan Sentimen
8. 2.8 Lexicon-Based Labeling dan InSet Lexicon
9. 2.9 Validasi dan Perbaikan Label
10. 2.10 Pembagian Dataset Train, Validation, dan Test
11. 2.11 Klasifikasi Teks
12. 2.12 Deep Learning untuk NLP
13. 2.13 Transformer
14. 2.14 BERT
15. 2.15 IndoBERT
16. 2.16 Fine-Tuning IndoBERT untuk Klasifikasi Sentimen
17. 2.17 Evaluasi Model Klasifikasi
18. 2.18 Class Imbalance
19. 2.19 Visualisasi Hasil dan Dashboard
20. 2.20 Keyword Issue sebagai Analisis Tambahan
21. 2.21 Penelitian Terdahulu
22. 2.22 Kerangka Pemikiran

Jika ingin BAB 2 lebih ringkas, Python tidak perlu menjadi subbab utama. Python dan library dapat dijelaskan di BAB 3 bagian perangkat penelitian.

## Saran Kalimat atau Poin yang Bisa Ditambahkan

### Mobile Banking

Mobile banking merupakan layanan perbankan digital yang memungkinkan nasabah melakukan transaksi dan mengakses informasi rekening melalui perangkat mobile. Dalam konteks penelitian ini, mobile banking menjadi domain aplikasi yang dianalisis karena ulasan pengguna dapat mencerminkan persepsi terhadap kualitas layanan, kemudahan penggunaan, stabilitas aplikasi, dan pengalaman transaksi.

### Validasi Label

Label yang dihasilkan dari metode lexicon-based labeling perlu divalidasi karena pendekatan berbasis kamus tidak selalu mampu menangkap konteks kalimat, negasi, sarkasme, atau istilah khusus pada domain aplikasi perbankan. Oleh karena itu, validasi atau perbaikan label dapat digunakan untuk meningkatkan kualitas dataset sebelum digunakan dalam proses pelatihan model.

### Split Dataset

Pembagian dataset ke dalam data train, validation, dan test dilakukan agar proses pelatihan, pemilihan model, dan evaluasi dapat dilakukan secara terpisah. Data train digunakan untuk melatih model, data validation digunakan untuk memantau performa selama pelatihan, sedangkan data test digunakan untuk mengevaluasi performa akhir model terhadap data yang tidak digunakan pada proses pelatihan.

### Transformer

Transformer adalah arsitektur deep learning yang menggunakan mekanisme self-attention untuk menangkap hubungan antar kata dalam suatu teks. Arsitektur ini menjadi dasar dari BERT dan IndoBERT karena mampu memahami konteks kata secara lebih baik dibandingkan pendekatan sekuensial tradisional seperti RNN atau LSTM.

### Fine-Tuning IndoBERT

Fine-tuning adalah proses melatih kembali model pre-trained pada dataset khusus agar model dapat menyesuaikan representasi bahasa yang telah dipelajari sebelumnya dengan tugas tertentu. Dalam penelitian ini, IndoBERT di-fine-tuning menggunakan dataset ulasan JakOne Mobile yang telah memiliki label sentimen positif, negatif, dan netral.

### Class Imbalance

Class imbalance terjadi ketika jumlah data pada setiap kelas tidak seimbang. Pada analisis sentimen tiga kelas, kondisi ini dapat menyebabkan model lebih mudah mengenali kelas mayoritas dan lebih sulit mengenali kelas minoritas. Oleh karena itu, metrik seperti macro F1 penting digunakan karena menghitung rata-rata performa tiap kelas tanpa dipengaruhi jumlah data pada masing-masing kelas.

### Keyword Issue

Analisis keyword issue digunakan sebagai analisis tambahan untuk melihat kata atau isu yang sering muncul dalam ulasan pengguna. Dalam penelitian ini, keyword issue tidak menjadi fokus utama model klasifikasi, tetapi digunakan untuk memperkaya interpretasi hasil sentimen, misalnya pada isu transaksi, login, OTP, akun, verifikasi, password, kendala akses, dan error aplikasi.

## Catatan Konsistensi dengan Project

- Project aktif v3 memakai dataset `data/final/06_jakone_modeling_master_v3.csv`.
- Konfigurasi training v3 memakai model `indobenchmark/indobert-base-p1`.
- Kolom utama modeling v3 adalah `review`, `label`, dan `split_set`.
- Label yang digunakan adalah `negatif`, `netral`, dan `positif`.
- Training v3 menggunakan 2 epoch, batch size 8, learning rate 2e-5, max length 128, seed 42, dan `use_class_weight = false`.
- Evaluasi v3 baseline yang tersedia menunjukkan accuracy 0,9316 dan macro F1 0,8774.
- README masih memuat beberapa informasi lama seperti `indobert-base-p2` dan hasil evaluasi root lama. Untuk penulisan skripsi, gunakan satu versi final yang sudah dipilih agar BAB 2, BAB 3, BAB 4, README, dan dashboard konsisten.

