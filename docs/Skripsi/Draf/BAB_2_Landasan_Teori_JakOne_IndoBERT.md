# 2. TINJAUAN PUSTAKA

## 2.1 Analisis Sentimen

Analisis sentimen merupakan salah satu bidang dalam *Natural Language
Processing* (*NLP*) yang bertujuan untuk mengidentifikasi dan
mengategorikan opini atau emosi yang ada dalam sebuah teks. Menurut
Rivaldi,R.C & Wismarini,T.D (2024), analisis sentimen memanfaatkan
komputasional untuk memahami dan mengolah bahasa manusia melalui tahapan
seperti filtering dan steamming, yang berfungsi untuk menyaring
kata-kata tidak bermakna seta menyederhanalan struktur kata sebelum
dilakukan proses klasifikasi. Pendekatan ini berguna untuk memahami
persepsi masyarakat terhadap suatu produk atau layanan secara otomatis
dan dalam skala besar.

Dalam klasifikasi sentimen, umumnya terdapat tiga kategori yang
digunakan, yaitu positif, negatif, dan netral. Sentimen yang positif
menunjukkan tingkat kepuasan atau penilaian baik dari pengguna, sentimen
negatif menunjukkan bahwa ketidakpuasan atau kritik, sedangkan sentimen
netral menunjukkan bahwa teks tersebut tidak secara jelas menunjukan
kedenderungan yang jelas kesalah satu sisi. Pengelompokan dalam tiga
kelas kategori ini banyak digunakan dalam penelitian yang berkaitan
dengan ulasan produk dan layanan digital.

Dalam penelitian ini, analisis sentimen digunakan pada ulasan pengguna
terhadap aplikasi JakOne Mobile yang dari Google Play Store. Tujuannya
adalah untuk menganalisis tren kecenderungan sentimen pengguna terhadap
aplikasi tersebut secara otomatis dengan menggunakan model IndoBERT.
Dengan demikian, hasil analisis dapat memberikan pandangan yang objektif
mengenai kualitas layanan dari sudut pandang pengguna.

## 2.2 Ulasan Pengguna

Ulasan pengguna adalah opini yang diberikan oleh pengguna terhadap
layanan mengenai produk atau layanan melalui platform digital. Dalam
konteks aplikasi mobile, ulasan pengguna umumnya dapat diakses dan
tersedia secara publik pada aplikasi seperti Google Play Store. Menurut
Tarwoto et al. (2025), ulasan pengguna pada aplikasi layanan publik
berbasis digital dapat menjadi sumber data yang representatif untuk
mengukur tingkat kepuasan masyarakat secara otomatis, sehingga
pendekatan serupa relevan diterapkan pada ulasan pengguna aplikasi
layanan publik lainnya, termasuk aplikasi perbankan digital seperti
JakOne Mobile.

Google Play Store memberikan kesempatan kepada pengguna untuk memberikan
penilaian berupa bintang (antara 1 hingga 5) dan juga menyertakan ulasan
dalam bentuk teks secara bersamaan. Teks ulasan ini mengandung berbagai
sentimen yang dapat dianalisis untuk memahami kepuasan serta keluhan
pengguna. Penelitian seperti yang dilakukan dapat menunjukkan bahwa
ulasan aplikasi di Google Play Store bisa digunakan sebagai dataset yang
representatif untuk analisis sentimen berbasis teks.

Dalam penelitian ini, ulasan dari pengguna aplikasi JakOne Mobile
menjadi sumber data utama. Ulasan tersebut diambi langsung dari Google
Play Store dengan menggunakan teknik web scraping dan selanjutnya
diproses untuk keperluan klasifikasi sentimen.

## 2.3 JakOne Mobile

JakOne Mobile adalah aplikasi perbankan digital yang dikembangkan oleh
Bank DKI, sebuah lembaga perbankan yang dimiliki oleh Pemerintah
Provinsi DKI Jakarta. Aplikasi ini menyediakan berbagai layanan keuangan
digital, seperti transfer dana, pembayaran tagihan, pembelian pulsa,
serta akses informasi mengenai rekening. Sebagai aplikasi layanan publik
yang beroperasi di area perkotaan, JakOne Mobile memiliki basis pengguna
besar dan bervariasi dari berbagai latar belakang.

Dengan meningkatnya pengguna layanan keuangan digital di Indonesia,
aplikasi seperti JakOne Mobile mendapatkan banyak ulasan dari para
penggunanya di Google Play Store. Ulasan-ulasan tersebut
merepresentasikan pengalaman langsung pengguna terhadap layanan yang
disediakan. Oleh karena itu, analisis data ulasan dari JakOne Mobile
menjadi objek yang relevan untuk diteliti dalam penelitian analisis
sentimen.

Penelitian ini memilih JakOne Mobile sebagai objek penelitian karena
aplikasi ini merupakan layanan perbankan digital yang dikembangkan oleh
pemerintah daerah yang belum banyak diteliti sebelumnya dari perspektif
analisis sentimen. Dengan menganalisis sentimen pengguna, diharapkan
penelitian ini dapat memberikan masukan informasi yang berguna bagi
pengembang dan pengelola aplikasi.

## 2.4 Pyhton

Python adalah bahasa pemrograman tingkat tinggi yang banyak digunakan
untuk pengembangan aplikasi yang berkaitan dengan data, kecerdasan
buatan, dan *Natural Language Processing* (NLP). Bahasa ini menjadi
pilihan banyak pengguna karena memiliki sintaks yang mudah dipahami,
komunitas yang luas, serta dukungan perpustakaan yang lengkap. Dalam
bidang NLP dan analisis sentimen, Python menyediakan perpustakaan
seperti *Transformers*, *Scikit-learn*, Pandas, NumPy, Matplotlib, dan
Seaborn. Perpustakaan ini mendukung langkah-langkah pengolahan data,
pembuatan model, evaluasi, dan visualisasi hasil penelitian.

Penggunaan Python dalam penelitian ini sangat berperan dalam pengolahan
data dan penerapan model IndoBERT. Python dimanfaatkan dalam beberapa
tahapan, seperti pengumpulan data ulasan, *preprocessing* teks,
tokenisasi, pelatihan model, dan evaluasi hasil klasifikasi sentimen.
Perpustakaan *Hugging Face* *Transformers* mempermudah pemanfaatan model
*pre-trained* sebelumnya seperti BERT dan IndoBERT karena mendukung
proses *fine-tuning* dan prediksi teks. Dengan dukungan tersebut, Python
menjadi alat yang sesuai untuk membangun sistem analisis sentimen
menggunakan *deep learning*.

Selain itu, Python juga dapat digunakan untuk mengotomatisasi proses
pengambilan dan pengolahan data ulasan dari Google Play Store sehingga,
Python dimanfaatkan dalam tahapan analisis ulasan pengguna, mulai dari
*data scraping*, *preprocessing*, pemodelan sentimen, hingga visualisasi
hasil. Hal ini menunjukkan bahwa Python memiliki peran penting dalam
penelitian berbasis data teks. Dengan demikian, Python digunakan dalam
penelitian ini sebagai alat bantu untuk menganalisis sentimen dari
ulasan pengguna aplikasi JakOne Mobile dengan menggunakan IndoBERT.

## 2.5 Natural Language Processing

Natural Language Processing (NLP) adalah bidang ilmu yang menggabungkan
linguistik komputasi dan kecerdasan buatan sehingga komputer dapat
memahami, mengolah, dan menghasilkan bahasa manusia. Menurut Jurafsky
dan Martin (2023), NLP merupakan disiplin ilmu yang memadukan komputasi
linguistik dengan kecerdasan buatan guna membekali komputer dengan
kemampuan untuk memahami, menginterpretasikan, dan memproduksi bahasa
manusia. Bidang ini mencakup serangkaian tugas komputasi yang beroperasi
pada berbagai tingkat abstraksi bahasa, mulai dari pemrosesan unit
leksikal terkecil hingga pemahaman konteks dan makna pada level wacana.
NLP menjadi fondasi teknologi bahasa modern, termasuk analisis sentimen,
ringkasan otomatis, dan sistem tanya jawab.

Perkembangan NLP semakin cepat dengan adanya model berbasis Transformer
yang dapat memproses teks dalam konteks yang lebih luas. Model-model
seperti BERT, GPT, serta versi-versinya telah menjadi tonggak penting
dalam kemajuan NLP saat ini karena dapat memahami makna kata dalam
keseluruhan konteks kalimat. Pendekatan ini sangat berbeda dari metode
tradisional dalam NLP yang hanya menggunakan aturan atau statistik
sederhana.

Dalam penelitian ini, NLP berperan sebagai dasar yang menghubungkan
setiap fase tahapan dalam proses, mulai dari pembersihan teks, pelabelan
sentimen berbasis leksikon, hingga pelatihan model deep learning dengan
memanfaatkan IndoBERT untuk mengklasifikasikan sentimen dari ulasan
pengguna JakOne Mobile.

## 2.6 Text Preprocessing

Text preprocessing adalah tahapan awal dalam pengolahan dan manipulasi
teks yang bertujuan untuk membersihkan dan menyederhanakan informasi
dari data sebelum digunakan dalam proses analisis atau pelatihan model.
Haddi et al. (2013) menegaskan bahwa proses [pra-pengolahan]{.mark} teks
bukan sekadar tahapan opsional, melainkan merupakan komponen kritis yang
secara langsung menentukan kualitas representasi fitur dan pada akhirnya
memengaruhi performa model klasifikasi sentimen. Tahapan ini berfungsi
untuk mereduksi variabilitas linguistik yang tidak informatif, seperti
variasi ejaan, penggunaan karakter khusus, dan kata-kata yang tidak
bermakna secara semantik (*stopwords*), sehingga model dapat berfokus
pada fitur-fitur yang secara leksikal relevan untuk analisis sentimen.

Beberapa tahapan preprocessing yang umum dilakukan antara lain adalah
case folding (mengubah teks menjadi huruf kecil), penghapusan karakter
khusus dan angka, tokenisasi (memecah kalimat menjadi kata-kata),
penghapusan stopword (kata yang tidak memiliki makna penting), dan
normalisasi kata (mengganti singkatan atau kata tidak baku ke bentuk
yang lebih standar) preprocessing yang baik akan meningkatkan kualitas
data dan secara langsung berdampak pada performa model klasifikasi.

Dalam penelitian ini, preprocessing dilakukan sebelum proses pelabelan
menggunakan InSet Lexicon serta sebelum data dimasukkan ke dalam model
IndoBERT. Tahapan ini memastikan bahwa data yang digunakan bersih,
konsisten, dan siap untuk dianalisis lebih lanjut.

## 2.7 Pelabelan Sentimen Berbasis Lexicon

Pelabelan sentimen dengan pendekatan lexicon adalah metode untuk
pemberian label sentimen pada teks dengan cara menghitung skor kata-kata
yang terdapat dalam kamus sentimen (lexicon). Setiap kata dalam lexicon
memiliki nilai skor positif atau negatif. Jika total skor dari seluruh
kata dalam suatu teks bernilai positif, maka teks tersebut dilabeli
sentimen positif; jika negatif, dilabeli sentimen negatif; dan jika nol
atau berada dalam rentang tertentu, dilabeli netral).

Menurut Liu (2022), pelabelan sentimen berbasis leksikon merupakan
pendekatan komputasional yang memanfaatkan kamus kata bersentimen
(*sentiment lexicon*) sebagai sumber pengetahuan utama untuk menentukan
orientasi polaritas suatu teks. Setiap kata dalam leksikon diasosiasikan
dengan nilai numerik yang merepresentasikan kekuatan dan arah
sentimennya. Dengan mengakumulasikan skor-skor tersebut secara
keseluruhan dalam sebuah teks, dapat ditentukan apakah teks tersebut
bersentimen positif, negatif, atau netral. Keunggulan utama pendekatan
ini terletak pada sifatnya yang tidak bergantung pada data latih
berlabel (*unsupervised*), sehingga dapat diterapkan secara langsung
pada dataset yang belum memiliki anotasi, termasuk untuk keperluan
penciptaan label awal pada pelatihan model *supervised* berikutnya..

Dalam penelitian ini, teknik pelabelan yang berbasis lexicon digunakan
untuk memberikan label awal pada dataset berisi ulasan pengguna JakOne
Mobile. Label yang dihasilkan selanjutnya digunakan sebagai data latih
untuk melatih model IndoBERT.

## 2.8 InSet Lexicon

InSet Lexicon (Indonesian Sentiment Lexicon) menurut Koto dan
Rahmaningtyas (2017), merupakan kamus sentimen berbahasa Indonesia yang
dibangun untuk mengidentifikasi opini tertulis dan mengategorikannya ke
dalam opini positif atau negatif. Leksikon ini dirancang khusus untuk
menganalisis sentimen publik terhadap topik, peristiwa, atau produk
tertentu dalam teks mikroblog berbahasa Indonesia. InSet Lexicon terdiri
dari 3.609 kata positif dan 6.609 kata negatif, dengan bobot skor yang
berkisar antara -5 hingga +5 untuk merepresentasikan intensitas
polaritas sentimen setiap kata. Dalam evaluasinya, InSet Lexicon
menunjukkan performa yang lebih baik dibandingkan kamus sentimen bahasa
Indonesia yang telah ada sebelumnya karena mencakup kosakata yang lebih
komprehensif dan relevan..

InSet Lexicon menjadi salah satu kamus sentimen bahasa Indonesia yang
banyak digunakan dalam penelitian NLP yang menggunakan Indonesia karena
memiliki kosakata yang cukup lengkap dan relevan untuk berbagai domain
teks. Sehingga peneliti menggunakan InSet Lexicon sebagai alat pelabelan
otomatis sebelum proses pelatihan model machine learning atau deep
learning.

Dalam penelitian ini, InSet Lexicon digunakan untuk secara otomastis
memberikan label sentimen pada setiap ulasan pengguna JakOne Mobile.
Proses pelabelan dilakukan dengan cara menjumlahkan skor dari kata-kata
yang ada dalam setiap ulasan berdasarkan nilai yang tertera dalam kamus,
kemudian menentukan label sentimen berdasarkan hasil skor yang
diperoleh.

## 2.9 Transformer 

Transformer merupakan arsitektur jaringan saraf tiruan yang
diperkenalkan oleh Vaswani et al. (2017) Transformer dengan struktur
*encoder-decoder* yang masing-masing tersusun atas lapisan-lapisan
identik yang dapat ditumpuk. Setiap lapisan *encoder* terdiri dari dua
sub-lapisan utama: pertama, mekanisme *multi-head self-attention*; dan
kedua, jaringan saraf *feedforward* yang diaplikasikan per posisi secara
independen. *Multi-head attention* bekerja dengan memproyeksikan
*query*, *key*, dan *value* ke dalam beberapa ruang representasi berbeda
secara paralel --- yang disebut *attention heads* --- sehingga model
dapat menangkap aspek-aspek relasional yang berbeda secara bersamaan.
Hasil dari masing-masing *head* kemudian digabungkan dan diproyeksikan
kembali untuk menghasilkan representasi akhir. Dibandingkan dengan
arsitektur RNN yang memproses token secara sekuensial dan rentan
terhadap masalah *vanishing gradient* pada sekuens panjang, Transformer
mampu menangkap dependensi jarak jauh dengan kompleksitas komputasi yang
konstan per lapisan. Keunggulan inilah yang kemudian menjadikan
arsitektur Transformer sebagai fondasi bagi serangkaian model bahasa
mutakhir, termasuk BERT yang menjadi basis dari model IndoBERT yang
digunakan dalam penelitian ini.

Secara umum, Transformer terdiri dari dua komponen utama, yaitu
*encoder* dan *decoder*. *Encoder* berfungsi untuk membaca dan
megonversi teks yang masuk menjadi representasi yang dapat dipahami oleh
model, sedangkan *decoder* digunakan untuk menghasilkan *ouput*
berdasarkan representasi tersebut. Salah satu manfaat utama dari
Transformer adalah kemampuannya untuk memproses kata-kata bersamaan,
sehingga lebih efisien dibandingkan model -- model sebelumnya seperti
RNN dan LSTM. Selain itu, mekanisme *self-attention* membantu model
dalam menangkap konteks kata dengan berdasarkan keterkaitan dengan kata
lain dalam satu kalimat.

Transformer adalah struktur yang penting dalam pengolahan bahasa alami
karena dapat memahami hubungan antara kata dalam konteks tertentu.
Arsitektur ini kemudian menjadi dasar dari berbagai model bahasa modern,
termasuk BERT. Dalam penelitian ini, pemahaman tentang Transformer
penting karena IndoBERT merupakan model yang dikembangkan dari
arsitektur BERT berbasis Transformer. Oleh karena itu, konsep
Transformer menjadi dasar teori yang mendukung penerapan model IndoBERT
dalam analisis sentimen dari ulasan pengguna aplikasi JakOne Mobile.

## 2.10 Klasifikasi Teks

Klasifikasi teks adalah suatu tugas dalam NLP yang bertujuan untuk
mengelompokkan suatu dokumen atau bagian-bagian teks ke dalam satu atau
lebih kategori yang telah ditentukan sebelumnya. Proses ini dilakukan
secara otomatis menggunakan algoritma machine learning atau deep
learning yang dilatih menggunakan data yang memiliki label. Menurut
Kowsari et al. (2019), klasifikasi teks merupakan tugas fundamental
dalam pemrosesan bahasa alami yang secara operasional bertujuan
memetakan setiap dokumen teks ke dalam satu atau lebih kategori dari
sekumpulan kelas yang telah didefinisikan sebelumnya. Tugas ini
memerlukan tahapan transformasi teks dari format tidak terstruktur
menjadi representasi numerik yang bermakna, yang selanjutnya digunakan
sebagai masukan bagi algoritma pembelajaran mesin untuk mempelajari pola
pembeda antarkelas.

Keberhasilan proses klasifikasi teks sangat bergantung pada kapasitas
model untuk memahami relasi dan pola yang kompleks dan nonlinear dalam
data tekstual, sehingga pemilihan arsitektur model yang tepat menjadi
faktor penentu performa klasifikasi.Dalam konteks analisis sentimen,
klasifikasi teks dilakukan untuk mengelompokkan teks ke dalam ketegori
sentimen positif, negatif, atau netral. Model yang digunakan untuk
klasifikasi bisa berupa model berbasis statistik seperti Naive Bayes dan
Support Vector Machine, serta model deep learning seperti LSTM, CNN,
atau BERT. Pemilihan model bergantung pada kompleksitas data dan tingkat
akurasi yang diinginkan.

Penelitian ini memanfaatkan IndoBERT sebagai model untuk klasifikasi
teks mengkategorikan ulasan dari pengguna JakOne Mobile ke dalam tiga
ketegori sentimen. Pendekatan ini dipilih karena model berbasis
Transformer seperti IndoBERT telah terbukti menghasilkan tingkat akurasi
yang lebih tinggi dibandingkan model klasifikasi tradisional, terutama
untuk teks dalam bahasa Indonesia.

## 2.11 Pembagian Dataset Train, Validation, dan Test

Pembagian dataset merupakan tahapan penting dalam pengembangan model
*machine learning* dan *deep learning*. Menurut Prasetyo (2024),
pembagian dataset dilakukan untuk memisahkan data ke dalam beberapa
bagian, seperti data latih, data validasi, dan data uji. Data latih
digunakan untuk melatih model, data validasi digunakan untuk memantau
proses pelatihan, sedangkan data uji digunakan untuk mengevaluasi
performa akhir model. Pembagian ini bertujuan agar hasil evaluasi model
lebih objektif dan tidak hanya baik pada data yang digunakan saat
pelatihan.

Secara umum, pembagian dataset membantu model untuk diuji pada data yang
belum pernah ditemui sebelumnya. Hal ini penting untuk mengetahui apakah
model dapat mengenali pola secara umum atau hanya meningat data latih.
Jika model terlalu menyesuaikan diri dengan data latih, maka dapat
menyebabkan *overfitting*, yaitu kondisi ketika model memiliki performa
baik pada data latih tetapi kurang baik pada data baru. Oleh karena itu,
pemisahan data latih, validasi, dan uji perlu dilakukan dengan tepat
agar hasil evaluasi yang dihasilkan lebih dapat dipercaya.

Pembagian dataset berperan penting dalam menjaga kualitas proses
pelatihan dan evaluasi model. Dalam penelitian ini, dataset ulasan
pengguna aplikasi JakOne Mobile dibagi ke dalam beberapa bagian agar
model IndoBERT dapat dilatih dan diuji secara terpisah. Pembagian ini
juga perlu memperhatikan distribusi kelas sentimen positif, negatif, dan
netral agar setiap subset tetap mewakili data secara seimbang. Dengan
demikian, pembagian dataset menjadi salah satu tahap penting sebelum
melakukan proses pelatihan dan evaluasi model analisis sentimen
dilakukan.

## 2.12 Machine Learning dan Deep Learning

Menurut Fajri, Tholib, dan Yuliana (2022), machine learning merupakan
cabang ilmu dari kecerdasan buatan yang memanfaatkan data untuk
mengembangkan model statistik, sehingga sistem mampu membuat prediksi
dan mempelajari pola tertentu berdasarkan pengalaman secara otomatis
tanpa harus diprogram secara eksplisit untuk setiap kasus. Salah satu
turunan dari machine learning adalah jaringan saraf tiruan (Artificial
Neural Network), yaitu sistem yang menyerupai struktur jaringan saraf
biologis dan terdiri atas lapisan input, lapisan output, serta satu atau
lebih lapisan tersembunyi. Ketika jumlah lapisan tersembunyi pada
jaringan saraf tiruan tersebut diperbanyak secara signifikan, pendekatan
ini berkembang menjadi deep learning, yang memungkinkan model
mengekstraksi representasi fitur yang lebih kompleks dan abstrak secara
bertingkat dibandingkan algoritma machine learning konvensional.
Perbedaan mendasar antara kedua pendekatan tersebut terletak pada
kedalaman arsitektur dan tingkat otomatisasi dalam proses ekstraksi
fitur, di mana deep learning cenderung lebih unggul dalam menangani data
berskala besar dan tidak terstruktur, seperti teks ulasan pengguna pada
aplikasi mobile banking.x

Dalam penelitian ini, deep learning digunakan dengan menggunakan model
IndoBERT yang merupakan turunan dari arsitektur BERT. Metode deep
learning dipilih karena kemampuan untuk menangkap nuansa bahasa
Indonesia yang beragam dan kompleks, sehingga diharapkan dapat
menghasilkan klasifikasi sentimen yang lebih akurat.

## 2.13 BERT

BERT (Bidirectional Encoder Representations from Transformers) adalah
sebuah model bahasa yang didasarkan pada arsitektur Transformer. Salah
satu keunggulan BERT dibandingkan model-model sebelumnya adalah
kemampuannya untuk memahami konteks suatu kata dari dua arah, yaitu
dengan mempertimbangkan kata-kata baik yang ada di sebelah kiri dan
kanan kata tersebut dalam suatu kalimat. Hal ini berbeda dengan
model-model sebelumnya seperti ELMo dan GPT yang hanya memproses teks
dalam satu arah.

BERT dilatih dengan dua tugas utama, yaitu Masked Language Model (MLM)
dan Next Sentence Prediction (NSP), menggunakan dataset data teks yang
sangat besar. Proses pelatihan ini menghasilkan representasi kata yang
kaya konteks dan dapat digunakan kembali untuk berbagai tugas NLP
melalui proses fine-tuning. Konsep tersebut diperkenalkan oleh Devlin et
al. (2019) melalui model BERT (Bidirectional Encoder Representations
from Transformers), yaitu model representasi bahasa yang dirancang untuk
melakukan pre-training representasi bidirectional secara mendalam dengan
mengondisikan konteks kiri dan kanan suatu kata secara bersamaan pada
seluruh lapisan arsitektur Transformer. Pendekatan bidirectional ini
menjadi pembeda utama BERT dari model bahasa sebelumnya yang umumnya
hanya memproses teks secara satu arah, sehingga BERT dapat menangkap
hubungan kontekstual antar kata secara lebih komprehensif. Keunggulan
lain dari BERT adalah kemampuannya untuk di-fine-tune pada berbagai
tugas pemrosesan bahasa alami, seperti klasifikasi teks dan analisis
sentimen, hanya dengan menambahkan satu lapisan keluaran tambahan tanpa
memerlukan modifikasi arsitektur yang signifikan, sehingga model ini
menjadi dasar bagi pengembangan berbagai model turunan berbasis bahasa,
termasuk model yang dikembangkan khusus untuk bahasa Indonesia..

Dalam penelitian ini, arsitektur BERT digunakan sebagai dasar untuk
model IndoBERT yang digunakan. Memahami bagaimana kerja BERT adalah hal
yang penting karena prinsip-prinsip yang sama diterapkan dalam IndoBERT,
termasuk mekanisme self-attention dan proses fine-tuning untuk tugas
klasifikasi sentimen.

## 2.14 IndoBERT

IndoBERT merupakan model BERT yang yang dirancang khusus untuk memahami
bahasa Indonesia. Model ini dilatih dengan menggunakan kumpulan teks
berbahasa Indonesia dalam jumlah besar, sehingga memahami yang lebih
baik terhadap karakteristik bahasa Indonesia dibandingkan model BERT
multibahasa (mBERT). IndoBERT tersedia dalam beberapa varian ukuran,
yaitu IndoBERT-base dan IndoBERT-large.

Penerapan menggunakan model IndoBERT dalam analisis sentimen untuk
bahasa Indonesia telah terbukti menghasilkan performa yang lebih baik
dibandingkan dengan model BERT berbahasa umum. IndoBERT memperoleh skor
yang lebih tinggi pada beragam tugas NLP berbahasa Indonesia, termasuk
dalam klasifikasi teks dan analisis sentimen, jika dibandingkan model
multilingual yang tidak dilatih secara spesifik untuk bahasa Indonesia.

Dalam penelitian ini, IndoBERT diterapkan sebagai model utama untuk
mengklasifikasikan sentimen dari ulasan pengguna JakOne Mobile. Proses
yang dilakukan meliputi fine-tuning model IndoBERT menggunakan dataset
ulasan yang telah diberi label melalui InSet Lexicon, sehingga model
dapat memahami pola-pola sentimen yang relevan untuk konteks aplikasi
perbankan digital.

## 2.15 Evaluasi Model Klasifikasi

Evaluasi model klasifikasi dilakukan untuk mengukur seberapa baik model
yang telah dibuat dalam melakukan prediksi yang akurat. Terdapat
beberapa metrik evaluasi yang umum digunakan dalam klasifikasi teks,
yaitu accuracy, precision, recall, dan F1-score. Accuracy mengukur
proporsi prediksi yang benar dari seluruh data uji. Precision mengukur
tingkat ketepatan dari prediksi positif yang dihasilkan model, sedangkan
recall mengukur seberapa banyak data positif yang berhasil terdeteksi
(Sokolova dan Lapalme, 2022).

F1-score adalah rata-rata harmonik yang menghubungkan precision dan
recall, sehingga memberikan gambaran yang lebih seimbang mengenai
kinerja performa model, terutama ketika ada ketidakseimbangan pada
distribusi kelas. Dalam klasifikasi multi-kelas seperti penelitian ini
yang memiliki tiga kelas sentimen, digunakan macro average, yaitu
rata-rata metrik dari setiap kelas tanpa mempertimbangkan jumlah data
per kelas. Selain itu, confusion matrix digunakan untuk
memvisualisasikan dengan detail bagaimana distribusi prediksi model pada
setiap kelas.

Dalam penelitian ini, evaluasi dilakukan menggunakan pengukuran
accuracy, precision, recall, F1-score dengan macro average, serta
confusion matrix. Penggunaan beragam metrik ini bertujuan untuk
memberikan gambaran yang menyeluruh secara komprehensif dan objektif
tentang kinerja performa model IndoBERT dalam mengklasifikasikan
sentimen dari ulasan pengguna JakOne Mobile.

## 2.16 Penelitian Terdahulu

Penelitian terdahulu dikaji untuk memahami perkembangan studi yang
relevan dengan topik penelitian ini, sekaligus untuk mengidentifikasi
posisi penelitian ini di antara penelitian yang sudah ada. Berikut
disajikan ringkasan beberapa penelitian terdahulu yang berkaitan dengan
analisis sentimen, IndoBERT, pelabelan berbasis lexicon, dan klasifikasi
ulasan aplikasi.

  ----------------------------------------------------------------------------
   **No**  **Penulis &   **Tujuan**           **Kelebihan**   **Kekurangan**
           Tahun**                                            
  -------- ------------- -------------------- --------------- ----------------
     1     Saputra, A.   Menganalisis         Menggunakan     Dataset masih
           R., et al.    sentimen ulasan      model BERT      terbatas dan
           (2024)\       pengguna aplikasi    khusus bahasa   belum mencakup
           Universitas   mobile banking       Indonesia       variasi dialek
           Gunadarma     menggunakan IndoBERT dengan          pengguna
                                              pelabelan       
                                              otomatis        

     2     Wibirama, S., Melakukan            Fokus pada      Tidak melakukan
           et al.        klasifikasi sentimen aplikasi sektor perbandingan
           (2023)\       ulasan aplikasi      publik yang     dengan model
           Universitas   pemerintah dari      relevan dengan  lain sebagai
           Gunadarma     Google Play Store    objek           baseline
                                              penelitian ini  

     3     Nugroho, P.,  Membandingkan metode Memberikan      Perbandingan
           et al.        pelabelan lexicon    alternatif      masih terbatas
           (2022)\       dan anotasi manual   pelabelan yang  pada domain
           Universitas   untuk analisis       efisien tanpa   berita dan media
           Gunadarma     sentimen bahasa      anotasi manual  sosial
                         Indonesia                            

     4     Pramana, D.,  Menganalisis         Dataset lebih   Tidak
           et al.        sentimen ulasan      besar dan       menggunakan
           (2025)\       fintech menggunakan  beragam, domain pelabelan
           Universitas   model BERT bahasa    fintech relevan berbasis
           Indonesia     Indonesia            dengan          lexicon, seluruh
                                              perbankan       label diperoleh
                                              digital         dari anotasi
                                                              manual

     5     Hidayah, N.,  Mengklasifikasikan   Melakukan       Domain
           et al.        sentimen ulasan      perbandingan    e-commerce
           (2025)\       aplikasi e-commerce  antara model    berbeda dari
           Universitas   menggunakan IndoBERT deep learning   domain
           Gadjah Mada   dan SVM              dan machine     perbankan,
                                              learning klasik sehingga
                                                              generalisasi
                                                              mungkin terbatas
  ----------------------------------------------------------------------------

  : Tabel 2. 1 Ringkasan Penelitian Terdahulu

Berdasarkan tabel di atas, terlihat bahwa banyak penelitian terdahulu
telah menggunakan IndoBERT dan InSet Lexicon dalam analisis sentimen
pada berbagai bidang, termasuk mobile banking dan aplikasi pemerintah.
Penelitian ini mengikuti metode yang sama dengan menggunakan InSet
Lexicon untuk pelabelan otomatis dan IndoBERT untuk klasifikasi
sentimen, namun berfokus pada aplikasi JakOne Mobile yang merupakan
layanan perbankan digital milik pemerintah daerah yang belum pernah
menjadi objek penelitian serupa sebelumnya.
