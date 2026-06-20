# **4. Hasil dan Pembahasan**

## **4.1 Hasil Pengumpulan Data**

Proses pengumpulan data dilakukan dengan mengambil ulasan pengguna
aplikasi JakOne Mobile yang tersedia di Google Play Store, sebagaimana
ditunjukkan pada Gambar 4.1 berikut.

![](media/image1.png){width="6.268055555555556in"
height="2.2152777777777777in"}

Gambar 4.1 Halaman Aplikasi JakOne Mobile pada Google Play Store

Pengambilan data ini menggunakan pustaka google-play-scraper dengan
teknik penyortiran tertentu untuk menjaga kualitas data yang diperoleh.
Dari total sekitar 21.600 ulasan pengguna yang tersedia, diperoleh
sebanyak 14.272 ulasan terbaru pada rentang waktu tahun 2022 hingga
2026. Ulasan dikumpulkan dengan konfigurasi khusus, yaitu hanya ulasan
berbahasa Indonesia (lang=\'id\') yang berasal dari pengguna berdomisili
di Indonesia (country=\'id\'). Proses scraping dilakukan pada lingkungan
Visual Studio Code yang mendukung eksekusi Python. Pustaka diakses
melalui perintah import google_play_scraper, dengan ID aplikasi
dideklarasikan melalui app_id = \'com.dev.jakone.mbanking\'.

Tahapan selanjutnya adalah pengambilan data ulasan pengguna aplikasi
JakOne Mobile sebanyak 14.272 ulasan, dengan batasan berbahasa Indonesia
dan rentang waktu tahun 2022 hingga 2026. Data hasil scraping disimpan
dalam bentuk DataFrame, yaitu format penyimpanan data tabular yang
memudahkan proses analisis lebih lanjut. Struktur DataFrame ini
memungkinkan data difilter, dikelompokkan, dan dianalisis secara lebih
efisien pada tahapan berikutnya.

## **4.2 Hasil Prepocessing Data** 

Proses preprocessing data dilakukan secara berurutan sesuai dengan
tahapan yang telah dirancang dan dijelaskan pada bab sebelumnya. Tahapan
ini bertujuan membersihkan data mentah yang mengandung banyak noise
serta elemen teks yang tidak relevan, sehingga dihasilkan kumpulan data
yang bersih, terstruktur, dan siap digunakan pada proses-proses
selanjutnya. Hasil dari setiap tahapan preprocessing tersebut dijelaskan
secara lebih rinci pada subbab-subbab berikut.

### **4.2.1 Case Folding** 

Tahapan pertama dalam proses preprocessing data adalah case folding,
yaitu mengubah seluruh teks ulasan pada dataset menjadi huruf kecil
(lowercase) secara menyeluruh. Proses ini dilakukan terhadap 14.272 data
sehingga tidak ada perubahan pada total data ulasan yang diproses.
Perubahan yang terjadi hanya pada bentuk penulisan kata, yaitu
menyamakan seluruh karakter alfabet tanpa menghilangkan atau menambahkan
kata baru ke dalam data ulasan.

Tabel 4.1 Contoh Hasil Case Folding

  -------------------------------------------------------
  **Ulasan Awal**              **Hasil *Case Folding***
  ---------------------------- --------------------------
  Aplikasi Sering ERROR saat   aplikasi sering error saat
  login                        login

  JakOne Mobile Sangat         jakone mobile sangat
  Membantu                     membantu

  Tidak Bisa Masuk Akun        tidak bisa masuk akun
  -------------------------------------------------------

### **4.2.2 Cleansing** 

Setelah tahapan case folding, proses preprocessing dilanjutkan dengan
cleansing atau pembersihan data. Pada tahapan ini ditemukan berbagai
elemen non-teks dalam dokumen ulasan pengguna, seperti emoji, tautan
URL, sebutan akun (mention), simbol tertentu, dan angka. Seluruh elemen
tersebut dihapus dari dataset karena tidak membawa informasi yang
representatif untuk analisis sentimen. Dengan penghapusan ini, struktur
teks ulasan menjadi lebih berfokus pada teks murni dari pengguna,
sehingga noise yang berpotensi mengganggu akurasi analisis pada tahap
berikutnya dapat dikurangi.

Tabel 4.2 Contoh Hasil Cleansing

  -----------------------------------------------------
  **Hasil *Case Folding***    **Hasil *Cleansing***
  --------------------------- -------------------------
  aplikasi error!!! tolong    aplikasi error tolong
  diperbaiki                  diperbaiki

  gak bisa login akun saya??? gak bisa login akun saya

  aplikasi bagus banget 😊    aplikasi bagus banget
  -----------------------------------------------------

### **4.2.3 Normalisasi Kata**

Tahapan selanjutnya setelah pembersihan data adalah normalisasi kata.
Pada tahapan ini ditemukan banyak kosakata tidak baku, bahasa gaul
(slang), serta penyingkatan kata yang digunakan pengguna saat menulis
ulasan. Banyaknya variasi penulisan yang tidak sesuai standar dapat
meningkatkan jumlah kosakata unik (vocabulary size) secara semu dan
mengurangi konsistensi makna asli teks. Oleh karena itu, normalisasi
kata bertujuan menyeragamkan kata-kata tidak baku ke dalam bentuk baku
yang sesuai dengan Kamus Besar Bahasa Indonesia (KBBI).

Tabel 4.3 Contoh Hasil Normalisasi Kata

  --------------------------------------------
  **Hasil             **Hasil Normalisasi**
  *Cleansing***       
  ------------------- ------------------------
  apk nya gk bisa     aplikasi nya tidak bisa
  dibuka              dibuka

  yg ini sering error yang ini sering error

  tdk bisa login dari tidak bisa login dari
  tadi                tadi
  --------------------------------------------

### **4.2.4 Stepword Removal** 

Tahapan berikutnya setelah normalisasi kata adalah stopword removal,
yaitu proses penghapusan kata-kata yang sering muncul dalam suatu bahasa
namun tidak memberikan kontribusi signifikan terhadap informasi teks,
seperti kata hubung, kata depan, dan kata ganti. Setelah kata-kata
fungsional tersebut dieliminasi, struktur teks ulasan menjadi lebih
didominasi oleh kata sifat, kata kerja, dan kata benda yang spesifik.
Hal ini mempermudah model dalam mengenali pola teks karena informasi
yang tersisa memiliki bobot konteks yang lebih tinggi. Meski demikian,
daftar stopword tetap mempertahankan kata negasi seperti \"tidak\",
\"belum\", dan \"kurang\", karena penghapusan kata-kata tersebut
berisiko mengubah makna sentimen secara fatal.

Tabel 4.4 Contoh Hasil Stopword Removal

  -------------------------------------------------------------
  **Hasil Normalisasi**           **Hasil Stopword Removal**
  ------------------------------- -----------------------------
  saya tidak bisa login ke akun   tidak bisa login akun

  fitur yang tersedia cukup       fitur tersedia cukup lengkap
  lengkap                         

  aplikasi ini sangat membantu    aplikasi sangat membantu
  pengguna                        pengguna
  -------------------------------------------------------------

### **4.2.5 Penghapusan Data Kosong dan Duplikasi** 

Setelah melalui seluruh rangkaian tahapan preprocessing teks, mulai
dari case folding hingga stopword removal, dilakukan evaluasi akhir
berupa penghapusan data kosong dan duplikasi. Data kosong terjadi karena
ulasan pengguna hanya terdiri dari elemen non-teks, seperti emoji,
angka, atau simbol, yang telah dibersihkan pada tahap cleansing.
Sementara itu, data duplikat ditemukan akibat pengiriman ulasan yang
sama secara berulang oleh pengguna.

Berdasarkan hasil eliminasi, terdapat sebanyak 100 data ulasan kosong
(yang terhapus setelah melalui proses cleansing dan stopword removal)
dan 0 data duplikat (karena penyaringan duplikasi ulasan sudah disaring
terlebih dahulu pada tahap scraping awal) yang dihapus dari dataset.
Secara akumulatif, total data yang dihapus tersebut mewakili
sekitar 0,70% dari keseluruhan data awal (14.272 ulasan) yang digunakan.
Pengurangan ini merupakan bagian dari proses penyaringan kualitas data
untuk memastikan efektivitas dan efisiensi pada tahap berikutnya,
sehingga memberikan dampak positif terhadap kualitas dataset secara
keseluruhan

## **4.3 Hasil Pelabelan Sentimen** 

Gambar 4.2 Distribusi Sentimen Ulasan Pengguna JakOne Mobile

Hasil analisis sentimen terhadap 14.172 data ulasan menunjukkan bahwa
opini pengguna didominasi oleh sentimen positif sebesar 59,48% (8.421
ulasan), diikuti sentimen negatif sebesar 32,48% (4.605 ulasan), serta
sentimen netral sebagai kelompok minoritas dengan 8,04% (1.146 ulasan).
Tingginya persentase sentimen positif mengindikasikan bahwa secara umum
mayoritas pengguna memberikan respons positif terhadap fungsionalitas
aplikasi JakOne Mobile.

Namun, angka sentimen negatif yang mencapai 32,48% dari keseluruhan data
merupakan temuan yang perlu diperhatikan. Dalam konteks evaluasi
aplikasi, khususnya pada aspek krusial seperti layanan dari sisi
transaksi keuangan dan keamanan, hal ini menjadi titik permasalahan
utama (critical pain point), dengan keluhan pengguna yang umumnya
berkaitan dengan kendala teknis, kekhawatiran privasi, atau kegagalan
sistem.

Hasil mengenai permasalahan utama (critical pain points) pengguna ini
diperkuat dengan analisis frekuensi kata kunci pada ulasan berlabel
negatif. Ditemukan bahwa keluhan pengguna didominasi oleh kendala fungsi
transfer dana dengan kata kunci \'transfer\' (muncul sebanyak 924 kali),
kegagalan teknis sistem dengan kata kunci \'error\' (598 kali)
dan \'gagal\' (413 kali), tingkat kemudahan akses dengan
kata \'susah\' (485 kali), serta hambatan autentikasi masuk dengan kata
kunci \'login\' (451 kali) dan \'otp\' (351 kali)

Di sisi lain, minimnya ulasan bersentimen netral sebesar 8,04%
mengindikasikan adanya kecenderungan perilaku penggguna (user behavior)
dimana pengguna menuliskan ulasan di platform Google Play hanya ketika
merasakan pengalaman yang memuaskan atau justru mengecewakan, sehingga
menyisakan sedikit ruang bagi opini pengguna yang bersifat biasa saja
atau ambigu. Kondisi ini juga didapat dari data penilaian bintang (star
rating) di mana ulasan dengan rating menengah (bintang 3) sangat sedikit
dibandingkan dengan ulasan yang memiliki rating ekstrem, yaitu 5 untuk
kepuasan tertingi atau rating bintang 1 untuk keluhan sistem.

Tabel 4.5 Tabulasi Silang Label Sentimen dengan Rating Bintang

  ---------------------------------------------------------------------------
  Label         Bintang 1 Bintang 2 Bintang 3 Bintang 4 Bintang 5 Total
  Sentimen                                                        Ulasan
  ------------- --------- --------- --------- --------- --------- -----------
  Negatif       3.358     472       356       108       311       4.605

  Netral        502       82        97        62        403       1.146

  Positif       861       202       182       182       6.994     8.421

  23            4.721     756       635       352       7.708     14.172
  ---------------------------------------------------------------------------

Berdasarkan hasil analisis tabulasi silang pada Tabel di atas, terlihat
bahwa data didominasi oleh rating ekstrem, yaitu rating bintang 5 (7.708
ulasan atau 54,39%) dan bintang 1 (4.721 ulasan atau 33,31%).
Sebaliknya, rating menengah yaitu bintang 3 hanya berjumlah 635
ulasan (4,48% dari keseluruhan data). Hal ini membuktikan hipotesis
bahwa pengguna cenderung mengekspresikan opini secara tertulis hanya
saat mereka mengalami kepuasan maksimal (sentimen positif yang
berkorelasi dengan 83,05% rating bintang 5) atau kekecewaan mendalam
(sentimen negatif yang berkorelasi dengan 72,92% rating bintang 1)

## **4.4 Distribusi Dataset dan Pembagian Data** 

Setelah proses pelabelan sentimen menggunakan InSet Lexicon selesai
dilakukan terhadap 14.172 data hasil preprocessing, diperoleh distribusi
label sentimen yang terdiri dari tiga kelas, yaitu positif, negatif, dan
netral. Dominasi sentimen positif pada dataset ulasan JakOne Mobile ini
sejalan dengan karakteristik umum ulasan aplikasi pada platform Google
Play Store, di mana pengguna dengan pengalaman positif maupun pengguna
yang baru saja mengunduh aplikasi cenderung lebih banyak memberikan
ulasan dibandingkan pengguna dengan pengalaman netral atau biasa-biasa
saja.

Dataset yang telah diberi label selanjutnya dibagi menjadi tiga subset,
yaitu data latih (train), data validasi (validation), dan data uji
(test), dengan rasio pembagian 80:10:10. Pembagian data dilakukan secara
stratified, yaitu dengan menjaga proporsi setiap label sentimen agar
tetap konsisten pada masing-masing subset. Pendekatan ini dipilih agar
data validasi dan data uji tetap merepresentasikan distribusi populasi
data secara keseluruhan, termasuk kelas netral yang jumlahnya relatif
kecil. Rincian pembagian data berdasarkan label sentimen disajikan pada
Tabel 4.6.

Tabel 4.6 Pembagian Data Train, Validation, dan Test Berdasarkan Label
Sentimen

  -----------------------------------------------------
  Label Sentimen Train (80%) Validation      Test (10%)
                             (10%)           
  -------------- ----------- --------------- ----------
  Positif        6.737       842             842

  Negatif        3.685       460             460

  Netral         916         115             115

  Total          11.338      1.417           1.417
  -----------------------------------------------------

Tabel 4.7 menyajikan rekapitulasi jumlah dan persentase keseluruhan data
pada masing-masing subset tanpa memperhatikan distribusi label.

Tabel 4.7 Rekapitulasi Jumlah Data Train, Validation, dan Test

  -------------------------------------
  Jenis Data   Jumlah Data Persentase
  ------------ ----------- ------------
  Train        11.338      80,00%

  Validation   1.417       10,00%

  Test         1.417       10,00%

  Total        14.172      100,00%
  -------------------------------------

Berdasarkan Tabel 4.6, proporsi setiap label sentimen pada subset train,
validation, dan test relatif konsisten dengan proporsi pada dataset
keseluruhan, dengan selisih yang tidak signifikan pada setiap kelas.
Konsistensi ini membuktikan bahwa proses pembagian data secara
stratified berhasil mempertahankan karakteristik distribusi populasi
pada setiap subset, sehingga performa model yang akan dievaluasi pada
data validation dan test dapat dianggap merepresentasikan performa model
pada data dengan distribusi yang serupa dengan data latih. Subset train
yang berjumlah 11.338 data digunakan sebagai data pembelajaran utama
bagi model, subset validation yang berjumlah 1.417 data digunakan untuk
memantau performa model selama proses pelatihan, dan subset test yang
berjumlah 1.417 data digunakan sebagai evaluasi akhir terhadap model
yang telah dilatih

## **4.5 Hasil Penelitihan Model IndoBERT** 

Subbab ini menjelaskan hasil dari proses pelatihan model klasifikasi
sentimen berbasis IndoBERT, mulai dari persiapan data pelatihan,
konfigurasi model, proses training dan validasi, hingga interpretasi
umum terhadap hasil pelatihan yang diperoleh. Pembahasan mengenai
performa model secara kuantitatif terhadap data uji (test set), seperti
precision, recall, dan confusion matrix, akan disajikan secara terpisah
pada subbab evaluasi model.

### **4.5.1 Persiapan Data Pelatihan**

Sebelum proses pelatihan dilakukan, data hasil pembagian dataset yang
telah dijelaskan pada subbab 4.4 dipersiapkan dalam format yang sesuai
dengan kebutuhan arsitektur model IndoBERT. Data latih (train) dan data
validasi (validation) yang digunakan pada tahap ini disajikan kembali
secara ringkas pada Tabel 4.8.

**Tabel 4.8 Pembagian Data untuk Proses Pelatihan Model**

  -------------------------------------
  Jenis Data   Jumlah Data Persentase
  ------------ ----------- ------------
  Train        11.338      80,00%

  Validation   1.417       10,00%

  Test         1.417       10,00%
  -------------------------------------

Data test yang telah dipisahkan pada subbab 4.4 tidak digunakan dalam
tahap ini dan disimpan secara khusus untuk keperluan evaluasi akhir
model setelah proses pelatihan selesai dilakukan, guna menghindari
kebocoran data (data leakage) yang dapat menyebabkan estimasi performa
model menjadi bias.

Setiap data teks ulasan yang telah melalui tahapan preprocessing pada
subbab 4.2 selanjutnya dikonversi ke dalam format token menggunakan
tokenizer bawaan dari model IndoBERT, yaitu WordPiece Tokenizer, dengan
panjang token maksimum ditetapkan sebesar 128. Token yang dihasilkan
selanjutnya direpresentasikan dalam bentuk input_ids, attention_mask,
serta label sentimen yang telah dikodekan secara numerik (label
encoding), yaitu 0 untuk negatif, 1 untuk netral, dan 2 untuk positif

### **4.5.2 Konfigurasi Model IndoBERT**

Model yang digunakan dalam penelitian ini adalah IndoBERT Base, yaitu
model bahasa pre-trained berbasis arsitektur BERT yang telah dilatih
khusus menggunakan korpus berbahasa Indonesia berskala besar. Pada tahap
fine-tuning, lapisan output model ditambahkan sebuah lapisan klasifikasi
(classification head) yang disesuaikan dengan jumlah kelas sentimen pada
penelitian ini, yaitu tiga kelas: positif, negatif, dan netral.
Konfigurasi hyperparameter yang digunakan dalam proses fine-tuning
disajikan pada Tabel 4.9.

**Tabel 4.9 Konfigurasi Hyperparameter Model IndoBERT**

+-----------------------+----------------------------------------+
| **Parameter**         | **Nilai**                              |
+:======================+:=======================================+
| Model Dasar           | IndoBERT Base                          |
| (Pre-trained)         | (indobenchmark/indobert-base-p1)       |
+-----------------------+----------------------------------------+
| Jumlah Epoch          | **2**                                  |
+-----------------------+----------------------------------------+
| Batch Size            | **8**                                  |
+-----------------------+----------------------------------------+
| Learning Rate         |   --                                   |
|                       |                                        |
|                       |   --                                   |
|                       |                                        |
|                       |   -------------                        |
|                       |   **2e-05                              |
|                       |   (0,00002)**                          |
|                       |   -------------                        |
|                       |                                        |
|                       |   -------------                        |
+-----------------------+----------------------------------------+
| Optimizer             | **AdamW**                              |
+-----------------------+----------------------------------------+
| Maximum Sequence      | **128**                                |
| Length                |                                        |
+-----------------------+----------------------------------------+
| Jumlah Kelas Output   | 3 (Positif, Negatif, Netral)           |
+-----------------------+----------------------------------------+
| Loss Function         | **CrossEntropyLoss**                   |
+-----------------------+----------------------------------------+
| Perangkat Pelatihan   |   --                                   |
| (Device)              |                                        |
|                       |   --                                   |
|                       |                                        |
|                       |   -----------                          |
|                       |   **CUDA                               |
|                       |   (GPU)**                              |
|                       |   -----------                          |
|                       |                                        |
|                       |   -----------                          |
+-----------------------+----------------------------------------+

Pemilihan nilai 2e-5 sebagai nilai learning rate serta penggunaan
optimizer AdamW didasarkan pada konfigurasi yang umum digunakan dalam
proses fine-tuning model berbasis BERT, dengan pertimbangan terhadap
stabilitas konvergensi serta efisiensi waktu pelatihan. Jumlah epoch
yang relatif sedikit, yaitu dua epoch, dipilih untuk menyesuaikan dengan
karakteristik fine-tuning model pre-trained berskala besar seperti
IndoBERT, yang umumnya telah memiliki representasi bahasa yang kuat
sehingga tidak memerlukan jumlah epoch yang banyak untuk mencapai
konvergensi pada tugas klasifikasi spesifik.

### **4.5.3 Proses Training dan Validasi**

Proses pelatihan model dilakukan sebanyak dua epoch menggunakan data
latih yang telah dipersiapkan pada subbab 4.5.1. Pada setiap akhir
epoch, model dievaluasi menggunakan data validasi untuk memantau
perkembangan proses pembelajaran serta mendeteksi kemungkinan terjadinya
overfitting maupun underfitting. Proses pelatihan dijalankan pada
perangkat GPU berbasis CUDA.

Nilai training loss dan validation loss yang diperoleh pada setiap epoch
selama proses pelatihan dicatat dan disajikan pada Tabel 4.10, beserta
nilai validation accuracy dan validation F1 macro sebagai indikator
tambahan untuk memantau perkembangan performa model pada data validasi
dari waktu ke waktu.

**Tabel 4.10 Riwayat Training Loss dan Validation Loss Tiap Epoch**

+-----------+------------------+----------------+---------------------+
| **Epoch** | **Training       | **Validation   |   --                |
|           | Loss**           | Loss**         |                     |
|           |                  |                |   --                |
|           |                  |                |                     |
|           |                  |                |   ----------------- |
|           |                  |                |   **Validation      |
|           |                  |                |   Macro F1**        |
|           |                  |                |   ----------------- |
|           |                  |                |                     |
|           |                  |                |   ----------------- |
+:=========:+==================+================+=====================+
| 1         |   --             | **89,98%**     |   --                |
|           |                  |                |                     |
|           |   --             |                |   --                |
|           |                  |                |                     |
|           |   -------------- |                |   ------------      |
|           |   **0,340807**   |                |   **84,42%**        |
|           |   -------------- |                |   ------------      |
|           |                  |                |                     |
|           |   -------------- |                |   ------------      |
+-----------+------------------+----------------+---------------------+
| 2         | **0,306358**     |   --           |   --                |
|           |                  |                |                     |
|           |                  |   --           |   --                |
|           |                  |                |                     |
|           |                  |   ------------ |   ------------      |
|           |                  |   **91,95%**   |   **86,81%**        |
|           |                  |   ------------ |   ------------      |
|           |                  |                |                     |
|           |                  |   ------------ |   ------------      |
+-----------+------------------+----------------+---------------------+

Berdasarkan riwayat pelatihan yang tercatat pada Tabel 4.10, training
loss menunjukkan nilai sebesar 0,2983 pada epoch pertama dan mengalami
penurunan menjadi 0,2079 pada epoch kedua. Penurunan training loss ini
mengindikasikan bahwa model secara konsisten semakin baik dalam
mempelajari pola dari data latih pada setiap epoch yang dilalui.

Sejalan dengan penurunan training loss, validation loss juga menunjukkan
tren penurunan dari 0,3408 pada epoch pertama menjadi 0,3064 pada epoch
kedua. Penurunan validation loss yang searah dengan training loss ini
merupakan indikator penting, karena menunjukkan bahwa peningkatan
kemampuan model dalam mempelajari data latih juga diikuti oleh
peningkatan kemampuan generalisasi model terhadap data validasi yang
belum pernah dipelajari sebelumnya.

Selain kedua nilai loss tersebut, metrik validation accuracy dan
validation F1 macro juga menunjukkan peningkatan pada setiap epoch.
Validation accuracy meningkat dari 89,98% pada epoch pertama menjadi
91,95% pada epoch kedua, sementara validation F1 macro meningkat dari
84,42% menjadi 86,81% pada periode yang sama. Peningkatan F1 macro yang
konsisten dengan peningkatan accuracy menunjukkan bahwa peningkatan
performa model tidak hanya terjadi pada kelas mayoritas, tetapi juga
turut dirasakan secara proporsional pada kelas-kelas sentimen lainnya,
termasuk kelas netral yang memiliki jumlah data lebih sedikit
sebagaimana telah dijelaskan pada subbab 4.4.

### **4.5.4 Interpretasi Umum Hasil Pelatihan**

Berdasarkan riwayat training loss dan validation loss yang diperoleh
pada Tabel 4.10, dapat diinterpretasikan bahwa proses pembelajaran model
secara umum berjalan stabil dan tidak menunjukkan indikasi overfitting
pada kedua epoch yang dilalui. Indikasi ini terlihat dari pola penurunan
validation loss yang searah dengan penurunan training loss, alih-alih
validation loss yang stagnan atau justru meningkat seiring penurunan
training loss, yang umumnya menjadi tanda model mulai menghafal data
latih (overfitting) tanpa diikuti peningkatan kemampuan generalisasi.

Selisih antara training loss dan validation loss pada epoch kedua, yaitu
sebesar 0,0985, masih berada dalam rentang yang wajar mengingat proses
fine-tuning hanya dilakukan dalam dua epoch. Selisih ini menunjukkan
bahwa model belum menunjukkan kecenderungan untuk menghafal data latih
secara berlebihan, namun demikian pemantauan lebih lanjut tetap
diperlukan apabila jumlah epoch ditambah pada eksperimen selanjutnya,
mengingat selisih ini berpotensi melebar apabila pelatihan dilanjutkan
tanpa mekanisme regularisasi tambahan.

Apabila pada eksperimen lanjutan ditemukan indikasi overfitting, seperti
validation loss yang mulai meningkat sementara training loss terus
menurun, perlu dipertimbangkan penerapan teknik regularisasi tambahan,
seperti early stopping, dropout, atau pembatasan jumlah epoch pelatihan.
Sebaliknya, mengingat kedua nilai loss pada penelitian ini masih
menunjukkan tren penurunan yang konsisten hingga epoch terakhir tanpa
tanda-tanda stagnasi, terdapat kemungkinan bahwa performa model masih
dapat ditingkatkan lebih lanjut apabila jumlah epoch pelatihan ditambah
pada penelitian selanjutnya.

Secara umum, proses fine-tuning model IndoBERT pada penelitian ini
berhasil menghasilkan model yang konvergen dan stabil, sebagaimana
tercermin dari pola penurunan training loss dan validation loss yang
konsisten, serta peningkatan validation accuracy dan validation F1 macro
pada setiap epoch yang dilalui. Hasil model yang telah dilatih pada
tahap ini selanjutnya akan dievaluasi secara lebih mendalam menggunakan
data test pada subbab evaluasi model berikutnya.

## **4.6 Evaluasi Model**

Setelah proses pelatihan model IndoBERT selesai dilakukan sebagaimana
telah dijelaskan pada subbab 4.5, tahap selanjutnya adalah melakukan
evaluasi performa model menggunakan data uji (test set) yang berjumlah
1.418 data dan belum pernah digunakan pada proses pelatihan maupun
validasi. Evaluasi menggunakan data uji ini bertujuan untuk mengukur
kemampuan generalisasi model dalam mengklasifikasikan sentimen pada data
baru yang belum pernah dipelajari sebelumnya, sehingga hasil evaluasi
dapat dianggap merepresentasikan performa model pada kondisi penggunaan
yang sesungguhnya.

Evaluasi dilakukan dengan menghitung sejumlah metrik klasifikasi
standar, yaitu accuracy, precision, recall, dan F1-score, baik secara
keseluruhan maupun pada masing-masing kelas sentimen. Selain itu, hasil
prediksi model juga dianalisis melalui confusion matrix untuk memperoleh
gambaran yang lebih rinci mengenai pola kesalahan klasifikasi yang
terjadi pada setiap kelas.

### **4.6.1 Hasil Evaluasi Metrik Keseluruhan**

Hasil evaluasi model pada data uji secara keseluruhan disajikan pada
Tabel 4.11 berikut.

**Tabel 4.11 Hasil Metrik Evaluasi Model pada Data Uji**

  ----------------------------------- -----------------------------------
          **Metrik Evaluasi**                      **Nilai**

               Accuracy                         0,9316 (93,16%)

            Macro Precision                     0,8928 (89,28%)

             Macro Recall                       0,8669 (86,69%)

            Macro F1-Score                      0,8774 (87,74%)

           Weighted F1-Score                    0,9309 (93,09%)
  ----------------------------------- -----------------------------------

Berdasarkan Tabel 4.11, model IndoBERT yang telah dilatih memperoleh
nilai accuracy sebesar 0,9316 atau 93,16%, yang menunjukkan bahwa dari
keseluruhan data uji, sebagian besar ulasan berhasil diklasifikasikan ke
kelas sentimen yang sesuai. Nilai accuracy ini menunjukkan bahwa model
memiliki performa yang baik secara umum dalam melakukan klasifikasi
sentimen pada dataset yang digunakan.

Selain accuracy, model memperoleh nilai macro precision sebesar 0,8928,
macro recall sebesar 0,8669, dan macro F1-score sebesar 0,8774. Nilai
macro average dihitung dengan memberikan bobot yang sama pada setiap
kelas tanpa mempertimbangkan jumlah data pada masing-masing kelas,
sehingga metrik ini memberikan gambaran yang lebih objektif terhadap
performa model pada seluruh kelas, termasuk kelas netral yang memiliki
jumlah data jauh lebih kecil dibandingkan kelas positif dan negatif.

Sementara itu, nilai weighted F1-score tercatat sebesar 0,9309, yang
lebih tinggi dibandingkan macro F1-score sebesar 0,8774. Selisih ini
terjadi karena perhitungan weighted F1-score mempertimbangkan proporsi
jumlah data pada setiap kelas, sehingga performa model yang baik pada
kelas mayoritas, yaitu kelas positif dan negatif, memberikan kontribusi
yang lebih besar terhadap nilai weighted F1-score. Selisih sebesar
0,0535 antara macro F1-score dan weighted F1-score ini mengindikasikan
adanya pengaruh ketidakseimbangan distribusi kelas terhadap hasil
evaluasi, sebagaimana telah dijelaskan pada subbab 4.4, di mana performa
model belum sepenuhnya merata pada seluruh kelas meskipun accuracy dan
weighted F1-score menunjukkan nilai yang tinggi.

### **4.6.2 Classification Report per Kelas Sentimen**

Untuk memperoleh gambaran performa model secara lebih rinci pada
masing-masing kelas sentimen, dilakukan analisis classification report
yang menyajikan nilai precision, recall, dan F1-score untuk setiap
kelas. Hasil classification report disajikan pada Tabel 4.12.

**Tabel 4.12 Classification Report Model IndoBERT per Kelas Sentimen**

  ----------------- ----------------- ----------------- -----------------
       **Kelas        **Precision**      **Recall**       **F1-Score**
     Sentimen**                                         

       Positif           0,9768            0,9490            0,9627

       Negatif           0,8787            0,9588            0,9170

       Netral            0,8229            0,6930            0,7524

  **Macro Average**    **0,8928**        **0,8669**        **0,8774**
  ----------------- ----------------- ----------------- -----------------

Pada kelas positif, model memperoleh nilai precision sebesar 0,9768,
recall sebesar 0,9490, serta F1-score sebesar 0,9627. Nilai precision
yang sangat tinggi menunjukkan bahwa sebagian besar ulasan yang
diprediksi model sebagai positif memang benar-benar merupakan ulasan
positif, sementara nilai recall yang juga tinggi menunjukkan bahwa model
mampu menemukan sebagian besar data positif yang sebenarnya pada data
uji. Dengan F1-score sebesar 0,9627, kelas positif menjadi kelas dengan
performa terbaik di antara ketiga kelas sentimen, yang sejalan dengan
dominasi jumlah data positif sebagai kelas mayoritas pada dataset,
sebagaimana telah dijelaskan pada subbab 4.4.

Pada kelas negatif, diperoleh nilai precision sebesar 0,8787, recall
sebesar 0,9588, dan F1-score sebesar 0,9170. Nilai recall yang tinggi
menunjukkan bahwa model sangat baik dalam menangkap ulasan negatif,
yaitu sebagian besar ulasan yang benar-benar bersentimen negatif
berhasil diklasifikasikan dengan tepat. Namun, nilai precision pada
kelas negatif yang lebih rendah dibandingkan kelas positif menunjukkan
bahwa masih terdapat sejumlah ulasan dari kelas lain, khususnya netral,
yang turut diprediksi sebagai negatif. Kondisi ini dapat terjadi karena
beberapa ulasan mengandung kata-kata bernada keluhan, seperti "tidak
bisa", "gagal", "error", atau "transfer", meskipun label aktualnya tidak
selalu negatif, sehingga model cukup sensitif terhadap pola bahasa yang
mengandung indikasi masalah.

Pada kelas netral, model memperoleh nilai precision sebesar 0,8229,
recall sebesar 0,6930, serta F1-score sebesar 0,7524, yang menjadikan
kelas netral sebagai kelas dengan performa paling rendah di antara
ketiga kelas sentimen. Nilai recall yang relatif rendah menunjukkan
bahwa model belum sepenuhnya mampu mengenali seluruh ulasan netral
dengan baik, sehingga sebagian ulasan netral masih diklasifikasikan ke
kelas negatif maupun positif. Hal ini sejalan dengan ekspektasi yang
muncul akibat ketidakseimbangan kelas (class imbalance) yang telah
dijelaskan pada subbab 4.4, mengingat kelas netral memiliki jumlah data
paling sedikit pada dataset penelitian ini sehingga model memiliki lebih
sedikit contoh untuk mempelajari pola bahasa pada kelas tersebut. Selain
faktor jumlah data, karakteristik bahasa pada ulasan netral yang
cenderung lebih ambigu, seperti berupa pertanyaan, informasi singkat,
atau pernyataan yang tidak secara eksplisit menunjukkan sentimen kuat,
turut menyulitkan model dalam membedakannya dari kelas positif maupun
negatif.

Secara umum, perbandingan nilai F1-score antarkelas pada Tabel 4.12
menunjukkan bahwa model paling kuat dalam mengenali kelas positif,
diikuti oleh kelas negatif, sementara kelas netral menjadi kelas dengan
performa paling lemah. Pola ini mengindikasikan bahwa model lebih
efektif dalam mengenali sentimen dengan ekspresi yang jelas, baik
positif maupun negatif, dibandingkan sentimen netral yang cenderung
lebih samar dan bergantung pada konteks kalimat, yang pada penelitian
ini juga berkaitan erat dengan jumlah data latih yang tersedia untuk
masing-masing kelas selama proses pelatihan model pada subbab 4.5.

### **4.6.3 Analisis Confusion Matrix**

Untuk memperoleh gambaran yang lebih mendalam mengenai pola kesalahan
klasifikasi yang dilakukan oleh model, dilakukan analisis confusion
matrix yang menunjukkan distribusi hasil prediksi model terhadap label
sentimen yang sebenarnya (ground truth) pada data uji. Baris pada
confusion matrix menunjukkan label aktual, sedangkan kolom menunjukkan
label hasil prediksi model. Hasil confusion matrix disajikan pada Tabel
4.13.

**Tabel 4.13 Confusion Matrix Hasil Prediksi Model IndoBERT pada Data
Uji**

  ----------------- ----------------- ----------------- -----------------
     **Aktual \\       **Negatif**       **Netral**        **Positif**
     Prediksi**                                         

     **Negatif**         **442**             10                 9

     **Netral**            25              **79**              10

     **Positif**           36                 7              **800**
  ----------------- ----------------- ----------------- -----------------

Berdasarkan Tabel 4.13, dari 461 data aktual berlabel negatif, sebanyak
442 data berhasil diprediksi dengan benar sebagai negatif, sedangkan
hanya 10 data yang diprediksi sebagai netral dan 9 data yang diprediksi
sebagai positif. Hal ini menunjukkan bahwa model memiliki kemampuan yang
baik dalam mengenali ulasan negatif, sejalan dengan nilai recall kelas
negatif yang tinggi pada Tabel 4.12.

Pada kelas positif, dari 843 data aktual berlabel positif, sebanyak 800
data berhasil diprediksi dengan benar sebagai positif, sementara 36 data
diprediksi sebagai negatif dan 7 data diprediksi sebagai netral. Secara
umum, jumlah kesalahan pada kelas positif relatif kecil dibandingkan
jumlah data positif secara keseluruhan. Namun, adanya 36 data positif
yang diprediksi sebagai negatif menunjukkan bahwa beberapa ulasan
positif kemungkinan mengandung kata-kata yang secara leksikal
berasosiasi dengan keluhan atau masalah teknis, sehingga model
mengarahkannya ke kelas negatif.

Pola kesalahan paling menonjol terlihat pada kelas netral. Dari 114 data
aktual berlabel netral, hanya 79 data yang berhasil diprediksi dengan
benar sebagai netral, sedangkan 25 data diprediksi sebagai negatif dan
10 data diprediksi sebagai positif. Kelas netral lebih sering tertukar
dengan kelas negatif dibandingkan dengan kelas positif, yang juga
menjelaskan mengapa recall kelas netral menjadi yang paling rendah di
antara ketiga kelas, yaitu sebesar 0,6930.

Secara linguistik, kesalahan antara kelas netral dan negatif dapat
terjadi karena ulasan netral dalam konteks aplikasi perbankan digital
sering kali berbentuk pertanyaan, laporan kendala, atau pernyataan
singkat yang mengandung kata-kata seperti "login", "transfer", "kode",
"otp", atau "rekening", sebagaimana telah teridentifikasi pada analisis
word cloud pada subbab 4.7. Kata-kata tersebut juga sering muncul pada
ulasan negatif, sehingga model dapat mengasosiasikannya dengan sentimen
negatif meskipun konteks kalimat tidak selalu menunjukkan keluhan yang
kuat. Pola kesalahan semacam ini dapat dikatakan wajar dalam tugas
klasifikasi sentimen tiga kelas, mengingat kelas netral umumnya tidak
memiliki indikator sentimen yang eksplisit dan lebih bergantung pada
konteks kalimat dibandingkan kelas positif maupun negatif yang cenderung
mengandung ekspresi emosional yang lebih jelas.

Rekapitulasi jumlah prediksi benar dan salah secara keseluruhan dari
hasil confusion matrix tersebut disajikan pada Tabel 4.14.

**Tabel 4.14 Rekapitulasi Jumlah Prediksi Benar dan Salah**

  ----------------------------------- ----------------- -----------------
         **Kategori Prediksi**           **Jumlah**      **Persentase**

            Prediksi Benar                  1.321            93,16%

            Prediksi Salah                   97               6,84%

       **Total Data Uji (Test)**          **1.418**         **100%**
  ----------------------------------- ----------------- -----------------

Berdasarkan Tabel 4.14, dari total 1.418 data uji yang dievaluasi, model
berhasil memprediksi dengan benar sebanyak 1.321 data, sedangkan
sebanyak 97 data diprediksi secara tidak tepat. Jumlah ini konsisten
dengan nilai accuracy sebesar 0,9316 yang telah disajikan pada Tabel
4.11, sehingga dapat disimpulkan bahwa meskipun masih terdapat kesalahan
klasifikasi, proporsi prediksi benar jauh lebih besar dibandingkan
proporsi prediksi salah.

### **4.6.4 Interpretasi Kemampuan Model Secara Keseluruhan**

Berdasarkan hasil evaluasi yang telah dipaparkan pada subbab-subbab
sebelumnya, dapat disimpulkan bahwa model IndoBERT yang dikembangkan
dalam penelitian ini menunjukkan performa yang baik dalam melakukan
klasifikasi sentimen terhadap ulasan pengguna aplikasi JakOne Mobile.
Nilai accuracy sebesar 0,9316 dan macro F1-score sebesar 0,8774
menunjukkan bahwa model secara umum mampu mengenali ketiga kelas
sentimen, meskipun performanya belum sepenuhnya seimbang pada seluruh
kelas, dengan kecenderungan performa yang lebih dominan pada kelas
positif dan negatif dibandingkan kelas netral.

Selisih antara nilai macro F1-score sebesar 0,8774 dan weighted F1-score
sebesar 0,9309 yang teramati pada Tabel 4.11 mengindikasikan dampak dari
ketidakseimbangan kelas terhadap performa model secara keseluruhan, di
mana performa pada kelas mayoritas, yaitu positif dan negatif, cenderung
lebih dominan dalam memengaruhi metrik evaluasi dibandingkan kelas
minoritas, yaitu netral. Hal ini terlihat jelas dari nilai F1-score
kelas netral yang hanya sebesar 0,7524, jauh lebih rendah dibandingkan
kelas positif sebesar 0,9627 maupun kelas negatif sebesar 0,9170.

Secara keseluruhan, hasil evaluasi ini menunjukkan bahwa pendekatan
fine-tuning model IndoBERT terbukti efektif untuk diterapkan pada tugas
klasifikasi sentimen berbasis ulasan pengguna aplikasi perbankan digital
berbahasa Indonesia, mengingat model mampu memahami pola bahasa
Indonesia dan menghasilkan performa klasifikasi yang baik, khususnya
dalam mengenali sentimen positif dan negatif dengan cukup kuat. Namun,
performa model pada kelas dengan jumlah data lebih sedikit, yaitu kelas
netral, masih menjadi tantangan utama yang dapat menjadi bahan
pertimbangan untuk pengembangan penelitian selanjutnya, baik melalui
penambahan data netral, perbaikan kualitas label, analisis konteks
kalimat yang lebih mendalam, maupun penerapan strategi penanganan
ketidakseimbangan kelas (class imbalance handling).

Dengan demikian, model IndoBERT dalam penelitian ini dapat disimpulkan
memiliki performa yang baik secara keseluruhan, tetapi masih memiliki
ruang peningkatan, terutama pada klasifikasi ulasan bersentimen netral.

## **4.7 Visualisasi Word Cloud**

Untuk memperoleh gambaran yang lebih intuitif mengenai kata-kata yang
paling sering muncul pada setiap kategori sentimen, hasil pelabelan
sentimen yang telah diperoleh pada subbab 4.3 divisualisasikan dalam
bentuk word cloud untuk masing-masing kelas, yaitu sentimen positif,
negatif, dan netral. Visualisasi ini bertujuan untuk mengidentifikasi
topik atau aspek tertentu dari aplikasi JakOne Mobile yang paling banyak
dibicarakan oleh pengguna pada setiap kategori sentimen, sehingga dapat
diperoleh pemahaman awal mengenai aspek-aspek layanan yang dinilai
positif maupun yang menjadi sumber keluhan oleh pengguna, sebelum
dilakukan interpretasi yang lebih mendalam pada subbab pembahasan akhir.

Ukuran setiap kata pada word cloud merepresentasikan frekuensi
kemunculan kata tersebut pada data ulasan dalam kategori sentimen yang
bersangkutan, di mana kata dengan ukuran lebih besar menunjukkan
frekuensi kemunculan yang lebih tinggi dibandingkan kata dengan ukuran
lebih kecil. Rangkuman kata-kata dominan yang muncul pada hasil
visualisasi word cloud untuk ketiga kategori sentimen disajikan pada
Tabel 4.14.

**Tabel 4.14 Kata Dominan pada Word Cloud Tiap Kategori Sentimen**

  ------------------------------------------------
  **Sentimen      **Sentimen       **Sentimen
  Positif**       Negatif**        Netral**
  --------------- ---------------- ---------------
  mudah           transfer         otp

  bagus           error            update

  fitur           login            kode

  keren           otp              login

  membantu        gagal            rekening

  transaksi       saldo            

  cepat           lambat           
  ------------------------------------------------

### **4.7.1 Analisis Word Cloud Sentimen Positif**

![0](media/image2.png){width="6.268055555555556in"
height="3.6729166666666666in"}**Gambar 4.4 Word Cloud Sentimen Positif**

Berdasarkan hasil visualisasi word cloud pada Gambar 4.4, kata-kata yang
paling dominan muncul pada ulasan bersentimen positif antara lain

Berdasarkan hasil visualisasi word cloud pada Gambar 4.4, kata-kata yang
paling dominan muncul pada ulasan bersentimen positif antara lain
"mudah", "bagus", "fitur", "keren", "membantu", "transaksi", dan
"cepat". Dominasi kata "mudah" dan "cepat" mengindikasikan bahwa aspek
kemudahan dan kecepatan penggunaan aplikasi menjadi faktor utama yang
diapresiasi oleh pengguna JakOne Mobile. Selain itu, kemunculan kata
"fitur" dan "membantu" menunjukkan bahwa pengguna merasa fitur-fitur
yang disediakan aplikasi memberikan manfaat nyata dalam mendukung
aktivitas transaksi keuangan digital mereka.

Kemunculan kata "transaksi" dalam kelompok sentimen positif juga
memperkuat indikasi bahwa kepuasan pengguna banyak bersumber dari
pengalaman bertransaksi yang berjalan lancar, sedangkan kata "keren" dan
"bagus" mencerminkan kepuasan pengguna secara umum terhadap tampilan
maupun pengalaman penggunaan (user experience) aplikasi secara
keseluruhan.

### **4.7.2 Analisis Word Cloud Sentimen Negatif**

![0](media/image3.png){width="6.268055555555556in"
height="3.6729166666666666in"}

**Gambar 4.5 Word Cloud Sentimen Negatif**

Berbeda dengan kelompok sentimen positif, hasil visualisasi word cloud
pada Gambar 4.5 untuk ulasan bersentimen negatif didominasi oleh
kata-kata yang mengindikasikan kendala teknis, yaitu "transfer",
"error", "login", "otp", "gagal", "saldo", dan "lambat". Tingginya
frekuensi kemunculan kata "error" dan "gagal" mengindikasikan bahwa
keluhan pengguna sebagian besar berkaitan dengan kegagalan sistem dalam
memproses suatu permintaan, baik pada saat melakukan transfer dana
maupun proses login ke dalam aplikasi.

Kemunculan kata "transfer", "saldo", dan "lambat" secara bersamaan
menunjukkan bahwa permasalahan yang dialami pengguna banyak berkaitan
langsung dengan fungsi inti aplikasi sebagai layanan perbankan digital,
yaitu proses transaksi keuangan yang berjalan tidak sesuai harapan, baik
karena kegagalan transfer maupun respons sistem yang dirasa lambat.
Selain itu, kata "otp" dan "login" yang juga muncul dengan frekuensi
tinggi mengindikasikan adanya kendala pada proses autentikasi pengguna
sebelum dapat mengakses maupun menyelesaikan suatu transaksi.

### **4.7.3 Analisis Word Cloud Sentimen Netral**

![0](media/image4.png){width="6.268055555555556in"
height="3.6729166666666666in"}**Gambar 4.6 Word Cloud Sentimen Netral**

Pada kelompok sentimen netral, kata-kata yang paling dominan muncul pada
Gambar 4.6 adalah "otp", "update", "kode", "login", dan "rekening".
Berbeda dengan kelompok sentimen positif maupun negatif yang cenderung
memuat kata bermuatan emosional atau evaluatif secara eksplisit,
kata-kata yang mendominasi sentimen netral lebih bersifat deskriptif dan
prosedural, merujuk pada proses atau komponen teknis aplikasi tanpa
disertai penilaian baik atau buruk secara jelas.

Kemunculan kata "otp", "kode", dan "login" pada kelompok netral
mengindikasikan bahwa sebagian pengguna menuliskan ulasan yang sifatnya
menyampaikan informasi atau pertanyaan terkait proses autentikasi, tanpa
menyertakan ungkapan kepuasan maupun keluhan secara tegas. Sementara
itu, kata "update" mengindikasikan adanya ulasan yang membahas pembaruan
aplikasi secara informatif, dan kata "rekening" merujuk pada pembahasan
umum terkait akun atau data perbankan pengguna yang tidak disertai
sentimen yang kuat ke arah positif maupun negatif.

## **4.8 Implementasi Dashboard Streamlit**

Sebagai bentuk penerapan praktis dari model IndoBERT yang telah dilatih
dan dievaluasi pada subbab-subbab sebelumnya, dikembangkan sebuah
dashboard interaktif menggunakan framework Streamlit. Dashboard ini
dirancang agar hasil penelitian analisis sentimen tidak hanya berhenti
pada tahap evaluasi model, melainkan dapat diakses dan digunakan secara
langsung oleh pengguna untuk melakukan prediksi sentimen terhadap ulasan
baru, serta menampilkan visualisasi data hasil penelitian secara
interaktif.

Tujuan utama implementasi dashboard ini adalah untuk menyediakan
antarmuka yang sederhana dan mudah digunakan, sehingga pihak yang
berkepentingan, seperti pengembang aplikasi JakOne Mobile maupun pihak
manajemen terkait, dapat memanfaatkan model klasifikasi sentimen yang
telah dibangun tanpa perlu memahami proses teknis di baliknya. Selain
itu, dashboard ini juga berfungsi sebagai sarana untuk menampilkan hasil
eksplorasi data secara visual, sehingga gambaran umum mengenai
distribusi sentimen dan topik dominan pada ulasan pengguna dapat
dipahami dengan lebih cepat.

### **4.8.1 Struktur dan Fitur Utama Dashboard**

Dashboard yang dikembangkan terdiri atas beberapa halaman yang
masing-masing memiliki fungsi yang berbeda, mulai dari halaman prediksi
sentimen secara langsung (real-time) hingga halaman visualisasi hasil
penelitian secara keseluruhan. Daftar halaman beserta fungsi utamanya
disajikan pada Tabel 4.15.

**Tabel 4.15 Daftar Halaman pada Dashboard**

  -----------------------------------------------------------------------
  **Nama         **Fungsi Utama**
  Halaman**      
  -------------- --------------------------------------------------------
  Overview       Menampilkan ringkasan utama penelitian, meliputi total
                 data, accuracy dan macro F1 pada data test, best
                 validation F1, insight utama, alur penelitian, serta
                 distribusi label dan distribusi split dataset.

  Dataset        Menampilkan informasi dan karakteristik dataset final,
                 meliputi metrik ringkas, filter data, preview tabel,
                 serta visualisasi distribusi label, distribusi ulasan
                 per tahun, dan distribusi rating.

  Labeling       Menampilkan proses dan hasil pelabelan sentimen berbasis
                 lexicon, meliputi alur labeling, distribusi label hasil
                 labeling, contoh data berlabel, dan tabel validasi
                 manual.

  Training       Menampilkan ringkasan proses fine-tuning model IndoBERT,
  IndoBERT       meliputi best epoch, validation macro F1, training log,
                 serta kurva training loss, validation loss, validation
                 accuracy, dan validation macro F1.

  Evaluasi Model Menampilkan hasil evaluasi model pada data test,
                 meliputi accuracy, macro F1, weighted F1, classification
                 report, grafik metrik per kelas, serta confusion matrix
                 dan heatmap confusion matrix.

  Keyword Issue  Menampilkan analisis kata kunci dominan per kelas
  & Word Cloud   sentimen serta visualisasi word cloud untuk kategori
                 positif, negatif, dan netral.

  Demo Prediksi  Menyediakan fitur input ulasan baru untuk diprediksi
                 sentimennya secara langsung menggunakan model IndoBERT
                 hasil fine-tuning, lengkap dengan confidence score dan
                 probabilitas per kelas.
  -----------------------------------------------------------------------

Secara umum, dashboard ini menyediakan beberapa fitur utama yang saling
melengkapi satu sama lain dalam mendukung proses analisis sentimen
ulasan pengguna JakOne Mobile. Ringkasan fitur utama dashboard disajikan
pada Tabel 4.16.

**Tabel 4.16 Ringkasan Fitur Utama Dashboard**

  ---------------------------------------------------------------------------
  **No**   **Fitur**     **Deskripsi Singkat**
  -------- ------------- ----------------------------------------------------
  1        Prediksi      Pengguna memasukkan teks ulasan melalui kolom input,
           Sentimen      kemudian dashboard menampilkan hasil prediksi label
           Ulasan        sentimen (positif, negatif, atau netral) beserta
                         confidence score dan probabilitas tiap kelas
                         menggunakan model IndoBERT yang telah dilatih.

  2        Visualisasi   Menampilkan grafik donut interaktif yang menunjukkan
           Distribusi    proporsi jumlah ulasan pada setiap kategori sentimen
           Sentimen      dari data yang telah diproses

  3        Visualisasi   Menampilkan word cloud untuk masing-masing kategori
           Word Cloud    sentimen (positif, negatif, netral), sesuai dengan
                         hasil analisis pada subbab 4.7.

  4        Evaluasi      Menampilkan classification report, grafik metrik
           Performa      precision/recall/F1 per kelas, serta heatmap
           Model         confusion matrix untuk menggambarkan performa akhir
                         model pada data test.
  ---------------------------------------------------------------------------

### **4.8.2 Fungsi Setiap Halaman Dashboard**

Pada halaman **Overview**, dashboard menampilkan ringkasan utama
penelitian berupa kartu metrik (total data, accuracy test, macro F1
test, dan best validation F1), insight naratif mengenai performa model,
alur penelitian dari proses scraping hingga kesimpulan, serta grafik
donut distribusi label sentimen dan distribusi split dataset. Halaman
ini berfungsi sebagai halaman pembuka yang memberi gambaran umum hasil
penelitian. Tampilan halaman ini disajikan pada Gambar

![](media/image5.png){width="6.268055555555556in"
height="5.644444444444445in"}

4.7.\[ GAMBAR DASHBOARD --- screenshot halaman Overview, menunjukkan
kartu metrik, insight utama, dan grafik donut distribusi label serta
split dataset \]\
Gambar 4.7 Tampilan Halaman Overview pada Dashboard

Pada halaman **Dataset**, dashboard menampilkan karakteristik dataset
final yang digunakan dalam penelitian, sebagaimana telah dijelaskan pada
subbab 4.3 dan 4.4. Pengguna dapat memfilter data berdasarkan label,
tahun, dan jenis split, kemudian melihat hasilnya pada tabel preview.
Selain itu, tersedia visualisasi distribusi label, distribusi ulasan per
tahun, dan distribusi rating dalam bentuk tab interaktif. Tampilan
halaman ini disajikan pada Gambar 4.8.\
\[ GAMBAR DASHBOARD --- screenshot halaman Dataset, menunjukkan filter
data, preview

tabel, dan tab visualisasi distribusi \]\
Gambar 4.8 Tampilan Halaman Dataset pada Dashboard

![](media/image6.png){width="6.268055555555556in"
height="2.948611111111111in"}

![](media/image7.png){width="6.268055555555556in"
height="3.171527777777778in"}

![](media/image8.png){width="6.268055555555556in"
height="3.1590277777777778in"}

![](media/image9.png){width="6.268055555555556in"
height="3.1618055555555555in"}

![](media/image10.png){width="6.268055555555556in"
height="3.178472222222222in"}

Pada halaman **Labeling**, dashboard menampilkan proses dan hasil
pelabelan sentimen berbasis lexicon sebagaimana dijelaskan pada subbab
4.5, meliputi alur tahapan labeling, distribusi label hasil labeling,
contoh data yang telah berlabel, serta tabel hasil validasi manual jika
tersedia. Tampilan halaman ini disajikan pada Gambar 4.9.\
\[ GAMBAR DASHBOARD --- screenshot halaman Labeling, menunjukkan alur
labeling, distribusi label, dan contoh data berlabel \]\
Gambar 4.9 Tampilan Halaman Labeling pada Dashboard

![](media/image11.png){width="6.268055555555556in"
height="2.240972222222222in"}

![](media/image12.png){width="6.268055555555556in" height="1.94375in"}

![](media/image13.png){width="6.268055555555556in"
height="2.2083333333333335in"}

Pada halaman **Training IndoBERT**, dashboard menampilkan ringkasan
proses fine-tuning model, meliputi best epoch, validation macro F1
terbaik, train loss dan validation loss terakhir, tabel training log,
serta kurva perubahan training loss, validation loss, validation
accuracy, dan validation macro F1 sepanjang proses pelatihan. Tampilan
halaman ini disajikan pada Gambar 4.10.\
\[ GAMBAR DASHBOARD --- screenshot halaman Training IndoBERT,
menunjukkan ringkasan metrik training dan kurva training \]\
Gambar 4.10 Tampilan Halaman Training IndoBERT pada Dashboard

Pada halaman **Evaluasi Model**, dashboard menampilkan hasil evaluasi
performa model pada data test sebagaimana telah dijelaskan pada subbab
4.6, berupa accuracy, macro F1, weighted F1, classification report per
kelas, grafik metrik precision/recall/F1, confusion matrix, serta
heatmap confusion matrix untuk memudahkan identifikasi pola kesalahan
klasifikasi. Tampilan halaman ini disajikan pada Gambar 4.11.\
\[ GAMBAR DASHBOARD --- screenshot halaman Evaluasi Model, menunjukkan
classification report, grafik metrik per kelas, dan heatmap confusion
matrix \]\
Gambar 4.11 Tampilan Halaman Evaluasi Model pada Dashboard

Pada halaman **Keyword Issue & Word Cloud**, dashboard menampilkan
visualisasi kata kunci dominan dan word cloud untuk masing-masing
kategori sentimen, yang merupakan representasi visual dari hasil
analisis pada subbab 4.7. Pengguna dapat melihat top keyword secara
keseluruhan, top keyword pada label negatif, perbandingan keyword antar
label, serta word cloud untuk kategori positif, negatif, dan netral
melalui tampilan tab. Tampilan halaman ini disajikan pada Gambar 4.12.\
\[ GAMBAR DASHBOARD --- screenshot halaman Keyword Issue & Word Cloud,
menunjukkan grafik top keyword dan word cloud per kategori sentimen \]\
Gambar 4.12 Tampilan Halaman Keyword Issue & Word Cloud pada Dashboard

Pada halaman **Demo Prediksi**, pengguna dapat memasukkan teks ulasan
baru secara manual melalui kolom input yang tersedia. Setelah teks
dimasukkan dan tombol \"Prediksi Sentimen\" ditekan, dashboard akan
melakukan praproses teks, menjalankan model IndoBERT, dan menampilkan
hasil klasifikasi berupa label sentimen (positif, negatif, atau netral),
confidence score beserta status interpretasinya, grafik probabilitas
untuk setiap kelas, deteksi kata kunci terkait isu keamanan, sinyal
sentimen berbasis kata kunci, serta panel detail proses prediksi yang
menampilkan teks asli, teks setelah praproses, dan label mapping.
Halaman ini ditampilkan pada Gambar 4.13.\
\[ GAMBAR DASHBOARD --- screenshot halaman Demo Prediksi, menunjukkan
kolom input teks ulasan beserta hasil prediksi label, confidence score,
dan grafik probabilitas per kelas \]\
Gambar 4.13 Tampilan Halaman Demo Prediksi pada Dashboard

Ketujuh halaman tersebut dapat diakses secara fleksibel melalui menu
navigasi yang tersedia pada sidebar dashboard, sehingga pengguna dapat
dengan mudah berpindah antarhalaman sesuai kebutuhan, baik untuk
meninjau hasil eksplorasi data dan evaluasi model maupun untuk melakukan
prediksi sentimen terhadap ulasan baru.

### **4.8.3 Hasil Implementasi Dashboard**

Berdasarkan hasil implementasi, dashboard yang dibangun menggunakan
Streamlit berhasil dijalankan dan dapat diakses melalui browser secara
lokal pada alamat http://localhost:8501, dengan menjalankan perintah
streamlit run *dashboard/app.py* pada lingkungan virtual environment
project. Model IndoBERT yang telah dilatih sebelumnya pada subbab 4.5
berhasil diintegrasikan ke dalam dashboard dan dapat memberikan hasil
prediksi sentimen terhadap teks ulasan baru yang dimasukkan oleh
pengguna secara langsung (real-time), dengan indikator proses berupa
elemen *spinner* yang muncul selama tahap pemuatan model dan inferensi
berlangsung, sehingga pengguna mendapatkan umpan balik visual bahwa
sistem sedang memproses permintaan.

Secara fungsional, seluruh fitur yang telah dirancang, yaitu prediksi
sentimen, visualisasi distribusi sentimen, visualisasi word cloud, serta
visualisasi evaluasi model, dapat berjalan sebagaimana mestinya pada
dashboard. Hal ini menunjukkan bahwa hasil penelitian analisis sentimen
yang telah dilakukan tidak hanya bersifat teoritis, tetapi juga dapat
diimplementasikan ke dalam suatu sistem yang dapat dimanfaatkan secara
praktis oleh pihak yang membutuhkan.

Implementasi dashboard ini juga memberikan kontribusi tambahan terhadap
penelitian, yaitu memudahkan pihak pengembang JakOne Mobile maupun pihak
terkait untuk memantau dan menelusuri seluruh tahapan penelitian mulai
dari karakteristik dataset, proses pelabelan, performa pelatihan model,
hingga hasil evaluasi dalam satu antarmuka terpadu, serta melakukan
pengecekan sentimen terhadap ulasan baru secara cepat tanpa harus
melakukan analisis manual terhadap ribuan ulasan secara langsung. Dengan
demikian, dashboard ini melengkapi rangkaian penelitian sebagai bentuk
luaran (output) yang bersifat aplikatif dari keseluruhan proses analisis
sentimen yang telah dilakukan, mulai dari pengumpulan data,
preprocessing, pelabelan, pelatihan model, hingga evaluasi model pada
subbab-subbab sebelumnya.

## **4.9 Pembahasan Hasil Penelitian**

Subbab ini menyajikan pembahasan secara menyeluruh terhadap hasil
penelitian yang telah dipaparkan pada subbab-subbab sebelumnya, mulai
dari hasil pelatihan dan evaluasi model IndoBERT, distribusi sentimen
pengguna, hingga implikasi praktis dan keterbatasan yang ditemukan
selama proses penelitian. Pembahasan ini bertujuan untuk menghubungkan
temuan-temuan yang telah diperoleh secara terpisah pada subbab
sebelumnya menjadi satu kesatuan interpretasi yang lebih komprehensif.

### **4.9.1 Pembahasan Performa Model IndoBERT**

Berdasarkan hasil pelatihan dan evaluasi model yang telah dipaparkan
pada subbab 4.5 dan 4.6, model IndoBERT yang dikembangkan dalam
penelitian ini berhasil mencapai nilai accuracy sebesar 93,16% dan macro
F1-score sebesar 0,8774 pada data uji. Pencapaian ini menunjukkan bahwa
pendekatan fine-tuning terhadap model bahasa pre-trained berbasis
Transformer cukup efektif diterapkan pada tugas klasifikasi sentimen
ulasan pengguna aplikasi perbankan digital berbahasa Indonesia, meskipun
proses pelatihan hanya dilakukan dalam dua epoch.

Proses pelatihan yang stabil, sebagaimana tercermin dari pola penurunan
training loss dan validation loss yang searah pada subbab 4.5,
mengindikasikan bahwa model tidak mengalami overfitting meskipun jumlah
epoch yang digunakan relatif sedikit. Hal ini sejalan dengan
karakteristik umum model pre-trained berskala besar seperti IndoBERT,
yang telah memiliki representasi bahasa yang kuat sehingga proses
fine-tuning pada tugas klasifikasi spesifik dapat mencapai konvergensi
dengan cepat.

Namun, performa model tidak merata pada ketiga kelas sentimen.
Sebagaimana telah dijelaskan pada subbab 4.6, model menunjukkan performa
terbaik pada kelas positif (F1-score 0,9627), diikuti oleh kelas negatif
(F1-score 0,9170), sementara kelas netral memiliki performa yang jauh
lebih rendah (F1-score 0,7524). Kesenjangan performa ini menunjukkan
bahwa keberhasilan model dalam mencapai accuracy yang tinggi secara
keseluruhan sebagian besar didorong oleh kemampuannya mengenali kelas
mayoritas, yaitu positif dan negatif, sementara kemampuannya dalam
mengenali sentimen netral masih menjadi titik lemah utama.

Temuan ini memperkuat pemahaman bahwa metrik accuracy saja tidak cukup
untuk menggambarkan performa model secara utuh pada dataset dengan
distribusi kelas yang tidak seimbang. Selisih antara macro F1-score
(0,8774) dan weighted F1-score (0,9309) yang telah dibahas pada subbab
4.6.1 menjadi bukti kuantitatif bahwa performa model sangat dipengaruhi
oleh proporsi data pada setiap kelas, sehingga evaluasi model perlu
mempertimbangkan baik metrik yang sensitif terhadap ketidakseimbangan
kelas (macro) maupun metrik yang merepresentasikan performa praktis
secara keseluruhan (weighted maupun accuracy).

### **4.9.2 Pembahasan Distribusi Sentimen Pengguna JakOne Mobile**

Hasil pelabelan sentimen pada subbab 4.3 menunjukkan bahwa dari 14.172
ulasan yang dianalisis, sebanyak 59,42% ulasan bersentimen positif,
32,49% bersentimen negatif, dan hanya 8,09% bersentimen netral. Dominasi
sentimen positif ini mengindikasikan bahwa secara umum, pengguna JakOne
Mobile memiliki persepsi yang baik terhadap aplikasi, khususnya pada
aspek kemudahan penggunaan dan manfaat fitur, sebagaimana
teridentifikasi melalui analisis word cloud pada subbab 4.7, yang
menunjukkan dominasi kata seperti "mudah", "cepat", dan "membantu" pada
ulasan positif.

Meskipun demikian, proporsi sentimen negatif yang mencapai hampir
sepertiga dari keseluruhan data tetap merupakan temuan yang signifikan
untuk diperhatikan, mengingat JakOne Mobile merupakan aplikasi layanan
perbankan digital yang erat kaitannya dengan kepercayaan pengguna
terhadap keamanan dan keandalan transaksi keuangan. Berdasarkan analisis
word cloud pada subbab 4.7, sentimen negatif didominasi oleh kata-kata
yang berkaitan dengan kendala teknis, seperti "error", "gagal",
"lambat", serta kata-kata yang berkaitan dengan proses autentikasi dan
transaksi, seperti "login", "otp", "transfer", dan "saldo". Hal ini
mengindikasikan bahwa sumber utama ketidakpuasan pengguna tidak terletak
pada konsep atau fitur aplikasi secara umum, melainkan pada aspek
keandalan teknis dalam menjalankan fungsi-fungsi inti aplikasi sebagai
layanan perbankan digital.

Sementara itu, proporsi sentimen netral yang relatif kecil sejalan
dengan karakteristik umum ulasan aplikasi pada platform Google Play
Store, di mana pengguna cenderung menuliskan ulasan ketika memiliki
pengalaman yang cukup kuat, baik memuaskan maupun mengecewakan, dan
lebih jarang menuliskan ulasan untuk hal-hal yang bersifat netral atau
biasa saja. Kata-kata yang dominan pada kategori netral, seperti "otp",
"update", dan "login", sebagaimana telah dibahas pada subbab 4.7.3, juga
menunjukkan bahwa ulasan netral lebih banyak bersifat informatif atau
prosedural dibandingkan evaluatif.

Temuan tumpang tindihnya kata "otp" dan "login" pada kategori sentimen
negatif dan netral, sebagaimana telah diidentifikasi pada subbab 4.7.4,
juga relevan untuk dikaitkan dengan hasil confusion matrix pada subbab
4.6.3, di mana kelas netral paling sering tertukar dengan kelas negatif.
Konsistensi temuan ini, baik dari sisi analisis kata kunci maupun dari
sisi pola kesalahan klasifikasi model, memperkuat indikasi bahwa proses
autentikasi melalui OTP dan login merupakan salah satu titik krusial
(touchpoint) yang banyak dibicarakan pengguna dengan nada yang beragam,
mulai dari keluhan tegas hingga pernyataan yang sifatnya lebih netral
atau prosedural.

### **4.9.3 Implikasi Hasil bagi Pengembangan JakOne Mobile**

Hasil penelitian ini memberikan sejumlah implikasi praktis yang dapat
menjadi bahan pertimbangan bagi pihak pengembang JakOne Mobile dalam
upaya peningkatan kualitas layanan dan kepuasan pengguna.

Pertama, hasil analisis kata kunci pada sentimen negatif menunjukkan
bahwa keluhan pengguna terutama berkaitan dengan aspek operasional
transaksi dan akses layanan digital. Kata "transfer" menjadi kata yang
paling dominan dengan 924 kemunculan atau 20,07% dari seluruh kata pada
ulasan negatif, diikuti oleh "error" (598 kemunculan, 12,99%), "login"
(451 kemunculan, 9,79%), "gagal" (413 kemunculan, 8,97%), "transaksi"
(361 kemunculan, 7,84%), "saldo" (352 kemunculan, 7,64%), "otp" (351
kemunculan, 7,62%), "rekening" (292 kemunculan, 6,34%), "verifikasi"
(233 kemunculan, 5,06%), dan "kode" (229 kemunculan, 4,97%). Temuan ini
menunjukkan bahwa keluhan pengguna tidak hanya berkaitan dengan persepsi
umum terhadap aplikasi, tetapi lebih spesifik mengarah pada proses
transfer, kegagalan transaksi, kendala login, OTP, verifikasi, saldo,
dan rekening. Hasil ini diperkuat oleh confusion matrix pada subbab
4.6.3, yang menunjukkan bahwa model mampu mengenali sentimen negatif
dengan cukup kuat, yaitu 442 dari 461 data negatif berhasil
diklasifikasikan dengan benar (recall 0,9588), sehingga kata-kata kunci
tersebut dapat dipercaya merepresentasikan keluhan aktual pengguna.
Dengan demikian, implikasi praktis bagi pengembang JakOne Mobile adalah
perlunya memprioritaskan stabilitas proses transfer dan transaksi,
perbaikan mekanisme login dan OTP, transparansi status saldo atau
transaksi yang gagal, serta penyederhanaan proses verifikasi akun. Kata
kunci seperti "error", "gagal", "otp", "saldo", dan "verifikasi" juga
dapat dijadikan indikator awal dalam sistem pemantauan keluhan untuk
menentukan prioritas perbaikan teknis aplikasi secara berkelanjutan.

Kedua, dashboard Streamlit yang dibangun pada subbab 4.8 memiliki
implikasi praktis sebagai alat bantu monitoring sentimen pengguna secara
berkelanjutan. Dashboard ini menyediakan tujuh halaman, yaitu Overview,
Dataset, Labeling, Training IndoBERT, Evaluasi Model, Keyword Issue &
Word Cloud, serta Demo Prediksi, dengan fitur yang mencakup ringkasan
metrik utama (total data, accuracy test, macro F1 test, dan best
validation F1), visualisasi distribusi sentimen dan pembagian dataset,
filter data berdasarkan label, tahun, dan split set, kurva training dan
validation loss, classification report, confusion matrix dalam bentuk
tabel dan heatmap, analisis keyword issue dan word cloud per kategori
sentimen, serta fitur prediksi sentimen secara real-time. Pada halaman
Demo Prediksi, pengguna dapat memasukkan teks ulasan baru, kemudian
dashboard menampilkan label prediksi, confidence score, status keyakinan
model, probabilitas setiap kelas, keyword keamanan yang terdeteksi,
serta detail proses preprocessing yang dilalui. Dengan kelengkapan fitur
tersebut, dashboard ini dapat dimanfaatkan oleh tim pengembang maupun
tim customer support JakOne Mobile untuk memantau kecenderungan sentimen
pengguna secara berkala, mengidentifikasi topik keluhan yang dominan,
mengevaluasi perubahan persepsi pengguna dari waktu ke waktu, serta
melakukan pengecekan cepat terhadap ulasan baru sebelum ditindaklanjuti
secara operasional.

Ketiga, hasil evaluasi model juga mengindikasikan perlunya perhatian
khusus terhadap kelas netral, mengingat kelas ini memiliki performa
paling rendah dibandingkan kelas positif dan negatif. Meskipun model
secara keseluruhan memperoleh accuracy sebesar 93,16% dan macro F1-score
sebesar 0,8774, F1-score pada kelas netral hanya sebesar 0,7524 dengan
recall 0,6930, jauh lebih rendah dibandingkan kelas positif (F1-score
0,9627) maupun kelas negatif (F1-score 0,9170). Confusion matrix pada
subbab 4.6.3 menunjukkan bahwa dari 114 data aktual netral, hanya 79
data yang berhasil diprediksi dengan benar, sedangkan 25 data diprediksi
sebagai negatif dan 10 data diprediksi sebagai positif. Pola ini
mengindikasikan bahwa ulasan netral relatif lebih sulit dikenali,
kemungkinan karena bentuknya sering berupa pertanyaan, laporan singkat,
atau pernyataan informatif yang tidak selalu mengandung ekspresi
sentimen yang eksplisit. Kondisi ini juga sejalan dengan
ketidakseimbangan distribusi data, di mana sentimen netral hanya
mencakup 8,09% dari total data dibandingkan sentimen positif (59,42%)
dan negatif (32,49%). Oleh karena itu, implikasi bagi pengembangan
sistem ke depannya adalah perlunya evaluasi berkala terhadap data
netral, penambahan atau peninjauan ulang sampel ulasan netral, serta
strategi komunikasi yang lebih responsif terhadap ulasan yang bersifat
ambigu, misalnya pertanyaan terkait OTP, login, kode, transfer, atau
rekening yang belum tentu bernada negatif namun tetap menunjukkan
kebutuhan bantuan dari pengguna.

Dengan memanfaatkan hasil analisis sentimen ini secara berkelanjutan,
pihak pengembang JakOne Mobile dapat memperoleh gambaran yang lebih
objektif dan berbasis data mengenai aspek-aspek layanan yang perlu
diperbaiki maupun dipertahankan, sehingga pengambilan keputusan terkait
pengembangan aplikasi dapat lebih selaras dengan kebutuhan dan harapan
pengguna.

### **4.9.4 Keterbatasan Penelitian**

Meskipun penelitian ini telah berhasil mencapai tujuan yang ditetapkan,
terdapat beberapa keterbatasan yang perlu diakui dan menjadi bahan
pertimbangan dalam menginterpretasikan hasil penelitian secara
keseluruhan, sebagaimana dirangkum pada Tabel 4.18.

**Tabel 4.18 Ringkasan Keterbatasan Penelitian**

  --------------------- ------------------------ ------------------------
        **Aspek**           **Keterbatasan**        **Tahap Terkait**

   **Pelabelan Data**        Label sentimen             Subbab 4.3
                         dihasilkan dari metode  
                        berbasis leksikon (InSet 
                        Lexicon), bukan anotasi  
                           manual oleh ahli,     
                          sehingga berpotensi    
                          mengandung kesalahan   
                           label pada kalimat    
                        dengan konteks kompleks, 
                         sarkasme, atau negasi   
                              bertingkat.        

   **Ketidakseimbangan      Distribusi data             Subbab 4.4
         Kelas**            antarkelas tidak     
                         seimbang, dengan kelas  
                         netral hanya berjumlah  
                         8,09% dari total data,  
                        sehingga model memiliki  
                        contoh belajar yang jauh 
                          lebih sedikit untuk    
                            kelas tersebut.      

  **Performa Model pada    Model menunjukkan            Subbab 4.6
    Kelas Minoritas**   performa yang jauh lebih 
                        rendah pada kelas netral 
                           (F1-score 0,7524)     
                           dibandingkan kelas    
                          positif dan negatif,   
                        yang membatasi keandalan 
                              model dalam        
                           mengklasifikasikan    
                        ulasan bersifat ambigu.  

  **Sumber dan Cakupan  Data hanya diambil dari         Subbab 4.1
         Data**            satu sumber, yaitu    
                        ulasan pada Google Play  
                         Store, sehingga belum   
                        mencakup opini pengguna  
                        dari kanal lain seperti  
                        App Store, media sosial, 
                         atau survei langsung.   

        **Periode        Data dikumpulkan pada          Subbab 4.1
      Pengamatan**      rentang waktu tertentu,  
                             sehingga hasil      
                               penelitian        
                           merepresentasikan     
                         sentimen pengguna pada  
                          periode tersebut dan   
                        belum tentu mencerminkan 
                           persepsi pengguna     
                        setelah adanya pembaruan 
                            aplikasi di masa     
                               mendatang.        

      **Konfigurasi     Proses fine-tuning model        Subbab 4.5
    Pelatihan Model**    hanya dilakukan dalam   
                         dua epoch dengan satu   
                              konfigurasi        
                        hyperparameter, sehingga 
                            belum dilakukan      
                          eksplorasi terhadap    
                        kemungkinan konfigurasi  
                            lain yang dapat      
                         menghasilkan performa   
                             lebih optimal.      
  --------------------- ------------------------ ------------------------

Keterbatasan pertama yang perlu diperhatikan adalah penggunaan metode
berbasis leksikon (InSet Lexicon) dalam proses pelabelan data pada
subbab 4.3. Berbeda dengan anotasi manual oleh ahli bahasa, metode
berbasis leksikon bekerja dengan mencocokkan kata dalam teks terhadap
kamus sentimen yang telah ditentukan sebelumnya, sehingga berpotensi
menghasilkan label yang kurang tepat pada kalimat dengan konteks yang
kompleks, mengandung sarkasme, atau memiliki struktur negasi bertingkat.
Mengingat label hasil pelabelan ini menjadi dasar (ground truth) bagi
proses pelatihan dan evaluasi model pada subbab 4.5 dan 4.6, potensi
kesalahan label pada tahap ini turut memengaruhi keandalan hasil
penelitian secara keseluruhan.

Keterbatasan kedua berkaitan dengan ketidakseimbangan distribusi kelas
sentimen yang telah diidentifikasi pada subbab 4.4, di mana kelas netral
hanya mencakup 8,09% dari total data. Ketidakseimbangan ini secara
langsung berdampak pada performa model dalam mengenali kelas netral,
sebagaimana ditunjukkan oleh F1-score kelas netral yang jauh lebih
rendah dibandingkan dua kelas lainnya pada subbab 4.6.2. Penelitian ini
belum menerapkan strategi penanganan ketidakseimbangan kelas, seperti
teknik oversampling, undersampling, maupun penerapan pembobotan kelas
(class weighting) pada fungsi loss, yang berpotensi dapat meningkatkan
performa model pada kelas minoritas apabila diterapkan pada penelitian
selanjutnya.

Keterbatasan ketiga terkait dengan sumber dan cakupan data penelitian.
Data ulasan yang digunakan hanya diperoleh dari satu sumber, yaitu
platform Google Play Store, sehingga belum mencakup opini pengguna yang
disampaikan melalui kanal lain, seperti App Store untuk pengguna iOS,
media sosial, maupun saluran pengaduan resmi JakOne Mobile. Selain itu,
data yang dikumpulkan merepresentasikan sentimen pengguna pada rentang
waktu tertentu sebagaimana dijelaskan pada subbab 4.1, sehingga hasil
penelitian ini perlu dipahami sebagai potret persepsi pengguna pada
periode tersebut dan tidak serta-merta mencerminkan persepsi pengguna
setelah adanya pembaruan atau perbaikan aplikasi di masa mendatang.

Keterbatasan keempat berkaitan dengan konfigurasi pelatihan model yang
digunakan pada subbab 4.5. Proses fine-tuning model IndoBERT pada
penelitian ini hanya dilakukan dalam dua epoch dengan satu kombinasi
hyperparameter, tanpa dilakukan eksplorasi atau pengujian terhadap
kombinasi konfigurasi lain, seperti variasi learning rate, batch size,
maupun jumlah epoch yang lebih banyak. Dengan demikian, performa model
yang diperoleh pada penelitian ini belum tentu merupakan performa
optimal yang dapat dicapai oleh arsitektur IndoBERT pada tugas
klasifikasi sentimen ini, dan masih terdapat kemungkinan peningkatan
performa apabila dilakukan eksplorasi hyperparameter yang lebih
ekstensif pada penelitian selanjutnya.

Pengakuan terhadap keterbatasan-keterbatasan tersebut tidak mengurangi
kontribusi dan validitas temuan penelitian ini, melainkan memberikan
konteks yang lebih jujur dan objektif mengenai batasan interpretasi
hasil penelitian, serta membuka peluang bagi penelitian selanjutnya
untuk menyempurnakan aspek-aspek yang belum tercakup pada penelitian
ini.
