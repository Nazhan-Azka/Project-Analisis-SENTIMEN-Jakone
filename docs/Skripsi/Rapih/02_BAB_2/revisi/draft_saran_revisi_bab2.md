# Draft Saran Revisi BAB 2

Dokumen ini adalah draft saran tambahan untuk memperkuat BAB 2. File Word asli tidak diubah.

## Arah Revisi

BAB 2 tidak perlu diubah menjadi pembahasan khusus aspek keamanan. Fokus teori tetap pada analisis sentimen ulasan pengguna aplikasi JakOne Mobile menggunakan IndoBERT. Aspek seperti OTP, login, akun, verifikasi, transaksi, password, kendala akses, dan error aplikasi cukup ditempatkan sebagai keyword issue atau analisis tambahan pada bagian visualisasi/analisis hasil.

## Perbaikan Struktur

Perbaiki penomoran subbab agar berurutan. Saat ini terdapat subbab `2.2 Pyhton` setelah `2.3 JakOne Mobile`, sehingga urutan menjadi tidak konsisten. Kata "Pyhton" juga perlu diperbaiki menjadi "Python".

Saran urutan ringkas:

1. Analisis Sentimen
2. Ulasan Pengguna Aplikasi
3. Mobile Banking
4. JakOne Mobile
5. Natural Language Processing
6. Text Preprocessing Bahasa Indonesia
7. Pelabelan Sentimen
8. Lexicon-Based Labeling dan InSet Lexicon
9. Validasi Label
10. Split Dataset Train, Validation, dan Test
11. Klasifikasi Teks
12. Deep Learning untuk NLP
13. Transformer
14. BERT
15. IndoBERT
16. Fine-Tuning IndoBERT
17. Evaluasi Klasifikasi
18. Class Imbalance
19. Visualisasi Hasil dan Keyword Issue
20. Penelitian Terdahulu
21. Kerangka Pemikiran

## Draft Tambahan Subbab

### Mobile Banking

Mobile banking merupakan layanan perbankan digital yang memungkinkan nasabah mengakses layanan keuangan melalui perangkat mobile. Layanan ini dapat mencakup pengecekan saldo, transfer dana, pembayaran tagihan, pembelian produk digital, serta layanan transaksi lainnya. Dalam penelitian analisis sentimen, mobile banking menjadi domain yang relevan karena ulasan pengguna dapat mencerminkan pengalaman pengguna terhadap kemudahan penggunaan, kecepatan layanan, stabilitas aplikasi, dan kualitas transaksi digital.

### Validasi dan Perbaikan Label

Pelabelan otomatis menggunakan lexicon dapat membantu mempercepat proses pembentukan dataset berlabel, tetapi hasil label tetap berpotensi mengandung kesalahan. Kesalahan tersebut dapat muncul karena pendekatan berbasis kamus tidak selalu mampu memahami konteks kalimat, negasi, sarkasme, atau istilah khusus yang digunakan pengguna. Oleh karena itu, validasi atau perbaikan label diperlukan untuk mengevaluasi kualitas label dan mengurangi kemungkinan noise pada dataset sebelum digunakan dalam proses pelatihan model.

### Split Dataset Train, Validation, dan Test

Pembagian dataset merupakan tahapan penting dalam pembangunan model klasifikasi. Data train digunakan untuk melatih model, data validation digunakan untuk memantau performa model selama proses pelatihan, sedangkan data test digunakan untuk mengukur performa akhir model terhadap data yang belum pernah digunakan pada proses pelatihan. Dalam klasifikasi sentimen multi-kelas, pembagian data sebaiknya mempertahankan proporsi label pada setiap subset agar hasil evaluasi lebih representatif.

### Transformer

Transformer adalah arsitektur deep learning yang menggunakan mekanisme self-attention untuk mempelajari hubungan antar token dalam suatu teks. Berbeda dengan model sekuensial seperti RNN atau LSTM yang memproses teks secara berurutan, Transformer dapat memperhatikan hubungan antar kata secara lebih fleksibel dalam satu kalimat. Arsitektur ini menjadi dasar bagi model bahasa modern seperti BERT dan IndoBERT.

### Fine-Tuning IndoBERT

Fine-tuning merupakan proses melatih kembali model pre-trained pada dataset khusus untuk menyelesaikan tugas tertentu. IndoBERT sebagai model pre-trained telah mempelajari representasi bahasa Indonesia dari korpus besar, tetapi tetap perlu disesuaikan dengan tugas klasifikasi sentimen. Dalam penelitian ini, proses fine-tuning dilakukan agar IndoBERT dapat mengenali pola sentimen pada ulasan pengguna aplikasi JakOne Mobile dan mengklasifikasikannya ke dalam kelas positif, negatif, dan netral.

### Class Imbalance

Class imbalance adalah kondisi ketika jumlah data pada setiap kelas tidak seimbang. Dalam analisis sentimen, kondisi ini dapat menyebabkan model lebih dominan mempelajari kelas mayoritas dan kurang optimal mengenali kelas minoritas. Oleh karena itu, penggunaan metrik macro F1 menjadi penting karena macro F1 menghitung rata-rata performa setiap kelas tanpa memperhitungkan banyaknya data pada kelas tersebut.

### Visualisasi Hasil dan Keyword Issue

Visualisasi hasil digunakan untuk menyajikan informasi penelitian secara lebih mudah dipahami, seperti distribusi label, distribusi data, confusion matrix, kurva training, dan word cloud. Selain itu, analisis keyword issue dapat digunakan sebagai analisis tambahan untuk melihat kata atau topik yang sering muncul dalam ulasan pengguna. Pada penelitian ini, keyword issue dapat mencakup isu seperti transaksi, login, OTP, akun, verifikasi, password, kendala akses, dan error aplikasi. Analisis tersebut berfungsi sebagai pelengkap interpretasi hasil sentimen, bukan sebagai fokus utama penelitian.

## Poin Perbaikan Kalimat

- "Pyhton" perlu diganti menjadi "Python".
- "menipulasi teks" sebaiknya menjadi "memanipulasi teks" atau "mengolah teks".
- "kecendurungan" jika muncul di BAB 2 perlu diganti menjadi "kecenderungan".
- "ketegori" perlu diganti menjadi "kategori".
- "mengcangkup" perlu diganti menjadi "mencakup".
- "analisa data" lebih baku ditulis "analisis data".
- Kalimat "sentimen negatif menunjukkan bahwa ketidakpuasan atau kritik" dapat diperbaiki menjadi "sentimen negatif menunjukkan ketidakpuasan atau kritik".

## Catatan untuk Penelitian Terdahulu

Tabel penelitian terdahulu perlu diverifikasi kembali. Pastikan setiap penelitian benar-benar ada, nama penulis tepat, tahun benar, judul sesuai, dan hasil metrik tidak berbeda dari sumber asli. Referensi yang paling penting untuk diperiksa adalah BERT, IndoBERT/IndoNLU, InSet Lexicon, analisis sentimen, dan evaluasi klasifikasi.

