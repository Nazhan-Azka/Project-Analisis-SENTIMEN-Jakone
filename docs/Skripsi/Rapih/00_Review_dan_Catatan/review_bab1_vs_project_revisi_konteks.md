# Review BAB 1 vs Project - Revisi Konteks Judul Awal

## Konteks yang Dipakai

Judul utama skripsi:

**Analisis Sentimen Ulasan Pengguna Aplikasi JakOne Mobile Menggunakan IndoBERT**

Berdasarkan konteks ini, fokus utama penelitian adalah analisis sentimen ulasan pengguna JakOne Mobile secara umum menggunakan IndoBERT. Model utama mengklasifikasikan ulasan ke dalam tiga kelas sentimen, yaitu positif, negatif, dan netral.

Aspek keamanan tidak menjadi fokus utama judul dan tidak perlu mengubah arah penelitian menjadi penelitian khusus keamanan. Aspek keamanan lebih tepat diposisikan sebagai analisis tambahan atau fitur pendukung untuk memperkaya interpretasi hasil, misalnya melalui analisis keyword issue pada kata seperti OTP, login, akun, verifikasi, transaksi, password, kendala akses, dan error yang berkaitan dengan keamanan.

## Ringkasan Kesesuaian BAB 1

BAB 1 sudah cukup sesuai dengan judul awal. Isi BAB 1 sudah membahas konteks mobile banking, aplikasi JakOne Mobile, ulasan pengguna Google Play Store, analisis sentimen, serta alasan penggunaan IndoBERT. Dengan demikian, arah utama BAB 1 masih sejalan dengan penelitian analisis sentimen ulasan pengguna JakOne Mobile secara umum.

Yang perlu diperbaiki bukan mengubah BAB 1 menjadi terlalu fokus pada keamanan, tetapi memperjelas alur penelitian yang sudah dilakukan dalam project, terutama preprocessing, pelabelan sentimen, pembagian dataset, fine-tuning IndoBERT, evaluasi model, dan visualisasi hasil.

## Fokus Utama Penelitian vs Analisis Tambahan

### Fokus Utama Penelitian

Fokus utama penelitian adalah:

- menganalisis ulasan pengguna aplikasi JakOne Mobile;
- mengklasifikasikan sentimen ulasan ke dalam kelas positif, negatif, dan netral;
- menggunakan IndoBERT sebagai metode utama klasifikasi sentimen;
- mengevaluasi performa model menggunakan metrik seperti accuracy, precision, recall, dan F1-score;
- melihat distribusi sentimen pengguna terhadap aplikasi JakOne Mobile secara umum.

Fokus utama ini sudah tercermin cukup baik dalam BAB 1.

### Analisis Tambahan / Fitur Pendukung

Analisis tambahan dalam project adalah:

- analisis keyword issue;
- word cloud;
- analisis isu tertentu yang sering muncul pada ulasan pengguna;
- pengamatan terhadap kata atau topik seperti OTP, login, akun, verifikasi, transaksi, password, kendala akses, dan error terkait keamanan;
- dashboard Streamlit untuk membantu visualisasi dataset, training, evaluasi, keyword issue, word cloud, dan demo prediksi.

Bagian ini sebaiknya ditulis sebagai pendukung pembahasan hasil sentimen, bukan sebagai inti utama penelitian.

## Penilaian per Bagian BAB 1

### 1. Latar Belakang

Status: sudah sesuai, perlu sedikit perapihan.

BAB 1 sudah tepat karena memulai dari perkembangan teknologi digital, mobile banking, JakOne Mobile, ulasan pengguna, dan kebutuhan analisis sentimen. Ini sudah cocok dengan judul awal.

Yang tetap perlu diperbaiki:

- Ada kalimat yang kurang jelas: "penelitian ini difokuskan yang menjadi perhatian utama masyarakat dan kemudahan transaksi."
- Ada typo: "kecendurungan opisi" sebaiknya menjadi "kecenderungan opini".
- Penjelasan IndoBERT muncul berulang dan bisa diringkas agar tidak repetitif.
- Perlu ditambahkan satu kalimat bahwa ulasan pengguna dapat mencerminkan berbagai aspek layanan, seperti kemudahan penggunaan, performa aplikasi, transaksi, login, keamanan, dan kualitas layanan.

Aspek keamanan boleh disebut di latar belakang, tetapi cukup sebagai salah satu contoh isu penting dalam mobile banking. Tidak perlu dibuat seolah-olah seluruh penelitian hanya meneliti keamanan.

### 2. Rumusan Masalah

Status: sudah sesuai secara dasar, tetapi perlu dilengkapi.

Rumusan masalah saat ini sudah sejalan dengan judul karena membahas klasifikasi sentimen menggunakan IndoBERT dan distribusi sentimen positif, negatif, dan netral.

Yang perlu ditambahkan:

- rumusan masalah tentang performa model IndoBERT;
- rumusan masalah tentang isu dominan dalam ulasan pengguna secara umum;
- jika ingin memasukkan aspek keamanan, tulis sebagai bagian dari isu dominan, bukan rumusan masalah utama.

Contoh rumusan masalah yang lebih sesuai:

1. Bagaimana metode IndoBERT digunakan untuk mengklasifikasikan sentimen ulasan pengguna aplikasi JakOne Mobile ke dalam kategori positif, negatif, dan netral?
2. Bagaimana performa model IndoBERT dalam melakukan klasifikasi sentimen ulasan pengguna JakOne Mobile berdasarkan metrik accuracy, precision, recall, dan F1-score?
3. Bagaimana distribusi sentimen dan isu dominan yang muncul dalam ulasan pengguna aplikasi JakOne Mobile?

Jika ingin menyebut keamanan:

4. Isu apa saja yang muncul dalam ulasan pengguna, termasuk isu akses, login, transaksi, OTP, verifikasi, dan keamanan akun?

Rumusan nomor 4 bersifat pendukung dan tidak harus menjadi rumusan utama jika BAB 1 ingin tetap ringkas.

### 3. Ruang Lingkup / Batasan Masalah

Status: sudah sesuai, tetapi perlu ditambah agar cocok dengan project.

Yang sudah sesuai:

- data berasal dari Google Play Store;
- objek penelitian adalah aplikasi JakOne Mobile;
- ulasan yang digunakan berbahasa Indonesia;
- metode utama adalah IndoBERT;
- label sentimen terdiri dari positif, negatif, dan netral.

Yang perlu ditambahkan:

- penelitian menggunakan data ulasan pengguna, bukan data internal Bank DKI;
- penelitian hanya melakukan analisis sentimen berbasis teks ulasan;
- penelitian tidak melakukan audit keamanan teknis, pengujian sistem, atau investigasi forensik;
- dataset yang digunakan untuk modeling memakai kolom utama `review`, `label`, dan `split_set`;
- data dibagi menjadi train, validation, dan test;
- hasil analisis keyword issue, termasuk isu keamanan, dipakai sebagai analisis pendukung.

Contoh batasan yang tepat:

Penelitian ini berfokus pada analisis sentimen ulasan pengguna aplikasi JakOne Mobile berdasarkan teks ulasan yang tersedia pada Google Play Store. Analisis dilakukan terhadap sentimen positif, negatif, dan netral menggunakan model IndoBERT. Pembahasan mengenai isu seperti login, OTP, verifikasi, transaksi, password, kendala akses, dan keamanan akun digunakan sebagai analisis tambahan berdasarkan kemunculan kata kunci dalam ulasan, bukan sebagai audit keamanan teknis terhadap sistem aplikasi.

### 4. Tujuan Penelitian

Status: sudah sesuai, perlu sedikit dilengkapi.

Tujuan dalam BAB 1 sudah selaras dengan judul karena mencakup klasifikasi sentimen, evaluasi model, distribusi sentimen, dan rekomendasi berbasis data.

Tambahan yang disarankan:

- menambahkan tujuan untuk mengidentifikasi isu dominan dalam ulasan pengguna secara umum;
- menambahkan bahwa analisis isu keamanan hanya bagian dari eksplorasi hasil, bukan tujuan utama.

Contoh tambahan tujuan:

Mengidentifikasi isu-isu dominan yang muncul dalam ulasan pengguna aplikasi JakOne Mobile sebagai analisis pendukung terhadap hasil klasifikasi sentimen.

### 5. Manfaat Penelitian

Status: belum terlihat sebagai subbab khusus dalam hasil ekstraksi BAB 1.

BAB 1 sebaiknya menambahkan subbab Manfaat Penelitian. Manfaat tidak perlu diarahkan khusus ke keamanan, tetapi ke analisis sentimen dan evaluasi layanan aplikasi.

Contoh manfaat:

- Bagi akademik, penelitian ini dapat menjadi referensi penerapan IndoBERT untuk analisis sentimen ulasan aplikasi mobile banking berbahasa Indonesia.
- Bagi pengembang atau pengelola layanan, hasil penelitian dapat membantu memahami persepsi pengguna terhadap aplikasi JakOne Mobile.
- Bagi penelitian selanjutnya, pipeline preprocessing, labeling, fine-tuning IndoBERT, evaluasi, dan visualisasi dashboard dapat menjadi acuan pengembangan analisis sentimen berbasis ulasan pengguna.

### 6. Sistematika Penulisan

Status: cukup sesuai.

Bagian sistematika sudah menjelaskan isi Bab 1 sampai Bab 5. Namun, ada kemungkinan hasil ekstraksi menjadikan paragraf Bab 2, Bab 3, Bab 4, dan Bab 5 sebagai heading markdown karena format DOCX. Secara isi, sistematika masih dapat dipakai.

## Hal Project yang Tetap Perlu Tertulis di BAB 1

- Data berasal dari ulasan pengguna aplikasi JakOne Mobile di Google Play Store.
- Penelitian melakukan klasifikasi sentimen positif, negatif, dan netral.
- IndoBERT digunakan sebagai metode utama.
- Preprocessing teks Bahasa Indonesia dilakukan sebelum pemodelan.
- Pelabelan awal dilakukan menggunakan lexicon.
- Validasi atau perbaikan label dilakukan untuk meningkatkan kualitas dataset.
- Dataset dibagi menjadi train, validation, dan test.
- Evaluasi model menggunakan accuracy, precision, recall, dan F1-score.
- Dashboard digunakan untuk visualisasi dan demo prediksi sebagai pelengkap hasil penelitian.

## Hal yang Tidak Perlu Terlalu Ditekankan

- Jangan menjadikan aspek keamanan sebagai fokus utama judul.
- Jangan membuat rumusan masalah utama hanya tentang keamanan.
- Jangan membuat tujuan utama penelitian menjadi analisis OTP, login, password, atau verifikasi saja.
- Jangan membuat BAB 1 terlihat seperti penelitian audit keamanan aplikasi.
- Jangan terlalu banyak membahas dugaan peretasan atau insiden keamanan jika tidak menjadi data utama penelitian.

Aspek keamanan cukup disebut sebagai salah satu jenis isu yang dapat muncul dalam ulasan pengguna mobile banking dan dianalisis melalui keyword issue/dashboard.

## Cara Menulis Aspek Keamanan sebagai Fitur Tambahan

Gunakan frasa seperti:

- "sebagai analisis pendukung";
- "sebagai bagian dari eksplorasi isu dominan";
- "sebagai salah satu kategori isu dalam ulasan pengguna";
- "untuk memperkaya interpretasi hasil sentimen";
- "bukan sebagai audit keamanan teknis".

Contoh kalimat siap tempel:

Selain melihat distribusi sentimen secara umum, penelitian ini juga melakukan analisis pendukung terhadap isu-isu yang sering muncul dalam ulasan pengguna, seperti transaksi, login, OTP, verifikasi, akun, password, kendala akses, dan error aplikasi. Analisis ini digunakan untuk memperkaya interpretasi hasil sentimen, bukan sebagai audit keamanan teknis terhadap sistem JakOne Mobile.

Contoh kalimat untuk batasan masalah:

Pembahasan mengenai aspek keamanan dalam penelitian ini dibatasi pada kemunculan isu atau kata kunci dalam ulasan pengguna, seperti OTP, login, akun, verifikasi, transaksi, password, dan kendala akses. Penelitian ini tidak melakukan pengujian keamanan sistem, analisis infrastruktur, maupun investigasi terhadap data internal aplikasi.

Contoh kalimat untuk dashboard:

Dashboard yang dibangun dalam penelitian ini berfungsi sebagai media visualisasi hasil analisis sentimen, evaluasi model, distribusi dataset, word cloud, keyword issue, serta demo prediksi. Fitur keyword issue dapat digunakan untuk melihat isu tertentu, termasuk isu akses dan keamanan, sebagai pelengkap interpretasi hasil.

## Kesimpulan Revisi Penilaian

BAB 1 tidak perlu diarahkan ulang menjadi penelitian khusus aspek keamanan. Secara garis besar, BAB 1 sudah sesuai dengan judul awal "Analisis Sentimen Ulasan Pengguna Aplikasi JakOne Mobile Menggunakan IndoBERT". Revisi yang dibutuhkan adalah memperkuat hubungan BAB 1 dengan pipeline project aktual dan menambahkan manfaat penelitian, bukan mengganti fokus penelitian.

Aspek keamanan sebaiknya tetap disebut secara proporsional sebagai salah satu isu dalam ulasan pengguna dan fitur analisis tambahan pada dashboard. Dengan posisi tersebut, BAB 1 tetap konsisten dengan judul utama sekaligus tetap mencerminkan fitur tambahan yang sudah dikerjakan dalam project.

