# BAB 3

# METODOLOGI PENELITIAN

## 3.1 Tahapan Penelitian

Penelitian ini dimulai dengan pengumpulan data menggunakan teknik *web
scraping* dari Google Play Store untuk memperoleh data ulasan pengguna
yang relevan. Data yang terkumpul kemudian melewati serangkaian tahap
pemrosesan sebelum digunakan dalam pelabelan dan pemodelan keseluruhan
tahap ini dikenal sebagai *pre-processing*. Tahap *pre-processing*
mencakup: pengubahan teks menjadi huruf kecil (*case folding*),
pembersihan elemen tidak relevan seperti URL dan *mention*
(*cleansing*), standarisasi kata tidak baku (normalisasi), penghapusan
kata umum yang tidak berkontribusi pada makna sentimen (*stopword
removal*), serta eliminasi data kosong dan data duplikat. Seluruh alur
penelitian disajikan pada gambar berikut.

![](media/image1.png){width="5.111805555555556in"
height="5.888888888888889in"}

Gambar 3. 1 Diagram Alur

Setelah data bersih, penelitian berlanjut ke tahap pemberian label (data
labelling). Tahap ini mengklasifikasikan setiap ulasan ke dalam tiga
kategori sentimen: positif, negatif, dan netral. Pelabelan dilakukan
secara otomatis menggunakan pendekatan berbasis leksikon dengan InSet
Lexicon, di mana skor sentimen tiap ulasan dihitung dan dijadikan dasar
penentuan kategori. Label yang dihasilkan pada tahap ini berfungsi
sebagai target klasifikasi pada model IndoBERT.

Sebelum pemodelan, label hasil otomatis divalidasi terlebih dahulu untuk
memastikan kualitasnya cukup andal dan representatif terhadap sentimen
yang sesungguhnya. Visualisasi distribusi label juga dilakukan agar
peneliti dapat memahami komposisi data secara menyeluruh. Setelah
validasi, data dipisah (*data splitting*) menjadi tiga bagiandata latih
(*training*), data validasi (*validation*), dan data uji (*testing*)agar
evaluasi model berlangsung secara objektif.

Tahap berikutnya adalah implementasi model IndoBERT, yaitu model
berbasis arsitektur BERT yang disesuaikan untuk bahasa Indonesia. Data
ulasan yang telah diproses dan diberi label ditokenisasi menggunakan
tokenizer IndoBERT, kemudian model menjalani *fine-tuning* untuk
mempelajari pola sentimen dalam data. Kemampuan model memahami konteks
teks bahasa Indonesia menjadi pertimbangan utama pemilihan IndoBERT
sebagai model klasifikasi.

Setelah pelatihan selesai, evaluasi model dilakukan untuk mengukur
seberapa baik model mengklasifikasikan sentimen secara tepat dan
konsisten. Evaluasi menggunakan beberapa metrik sekaligus akurasi,
presisi, recall, F1-score, dan *confusion matrix* sehingga performa
model dapat dinilai dari berbagai sudut pandang.

Sebagai tahap akhir, penelitian mengembangkan *dashboard* interaktif
berbasis Streamlit yang menyajikan seluruh hasil penelitian: ringkasan
proyek, distribusi dataset, hasil pelabelan, evaluasi model, hingga
demonstrasi prediksi sentimen secara *class imbalance*, dalam satu
antarmuka yang mudah dipahami.

## 3.2 Teknik Pengumpulan Data

Pengumpulan data dilakukan dengan teknik web scraping pada platform
Google Play Store menggunakan library Python *google_play_scraper*.
Aplikasi yang menjadi objek penelitian adalah JakOne Mobile,
diidentifikasi melalui ID resmi *com.dev.jakone.mbanking*. Penggunaan ID
aplikasi yang spesifik memastikan seluruh data ulasan berasal dari
aplikasi yang relevan dengan objek penelitian.

Pengambilan data dikonfigurasi dengan parameter lang=\'id\' dan
country=\'id\' agar data yang diperoleh sesuai dengan konteks pengguna
Indonesia. Informasi yang dikumpulkan mencakup teks ulasan, rating,
tanggal ulasan, versi aplikasi apabila tersedia, serta data pendukung
lain yang terkait dengan ulasan di Google Play Store.

Setelah data terkumpul, dilakukan penyaringan awal untuk memastikan
ulasan yang digunakan sesuai kebutuhan penelitian. Ulasan tidak relevan
atau duplikat dieliminasi pada tahap ini. Dari keseluruhan proses ini
diperoleh data mentah sebanyak 14.272 ulasan pengguna aplikasi JakOne
Mobile.

Seluruh data hasil scraping disimpan dalam format .csv untuk memudahkan
pengolahan pada tahap selanjutnya, yaitu *pre-processing*, pelabelan
sentimen, pembagian dataset, pemodelan dengan IndoBERT, dan evaluasi
model. Kualitas data awal berpengaruh langsung terhadap akurasi hasil
analisis sentimen pada keseluruhan penelitian.

![](media/image2.png){width="1.6190485564304462in"
height="3.355698818897638in"}

Gambar 3. 2 Tahapan Pengumpulan Data

## 3.3 Preprocessing Data

Data mentah hasil pengumpulan umumnya belum siap digunakan secara
langsung karena mengandung berbagai elemen pengganggu simbol, karakter
tidak relevan, kata tidak baku, dan data duplikat yang dapat menurunkan
kualitas analisis. Oleh karena itu, data ulasan perlu melalui proses
pembersihan dan standarisasi yang dikenal sebagai *preprocessing*
sebelum masuk ke tahap pelabelan dan pemodelan. Dalam klasifikasi teks,
kualitas data berpengaruh langsung terhadap performa model; tanpa
*preprocessing* yang memadai, noise pada data dapat menurunkan kualitas
model. Tahapan *preprocessing* yang diterapkan dalam penelitian ini
disajikan pada gambar berikut.

![](media/image3.png){width="1.251706036745407in"
height="4.190476815398076in"}

Gambar 3. 3 Tahapan Preprocessing Data

Dari tahapan *preprocessing* yang mencakup *case* *folding*,
*cleansing*, normalisasi kata, *stopword removal*, penghapusan data
kosong, dan penghapusan duplikasi diperoleh 14.172 ulasan bersih dari
14.272 ulasan mentah awal, dengan 100 ulasan yang gugur karena tidak
memenuhi syarat kualitas data.

### 3.3.1 Case Folding

*Case folding* adalah proses mengubah seluruh karakter teks menjadi
huruf kecil. Langkah ini diperlukan karena satu kata yang sama dapat
muncul dalam berbagai variasi penulisan misalnya \"Aplikasi\",
\"APLIKASI\", dan \"aplikasi\" yang tanpa diseragamkan akan diperlakukan
sebagai token berbeda oleh sistem pemrosesan teks. *Case folding*
menjamin konsistensi representasi teks sehingga data lebih siap diproses
pada tahap berikutnya.

### 3.3.2 Cleansing

Tahap *cleansing* menghapus elemen-elemen yang tidak relevan dari teks
ulasan, meliputi URL, mention, emoji, simbol, tanda baca berlebihan,
karakter khusus, dan spasi yang tidak perlu. Dalam ulasan Google Play
Store, pengguna kerap menyertakan karakter-karakter tersebut yang tidak
memiliki nilai analitis dalam penentuan sentimen. Dengan membersihkan
elemen ini, data berfokus pada konten teks yang sesungguhnya sehingga
proses analisis berikutnya berjalan lebih efektif.

### 3.3.3 Normalisasi Kata

Pengguna aplikasi cenderung menulis dalam bahasa sehari-hari yang kaya
singkatan dan variasi informal, seperti \"gk\", \"ga\", \"yg\", \"apk\",
atau \"tdk\". Tanpa normalisasi, kata-kata yang bermakna sama
diperlakukan sebagai entitas berbeda dalam proses pelabelan dan
pemodelan. Normalisasi kata mencocokkan setiap kata tidak baku terhadap
kamus normalisasi dan menggantinya dengan bentuk baku, sehingga
konsistensi representasi makna teks terjaga sebelum analisis lebih
lanjut dilakukan.

### 3.3.4 Stopword Removal

Kata-kata seperti \"yang\", \"dan\", \"di\", \"ke\", atau \"dari\" hadir
di hampir setiap kalimat, namun tidak berkontribusi pada penentuan
polaritas sentimen. Proses *stopword removal* membantu model berfokus
pada kata-kata yang mengandung muatan sentimen. Penerapan tahap ini
memerlukan kehati-hatian: kata fungsi tertentu, terutama negasi seperti
\"tidak\", \"bukan\", \"jangan\", \"gak\", dan \"nggak\", memiliki peran
penting dalam membentuk makna sentimen. Menghapus kata negasi dapat
membalikkan polaritas ulasan. Karena itu, dalam penelitian ini kata-kata
negasi dikecualikan dari daftar stopword agar konteks sentimen tetap
terjaga.

### 3.3.5 Penghapusan Data Kosong

Setelah serangkaian tahap pembersihan, sejumlah ulasan berpotensi
menjadi kosong kondisi yang terjadi ketika ulasan hanya terdiri dari
emoji, simbol, angka, atau karakter yang telah dihapus pada tahap
sebelumnya. Data seperti ini tidak lagi mengandung informasi teks yang
dapat dianalisis; keberadaannya dalam dataset justru mengganggu proses
pelabelan dan pemodelan. Penghapusan data kosong secara eksplisit
menghasilkan dataset yang lebih bersih dan siap untuk dianalisis.

### 3.3.6 Penghapusan Duplikasi

Duplikasi data dapat muncul karena pengguna mengirimkan ulasan identik
lebih dari satu kali atau karena data ganda pada saat pengumpulan. Data
duplikat menimbulkan bias dalam pelatihan model karena model terpapar
teks yang sama berulang seolah-olah merupakan sampel independen. Untuk
menjaga representativitas dataset, seluruh ulasan dengan konten identik
atau sangat serupa dieliminasi pada tahap ini. Langkah ini merupakan
penjaga kualitas data terakhir sebelum dataset masuk ke tahap pelabelan
sentimen dan pemodelan IndoBERT.

Setelah seluruh tahapan preprocessing diterapkan secara berurutan,
diperoleh 14.172 ulasan bersih dari total 14.272 ulasan mentah awal,
dengan 100 ulasan yang tidak memenuhi syarat kualitas data.

## 3.4 Pelabelan Sentimen

Agar data ulasan dapat digunakan sebagai input dalam pelatihan model
klasifikasi, setiap ulasan perlu diberi label yang mencerminkan kategori
sentimennya. Dalam penelitian ini, pelabelan dilakukan secara otomatis
menggunakan pendekatan berbasis leksikon (*lexicon-based*). Pendekatan
ini bekerja dengan mencocokkan setiap kata atau frasa dalam teks
terhadap kamus sentimen yang memuat daftar kata beserta nilai
polaritasnya. Skor tiap kata yang ditemukan kemudian diakumulasikan
menjadi skor sentimen keseluruhan ulasan, yang selanjutnya menentukan
label kategorinya.

Kamus sentimen yang digunakan adalah InSet Lexicon, sebuah kamus
berbahasa Indonesia yang dikembangkan untuk mengidentifikasi opini dalam
teks dan mengklasifikasikannya sebagai positif atau negatif. InSet
Lexicon disusun dari kumpulan kata *tweet* berbahasa Indonesia, di mana
setiap kata diberi bobot secara manual, kemudian diperkaya melalui
stemming dan penambahan sinonim.

Dalam konteks penelitian ini analisis sentimen pada aplikasi perbankan
digital kamus InSet Lexicon yang digunakan telah diperbarui menjadi
InSet Lexicon. Pembaruan dilakukan untuk menyesuaikan kosakata kamus
dengan karakteristik bahasa pengguna aplikasi JakOne Mobile, sehingga
hasil pelabelan lebih akurat dan relevan terhadap domain yang diteliti.

![](media/image4.png){width="2.4166666666666665in"
height="5.113463473315836in"}

Gambar 3. 4 Tahapan Pelabelan Data

Penentuan label sentimen didasarkan pada total skor akumulasi setiap
ulasan dengan aturan sebagai berikut.

> • Jika total skor \> 0, ulasan dikategorikan sebagai Positif.
>
> • Jika total skor \< 0, ulasan dikategorikan sebagai Negatif.
>
> • Jika total skor = 0, ulasan dikategorikan sebagai Netral.

Ulasan dengan skor positif mencerminkan dominasi kata bermuatan positif,
sedangkan skor negatif menandakan sebaliknya. Skor tepat nol terjadi
ketika tidak ada kata berbobot yang ditemukan atau bobot positif dan
negatif saling meniadakan; ulasan tersebut diklasifikasikan sebagai
netral. Label yang digunakan sebagai dasar pelatihan model adalah diberi
nama keterangan nya V3, yaitu label yang telah mengalami pembaruan dan
perbaikan dari versi-versi sebelumnya.

## 3.5 Validasi dan Perbaikan Label

Label yang dihasilkan secara otomatis oleh pendekatan berbasis leksikon
tidak selalu sempurna, karena proses otomatis tidak mempertimbangkan
konteks secara mendalam seperti yang dilakukan manusia. Untuk mengukur
sejauh mana label otomatis sesuai dengan penilaian sentimen yang
sesungguhnya, validasi dilakukan menggunakan 100 sampel data yang
peneliti labeli secara manual. Dalam linguistik komputasional,
pengukuran kesesuaian anotasi merupakan langkah standar untuk menilai
reliabilitas data berlabel sebelum digunakan dalam analisis lebih
lanjut.

Hasil validasi menunjukkan bahwa label V1 mencapai akurasi 80%,
sedangkan label V3 menghasilkan akurasi 85%. Peningkatan ini membuktikan
bahwa penyempurnaan kamus leksikon dan perbaikan aturan pelabelan antara
V1 dan V3 berdampak nyata terhadap kualitas label. Berdasarkan
perbandingan ini, label V3 dipilih sebagai label akhir dalam tahap
pemodelan.

Selain validasi berbasis sampel, dilakukan audit label secara menyeluruh
untuk mengidentifikasi potensi kesalahan sistematis dalam proses
pelabelan otomatis. Audit ini difokuskan pada dua faktor utama. Pertama,
konflik skor, yaitu kondisi ketika sebuah ulasan mengandung kata
berbobot positif dan negatif secara bersamaan sehingga skor akhirnya
kurang merepresentasikan sentimen keseluruhan ulasan. Kedua, pola
negasi, yaitu kondisi di mana kata-kata seperti \"tidak\", \"bukan\",
\"gak\", atau \"nggak\" membalikkan makna sentimen dari kata yang
mengikutinya misalnya mengubah frasa yang positif menjadi bermuatan
negatif. Penanganan kedua faktor ini penting agar label yang dihasilkan
benar-benar mencerminkan sentimen yang dimaksud penulis ulasan.

Melalui kombinasi validasi manual dan audit label, proses pelabelan
dalam penelitian ini tidak hanya mengandalkan keluaran otomatis dari
kamus sentimen, tetapi juga mempertimbangkan kualitas dan kesesuaian
label terhadap konteks ulasan pengguna JakOne Mobile. Hal ini memastikan
bahwa dataset yang digunakan dalam pelatihan model IndoBERT memiliki
label yang akurat dan selaras dengan tujuan penelitian.

## 3.6 Pembagian Dataset

Dataset yang telah diberi label selanjutnya dibagi menjadi tiga subset
menggunakan metode stratified split. Metode ini dipilih karena
kemampuannya mempertahankan proporsi distribusi kelas label pada setiap
subset karakteristik yang krusial mengingat adanya ketidakseimbangan
kelas dalam dataset penelitian ini. Dalam *Scikit-learn*, hal ini
diimplementasikan melalui parameter stratify pada fungsi
*train_test_split*, sehingga komposisi kelas pada data latih, data
validasi, dan data uji tetap proporsional terhadap distribusi
keseluruhan dataset.

Proporsi pembagian yang diterapkan adalah 80% untuk data latih, 10%
untuk data validasi, dan 10% untuk data uji. Rincian jumlah data pada
masing-masing subset disajikan pada tabel berikut.

Tabel 3. 5 Pembagian Dataset

  -----------------------------------------------------------------------
              **Subset**                 Jumlah Data        Persentase
  ----------------------------------- ------------------ ----------------
         *Train* (Data Latih)               11.337             80%

     *Validation* (Data Validasi)           1.417              10%

           *Test* (Data Uji)                1.418              10%

               **Total**                    14.172             100%
  -----------------------------------------------------------------------

Perlu diperhatikan bahwa terdapat ketidakseimbangan kelas (*class
imbalance*) yang cukup signifikan dalam dataset ini, terutama pada kelas
netral yang jumlahnya jauh lebih sedikit dibandingkan kelas positif dan
negatif, sebagaimana ditampilkan pada Tabel 3.6. Kondisi ini
berimplikasi pada pemilihan metrik evaluasi: akurasi saja tidak cukup
representatif karena dapat terdistorsi oleh dominasi kelas mayoritas.
Penelitian ini menggunakan *macro F1-score* yang menghitung rata-rata
*F1-score* setiap kelas secara setara tanpa mempertimbangkan ukuran
kelas, sehingga performa model pada kelas minoritas mendapat perhatian
yang proporsional.

Tabel 3. 6 Distribusi Label Sentimen

  -----------------------------------------------------------------------
      **Label Sentimen**         Jumlah Data          Persentase (%)
  -------------------------- -------------------- -----------------------
           Positif                  8.421                  59,4

           Negatif                  4.605                  32,5

            Netral                  1.146                   8,1

          **Total**                 14.172                  100
  -----------------------------------------------------------------------

## 3.7 Pemodelan Menggunakan IndoBERT

Model yang diimplementasikan dalam penelitian ini adalah IndoBERT versi
*indobenchmark/indobert-base-p1*, salah satu model bahasa Indonesia yang
tersedia dalam ekosistem IndoNLU. IndoBERT dikembangkan berdasarkan
arsitektur BERT (*Bidirectional Encoder Representations from
Transformers*), sebuah model representasi bahasa yang memahami konteks
secara dua arah mempertimbangkan kata-kata di sebelah kiri dan kanan
suatu token secara bersamaan di seluruh lapisan model. Kemampuan
pemahaman konteks yang bersifat bidireksional ini memungkinkan BERT
menginterpretasikan makna kata dengan lebih akurat sesuai kalimatnya.

Pemilihan IndoBERT dalam penelitian ini didasarkan pada tiga
pertimbangan. Pertama, IndoBERT telah dilatih menggunakan data berbahasa
Indonesia sehingga lebih mampu memahami pola linguistik khas dalam
ulasan pengguna JakOne Mobile. Kedua, karakteristik bidireksional
arsitektur BERT memungkinkan model memahami makna kata berdasarkan
konteks sebelum dan sesudahnya secara simultan, yang relevan dalam
analisis sentimen. Ketiga, mekanisme *fine-tuning* memungkinkan model
disesuaikan secara spesifik dengan tugas klasifikasi sentimen tiga kelas
dalam penelitian ini.

Proses *fine-tuning* dilakukan dengan menambahkan lapisan klasifikasi di
atas model dasar IndoBERT, kemudian melatihnya menggunakan data latih
yang telah diberi label. Konfigurasi hyperparameter yang diterapkan
selama proses pelatihan disajikan pada tabel berikut.

Tabel 3. 7 Konfigurasi Hyperparameter Fine-Tuning IndoBERT

  -----------------------------------------------------------------------
                   **Hyperparameter**                      **Nilai**
  ---------------------------------------------------- ------------------
                         Epoch                                 2

                       Batch Size                              8

                     Learning Rate                            2e-5

                   Max Length (token)                         128
  -----------------------------------------------------------------------

Model dilatih menggunakan 11.337 data latih dan dievaluasi secara
berkala menggunakan 1.417 data validasi untuk memantau perkembangan
performa selama pelatihan. Pemanfaatan data validasi yang terpisah
bertujuan mendeteksi overfitting secara dini kondisi ketika model
terlalu menyesuaikan diri terhadap data latih sehingga kehilangan
kemampuan generalisasi terhadap data baru.

## 3.8 Evaluasi Model

Evaluasi model dilakukan menggunakan data uji (*test set*) yang tidak
pernah diikutsertakan dalam proses pelatihan maupun validasi. Pemisahan
yang ketat ini mengukur kemampuan generalisasi model secara objektif
seberapa baik model mengklasifikasikan ulasan yang benar-benar baru.
Dalam konteks pengembangan model, data latih digunakan untuk membangun
representasi model, data validasi untuk pemantauan dan penyesuaian
selama pelatihan, sedangkan data uji berfungsi sebagai penilai akhir
yang netral.

Metrik evaluasi yang digunakan mencakup akurasi (*accuracy*), presisi
(*precision*), *recall*, *F1-score* per kelas, *macro F1-score*,
*weighted F1-score*, dan *confusion matrix*. Kombinasi metrik ini
dipilih karena masing-masing memberikan perspektif berbeda terhadap
performa model: akurasi menggambarkan ketepatan prediksi secara
keseluruhan, presisi mengukur kemampuan model menghindari *false*
*positive*, *recall* menilai kemampuan model menemukan seluruh data
positif, dan F1-score menyeimbangkan keduanya. *Scikit-learn*
menyediakan fungsi evaluasi *accuracy_score, precision_score,
recall_score, f1_score*, dan *confusion_matrix* untuk mengukur
metrik-metrik tersebut.

**Tabel 3. 8 Evaluasi Model**

  -------------------------------------------------------------------------
    **Metrik    **Keterangan**
   Evaluasi**   
  ------------- -----------------------------------------------------------
   *Accuracy*   Proporsi prediksi yang benar terhadap seluruh data uji,
                digunakan untuk mengukur ketepatan prediksi model secara
                keseluruhan.

   *Precision*  Proporsi prediksi positif yang benar-benar merupakan kelas
                positif, mengukur kemampuan model menghindari *false
                positive.*

    *Recall*    Proporsi data yang benar-benar positif dan berhasil
                diprediksi sebagai positif, mengukur kemampuan model
                menemukan seluruh data positif.

   *F1-score*   Rata-rata harmonik antara *precision* dan *recall* untuk
                setiap kelas.

     *Macro     Rata-rata *F1-score* dari seluruh kelas tanpa
    F1-score*   mempertimbangkan jumlah data tiap kelas, sehingga lebih
                sensitif terhadap performa pada kelas minoritas seperti
                kelas netral.

    *Weighted   Rata-rata F1-score tertimbang berdasarkan jumlah data tiap
    F1-score*   kelas.

   *Confusion   Matriks yang menampilkan jumlah prediksi benar dan salah
     matrix*    untuk setiap kombinasi kelas aktual dan kelas prediksi.
  -------------------------------------------------------------------------

Hasil evaluasi model pada data uji menggunakan dataset dan label V3
(baseline v3) disajikan pada tabel berikut.

Tabel 3. 9 Hasil Evaluasi Model IndoBERT (Baseline v3)

  -----------------------------------------------------------------------
                  **Metrik Evaluasi**                      **Nilai**
  ---------------------------------------------------- ------------------
                    *Test Accuracy*                          0,9316

                 *Test Macro F1-score*                       0,8774

                *Test Weighted F1-score*                     0,9309
  -----------------------------------------------------------------------

## 3.9 Perancangan Dashboard Streamlit

Sebagai tahap penutup, penelitian mengembangkan *dashboard* interaktif
menggunakan framework Streamlit berbasis Python. Streamlit dipilih
karena kemampuannya mengubah skrip Python menjadi aplikasi web
interaktif dengan penulisan kode yang relatif sederhana, sehingga sesuai
untuk menyajikan hasil penelitian yang melibatkan visualisasi dan
eksplorasi data secara dinamis.

*Dashboard* yang dikembangkan menyajikan seluruh aspek penelitian dalam
satu antarmuka terintegrasi, mencakup sepuluh halaman dengan fungsi yang
saling melengkapi sebagaimana dijabarkan pada tabel berikut.

Tabel 3. 10 Fitur Dashboard Streamlit

  -----------------------------------------------------------------------
    **Fitur**    **Keterangan**
  -------------- --------------------------------------------------------
   *Distribusi   Visualisasi sebaran data berdasarkan subset (train,
     dataset*    *validation*, test) dan distribusi label sentimen.

      *Hasil     Tampilan distribusi label hasil pelabelan otomatis serta
    labeling*    informasi proses pelabelan.

    *v model*    Informasi konfigurasi hyperparameter dan proses
                 pelatihan model IndoBERT.

    *Evaluasi    Tampilan metrik evaluasi hasil pengujian model pada data
      model*     uji.

    *Confusion   Visualisasi matriks konfusi untuk melihat performa
     matrix*     prediksi per kelas sentimen.

      *Error     Analisis kesalahan prediksi model untuk memahami pola
    analysis*    dan tipe kesalahan yang paling sering terjadi.

     *Keyword    Identifikasi kata kunci yang sering muncul pada ulasan
      issue*     yang salah diklasifikasikan.

   *Word cloud*  Representasi visual frekuensi kata yang paling sering
                 muncul pada setiap kelas sentimen.

  Demo prediksi  Fitur interaktif yang memungkinkan pengguna memasukkan
     sentimen    teks ulasan secara langsung dan mendapatkan prediksi
                 sentimen secara *real-time*.
  -----------------------------------------------------------------------

*Dashboard* ini menjembatani hasil analisis teknis dengan kebutuhan
penyampaian informasi yang mudah dipahami, baik oleh peneliti maupun
pemangku kepentingan yang ingin memahami sentimen pengguna terhadap
aplikasi JakOne Mobile.
