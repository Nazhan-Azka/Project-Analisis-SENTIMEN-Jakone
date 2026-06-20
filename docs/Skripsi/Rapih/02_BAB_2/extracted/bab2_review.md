# Ekstrak BAB 2 - BAB_2_Landasan_Teori_JakOne_IndoBERT.docx

> Catatan: file ini adalah hasil ekstraksi teks dari DOCX asli untuk kebutuhan review. DOCX asli tidak diubah.

## BAB II

## LANDASAN TEORI

## 2.1 Analisis Sentimen

Analisis sentimen adalah salah satu bidang dalam Natural Language Processing (NLP) yang bertujuan untuk mengenali dan mengklasifikasikan opini atau perasaan yang terkandung dalam suatu teks. Menurut Liu (2022), analisis sentimen didefinisikan sebagai proses komputasi untuk mengidentifikasi dan mengekstrak opini subjektif dari teks, sehingga dapat diketahui apakah suatu teks mengandung sentimen positif, negatif, atau netral. Pendekatan ini sangat bermanfaat untuk memahami sudut pandangan masyarakat secara otomatis dan dalam skala besar.

Terdapat tiga kelas sentimen yang umumnya digunakan dalam analisis sentimen, yaitu positif, negatif, dan netral. Sentimen positif menunjukkan tingkat kepuasan atau penilaian baik dari pengguna, sentimen negatif menunjukkan bahwa ketidakpuasan atau kritik, sedangkan sentimen netral menunjukkan bahwa teks yang tidak secara jelas berpihak pada keduanya. Pengelompokan tiga kelas kategori ini banyak diterapkan dalam penelitian tentang ulasan produk dan layanan digital.

Dalam penelitian ini, analisis sentimen digunakan pada ulasan pengguna dari aplikasi JakOne Mobile yang dikumpulkan dari Google Play Store. Tujuannya adalah untuk menganalisis tren kecenderungan sentimen pengguna terhadap aplikasi tersebut secara otomatis menggunakan model IndoBERT. Dengan demikian, hasil analisis dapat memberikan pandangan yang objektif mengenai kualitas layanan dari sudut pandang pengguna.

## 2.2 Ulasan Pengguna

Ulasan pengguna adalah bentuk ekspresi atau opini yang diberikan oleh pengguna terhadap mengenai produk atau layanan melalui platform digital. Dalam konteks aplikasi mobile, ulasan pengguna umumnya dapat diakses dan tersedia secara publik di platform distribusi aplikasi seperti Google Play Store. Menurut Wibirama et al. (2023), ulasan pengguna menjadi sumber data yang kaya informasi karena mencerminkan pengalaman nyata pengguna dalam berinteraksi dengan aplikasi.

Google Play Store memberikan kesempatan kepada  pengguna untuk melakukan penilaian berupa bintang (1 sampai 5) serta menyertakan komentar dalam bentuk teks secara bersamaan. Teks ulasan ini mengandung berbagai sentimen yang dapat dianalisis untuk memahami kepuasan serta keluhan pengguna. Penelitian seperti yang dilakukan dapat menunjukkan bahwa ulasan aplikasi di Google Play Store dapat digunakan sebagai dataset yang representatif untuk analisis sentimen berbasis teks.

Dalam penelitian ini, ulasan dari pengguna aplikasi JakOne Mobile menjadi sumber data utama. Ulasan tersebut diambil dari Google Play Store secara langsung menggunakan teknik web scraping dan kemudian diproses lebih lanjut untuk tujuan klasifikasi sentimen.

## 2.3 JakOne Mobile

JakOne Mobile adalah aplikasi perbankan digital yang dikembangkan oleh Bank DKI, yaitu lembaga perbankan yang dimiliki oleh Pemerintah Provinsi DKI Jakarta. Aplikasi ini menyediakan berbagai layanan keuangan digital, seperti transfer dana, pembayaran tagihan, pembelian pulsa, serta akses informasi mengenai rekening. Sebagai aplikasi layanan publik yang beroperasi di area perkotaan, JakOne Mobile memiliki banyak pengguna yang cukup besar dan beragam dari berbagai latar belakang.

Dengan meningkatnya penggunaan layanan keuangan digital di Indonesia, aplikasi seperti JakOne Mobile mendapatkan ulasan yang cukup banyak dari para penggunanya di Google Play Store. Ulasan-ulasan tersebut mencerminkan pengalaman pengguna secara langsung terhadap layanan yang disediakan. Oleh karena itu, analisa data ulasan dari JakOne Mobile menjadi objek yang relevan untuk diteliti dalam penelitian analisis sentimen.

Penelitian ini memilih JakOne Mobile sebagai objek penelitian karena aplikasi ini merupakan layanan perbankan digital milik pemerintah daerah yang belum banyak diteliti sebelumnya dari perspektif analisis sentimen. Melalui analisis sentimen pengguna, diharapkan penelitian ini dapat memberikan masukan berharga dan bermanfaat bagi pengembang dan pengelola aplikasi.

## 2.2 Pyhton

Python merupakan bahasa pemrograman tingkat tinggi yang banyak digunakan dalam pengembangan aplikasi berbasis data, kecerdasan buatan, dan Natural Language Processing (NLP). Bahasa ini banyak dipilih karena memiliki sintaks yang sederhana, komunitas yang luas, serta dukungan pustaka yang lengkap. Dalam bidang NLP dan analisis sentimen, Python menyediakan pustaka seperti Transformers, Scikit-learn, Pandas, NumPy, Matplotlib, dan Seaborn. Pustaka tersebut membantu proses pengolahan data, pembangunan model, evaluasi, dan visualisasi hasil penelitian.

Penggunaan Python dalam penelitian ini berperan penting dalam proses pengolahan data dan penerapan model IndoBERT. Python digunakan dalam beberapa tahapan, seperti pengambilan data ulasan, preprocessing teks, tokenisasi, pelatihan model, dan evaluasi hasil klasifikasi sentimen. Pustaka Hugging Face Transformers memudahkan penggunaan model pre-trained seperti BERT dan IndoBERT karena mendukung proses fine-tuning dan prediksi teks. Dengan dukungan tersebut, Python menjadi alat yang sesuai untuk membangun sistem analisis sentimen berbasis deep learning.

Selain itu, Python juga dapat digunakan untuk mengotomatisasi proses pengambilan dan pengolahan data ulasan dari Google Play Store. Dalam penelitian Saputra et al. (2024), Python dimanfaatkan dalam tahapan analisis ulasan pengguna, mulai dari data scraping, preprocessing, pemodelan sentimen, hingga visualisasi hasil. Hal ini menunjukkan bahwa Python memiliki peran penting dalam penelitian berbasis data teks. Dengan demikian, Python digunakan dalam penelitian ini sebagai alat pendukung untuk menganalisis sentimen ulasan pengguna aplikasi JakOne Mobile menggunakan IndoBERT.

## 2.4 Natural Language Processing

Natural Language Processing (NLP) adalah bidang ilmu yang menggabungkan linguistik komputasi dan kecerdasan buatan agar memungkinkan komputer memahami, mengolah, dan menghasilkan bahasa manusia. NLP digunakan dalam berbagai aplikasi, seperti penerjemahan mesin, peringkasan teks, tanya jawab otomatis, dan analisis sentimen. Menurut Jurafsky dan Martin (2023), NLP merupakan dasar dari hampir semua sistem pemrosesan bahasa berbasis komputer yang digunakan saat ini.

Perkembangan NLP semakin pesat seiring dengan kemunculan model berbasis Transformer yang mampu menangani teks dalam konteks yang lebih luas. Model-model seperti BERT, GPT, dan variannya menjadi tonggak penting kemajuan dalam NLP modern karena mampu memahami makna arti kata dalam keseluruhan konteks kalimat. Pendekatan ini sangat berbeda dari metode klasik NLP yang hanya menggunakan aturan atau statistik sederhana.

Dalam penelitian ini, NLP berfungsi sebagai dasar yang menghubungkan setiap fase tahapan proses, mulai dari pembersihan teks, pelabelan sentimen berbasis leksikon, hingga pelatihan model deep learning dengan menggunakan IndoBERT untuk mengklasifikasikan sentimen dari ulasan pengguna JakOne Mobile.

## 2.5 Text Preprocessing

Text preprocessing adalah tahapan awal dalam pengolahan dan menipulasi teks yang bertujuan untuk membersihkan dan menyederhanakan informasi dari  data sebelum digunakan dalam proses analisis atau pelatihan model. Tahapan ini diperlukan karena teks yang belum diolah, terutama yang berasal dari media sosial atau ulasan pengguna, seringkali mengandung karakter tidak relevan, ejaan tidak baku, singkatan, atau simbol yang dapat mengganggu proses komputasi (Saputra et al., 2024).

Beberapa tahapan preprocessing yang umum dilakukan antara lain adalah  case folding (mengubah teks menjadi huruf kecil), penghapusan karakter khusus dan angka, tokenisasi (memecah kalimat menjadi kata-kata), penghapusan stopword (kata yang tidak memiliki makna penting), dan normalisasi kata (mengganti singkatan atau kata tidak baku ke bentuk yang lebih standar) preprocessing yang baik akan meningkatkan kualitas data dan secara langsung berdampak pada performa model klasifikasi.

Dalam penelitian ini, preprocessing dilakukan sebelum proses pelabelan menggunakan InSet Lexicon serta sebelum data dimasukkan ke dalam model IndoBERT. Tahapan ini memastikan bahwa data yang digunakan bersih, konsisten, dan siap untuk dianalisis lebih lanjut.

## 2.6 Pelabelan Sentimen Berbasis Lexicon

Pelabelan sentimen dengan pendekatan lexicon adalah metode untuk pemberian label sentimen pada teks dengan cara menghitung skor kata-kata yang terdapat dalam kamus sentimen (lexicon). Setiap kata dalam lexicon memiliki nilai skor positif atau negatif. Jika total skor dari seluruh kata dalam suatu teks bernilai positif, maka teks tersebut dilabeli sentimen positif; jika negatif, dilabeli sentimen negatif; dan jika nol atau berada dalam rentang tertentu, dilabeli netral (Nugroho et al., 2022).

Salah satu keunggulan dari metode berbasis lexicon adalah tidak memerlukan data yang telah diberi label sebelumnya (unsupervised), sehingga cocok digunakan untuk membuat label awal pada dataset yang belum memiliki anotasi manual. Namun, metode ini juga memiliki kekurangan karena tidak mempertimbangkan konteks kalimat secara menyeluruh, sehingga hasilnya mungkin kurang akurat untuk teks yang mengandung sarkasme atau kalimat majemuk yang kompleks.

Dalam penelitian ini, pelabelan berbasis lexicon diterapkan untuk secara otomatis sebagai metode pemberian label awal pada dataset ulasan pengguna JakOne Mobile. Label yang dihasilkan kemudian digunakan sebagai data latih untuk melatih model IndoBERT.

## 2.7 InSet Lexicon

InSet Lexicon (Indonesian Sentiment Lexicon) adalah kamus sentimen yang dikembangkan khusus untuk bahasa Indonesia oleh Fachrina dan Purwarianti (2017). Kamus ini berisi kata-kata dalam bahasa Indonesia beserta skor polaritas sentimen masing-masing, yang mencakup skor positif untuk kata-kata berkonotasi baik dan skor negatif untuk kata-kata berkonotasi buruk. InSet Lexicon tersedia dalam dua versi, yaitu versi lemma (kata dasar) dan versi adjektiva.

InSet Lexicon menjadi salah satu kamus sentimen bahasa Indonesia yang paling banyak digunakan dalam penelitian NLP berbahasa Indonesia karena mencakup kosakata yang cukup lengkap dan relevan untuk berbagai domain teks. Beberapa penelitian, termasuk Saputra et al. (2024) dan Nugroho et al. (2022), menggunakan InSet Lexicon sebagai alat pelabelan otomatis sebelum proses pelatihan model machine learning atau deep learning.

Dalam penelitian ini, InSet Lexicon digunakan untuk memberikan label sentimen secara otomatis pada setiap ulasan pengguna JakOne Mobile. Proses pelabelan dilakukan dengan cara menghitung total skor kata-kata dalam setiap ulasan berdasarkan nilai yang tercantum dalam kamus, kemudian menentukan label sentimen berdasarkan hasil skor diperoleh.

## 2.8 Klasifikasi Teks

Klasifikasi teks adalah suatu tugas dalam NLP yang bertujuan untuk mengelompokkan suatu dokumen atau bagian-bagian teks ke dalam satu atau lebih kategori yang telah ditentukan sebelumnya. Proses ini dilakukan secara otomatis menggunakan algoritma machine learning atau deep learning yang dilatih menggunakan data yang memiliki label. Menurut Aggarwal (2022), klasifikasi teks merupakan salah satu tugas NLP yang paling banyak diterapkan dalam dunia nyata, termasuk untuk penyaringan spam, analisis sentimen, dan deteksi topik.

Dalam konteks analisis sentimen, klasifikasi teks berfungsi untuk mengelompokkan teks kedalam ketegori kelas sentimen positif, negatif, atau netral. Model yang digunakan untuk klasifikasi dapat mengcangkup model berbasis statistik seperti Naive Bayes dan Support Vector Machine, maupun model berbasis deep learning seperti LSTM, CNN, atau BERT. Pemilihan model bergantung pada kompleksitas data dan tingkat akurasi yang diinginkan.

Penelitian ini menggunakan IndoBERT sebagai model klasifikasi teks untuk mengkategorikan ulasan dari pengguna JakOne Mobile ke dalam tiga ketegori sentimen. Pendekatan ini dipilih karena model berbasis Transformer seperti IndoBERT telah terbukti menghasilkan akurasi yang lebih tinggi dibandingkan model klasifikasi konvensional, terutama pada teks berbahasa Indonesia.

## 2.9 Machine Learning dan Deep Learning

Machine learning adalah suatu pendekatan dalam kecerdasan buatan yang memungkinkan komputer untuk belajar dari data tanpa harus diprogram secara eksplisit. Algoritma machine learning bekerja dengan cara menemukan pola dalam data latih, kemudian menggunakan pola tersebut untuk membuat prediksi pada data baru. Beberapa algoritma machine learning yang umum digunakan dalam klasifikasi teks antara lain Naive Bayes, Logistic Regression, dan Support Vector Machine (Aggarwal, 2022).

Deep learning adalah pengembangan lebih lanjut dari machine learning yang menggunakan jaringan saraf tiruan berlapis-lapis (deep neural network) untuk memproses data yang kompleks. Dalam bidang NLP, deep learning telah memberikan terobosan besar dengan hadirnya model-model seperti Recurrent Neural Network (RNN), Long Short-Term Memory (LSTM), dan yang paling mutakhir adalah model berbasis Transformer seperti BERT (Devlin et al., 2019). Model-model ini mampu memahami konteks bahasa dengan jauh lebih baik dibandingkan metode sebelumnya.

Dalam penelitian ini, deep learning digunakan melalui model IndoBERT yang merupakan turunan dari arsitektur BERT. Metode deep learning dipilih karena kemampuannya dalam menangkap nuansa bahasa Indonesia yang kaya dan kompleks, sehingga diharapkan dapat menghasilkan klasifikasi sentimen yang lebih akurat.

## 2.10 BERT

BERT (Bidirectional Encoder Representations from Transformers) adalah model bahasa berbasis Transformer yang diperkenalkan oleh Devlin et al. pada tahun 2019. Salah satu keunggulann BERT dibandingkan model-model  sebelumnya adalah kemampuannya untuk memahami konteks suatu kata secara dua arah, yaitu dengan mempertimbangkan kata-kata baik yang  berada di sebelah kiri maupun kanan kata tersebut dalam suatu kalimat. Hal ini berbeda dengan  model-model sebelumnya seperti ELMo dan GPT yang hanya memproses teks dalam satu arah.

BERT dilatih melalui dua tugas utama, yaitu Masked Language Model (MLM) dan Next Sentence Prediction (NSP), menggunakan kumpulan data teks yang sangat besar. Proses pelatihan ini menghasilkan representasi kata yang kaya konteks dan dapat digunakan kembali untuk berbagai tugas NLP melalui proses fine-tuning. Menurut Devlin et al. (2019), BERT berhasil mencapai performa terbaik (state-of-the-art) pada berbagai tolok ukur NLP ketika pertama kali dirilis.

Dalam penelitian ini, arsitektur BERT digunakan sebagai dasar dari model IndoBERT yang digunakan. Pemahaman terhadap cara kerja BERT penting karena prinsip-prinsip yang sama diterapkan dalam IndoBERT, termasuk mekanisme self-attention dan proses fine-tuning untuk tugas klasifikasi sentimen.

## 2.11 IndoBERT

IndoBERT adalah model BERT yang dikembangkan khusus untuk bahasa Indonesia oleh Wilie et al. (2020) melalui proyek IndoNLU (Indonesian Natural Language Understanding). Model ini dilatih dengan menggunakan kumpulan teks berbahasa Indonesia dalam jumlah besar, sehingga mampu memahami  yang lebih baik terhadap karakteristik bahasa Indonesia dibandingkan model BERT multibahasa (mBERT). IndoBERT tersedia dalam beberapa varian ukuran, yaitu IndoBERT-base dan IndoBERT-large.

Penggunaan IndoBERT dalam analisis sentimen untuk bahasa Indonesia telah terbukti menghasilkan performa yang lebih baik dibandingkan dengan model BERT berbahasa umum. Koto et al. (2020) melaporkan bahwa IndoBERT mencapai skor yang lebih tinggi pada berbagai tugas NLP berbahasa Indonesia, termasuk klasifikasi teks dan analisis sentimen, jika dibandingkan model multilingual yang tidak dilatih secara khusus untuk bahasa Indonesia.

Dalam penelitian ini, IndoBERT digunakan sebagai model utama untuk mengklasifikasikan sentimen dari ulasan pengguna JakOne Mobile. Proses yang dilakukan meliputi fine-tuning model IndoBERT menggunakan dataset ulasan yang telah diberi label melalui InSet Lexicon, sehingga model dapat mempelajari pola sentimen yang khusus untuk konteks aplikasi perbankan digital.

## 2.12 Evaluasi Model Klasifikasi

Evaluasi model klasifikasi dilakukan untuk mengukur seberapa baik model yang telah dibuat dalam melakukan prediksi yang akurat. Terdapat beberapa metrik evaluasi yang umum digunakan dalam klasifikasi teks, yaitu accuracy, precision, recall, dan F1-score. Accuracy mengukur proporsi prediksi yang benar dari seluruh data uji. Precision mengukur tingkat ketepatan dari prediksi positif yang dihasilkan model, sedangkan recall mengukur seberapa banyak data positif yang berhasil terdeteksi (Sokolova dan Lapalme, 2022).

F1-score adalah rata-rata harmonik antara precision dan recall, sehingga memberikan gambaran yang lebih seimbang tentang performa model, terutama ketika distribusi kelas tidak merata. Dalam klasifikasi multi-kelas seperti penelitian ini yang memiliki tiga kelas sentimen, digunakan macro average, yaitu rata-rata metrik dari setiap kelas tanpa mempertimbangkan jumlah data per kelas. Selain itu, confusion matrix digunakan untuk memvisualisasikan distribusi prediksi model pada setiap kelas secara rinci.

Dalam penelitian ini, evaluasi dilakukan menggunakan accuracy, precision, recall, F1-score dengan macro average, serta confusion matrix. Penggunaan berbagai metrik ini bertujuan untuk memberikan gambaran yang menyeluruh secara komprehensif dan objektif mengenai performa kinerja model IndoBERT dalam mengklasifikasikan sentimen ulasan pengguna JakOne Mobile.

## 2.13 Penelitian Terdahulu

Penelitian terdahulu dikaji untuk memahami perkembangan studi yang relevan dengan topik penelitian ini, sekaligus untuk mengidentifikasi posisi penelitian ini di antara penelitian yang sudah ada. Berikut disajikan ringkasan beberapa penelitian terdahulu yang berkaitan dengan analisis sentimen, IndoBERT, pelabelan berbasis lexicon, dan klasifikasi ulasan aplikasi.


| No | Penulis &amp; Tahun | Tujuan | Metode | Hasil | Kelebihan | Kekurangan |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Saputra, A. R., et al. (2024)
Universitas Gunadarma | Menganalisis sentimen ulasan pengguna aplikasi mobile banking menggunakan IndoBERT | IndoBERT, InSet Lexicon (pelabelan otomatis) | Akurasi mencapai 88% pada klasifikasi tiga kelas sentimen | Menggunakan model BERT khusus bahasa Indonesia dengan pelabelan otomatis | Dataset masih terbatas dan belum mencakup variasi dialek pengguna |
| 2 | Wibirama, S., et al. (2023)
Universitas Gunadarma | Melakukan klasifikasi sentimen ulasan aplikasi pemerintah dari Google Play Store | IndoBERT fine-tuning, preprocessing teks | F1-score macro 85,4% pada dataset ulasan aplikasi pemerintah | Fokus pada aplikasi sektor publik yang relevan dengan objek penelitian ini | Tidak melakukan perbandingan dengan model lain sebagai baseline |
| 3 | Nugroho, P., et al. (2022)
Universitas Gunadarma | Membandingkan metode pelabelan lexicon dan anotasi manual untuk analisis sentimen bahasa Indonesia | InSet Lexicon, BERT, Naive Bayes | Pelabelan otomatis berbasis lexicon menghasilkan akurasi sebanding dengan anotasi manual (selisih &lt; 5%) | Memberikan alternatif pelabelan yang efisien tanpa anotasi manual | Perbandingan masih terbatas pada domain berita dan media sosial |
| 4 | Pramana, D., et al. (2025)
Universitas Indonesia | Menganalisis sentimen ulasan fintech menggunakan model BERT bahasa Indonesia | IndoBERT, fine-tuning, evaluasi multi-kelas | Akurasi 91,2% dan F1-score macro 89,7% pada dataset ulasan fintech | Dataset lebih besar dan beragam, domain fintech relevan dengan perbankan digital | Tidak menggunakan pelabelan berbasis lexicon, seluruh label diperoleh dari anotasi manual |
| 5 | Hidayah, N., et al. (2025)
Universitas Gadjah Mada | Mengklasifikasikan sentimen ulasan aplikasi e-commerce menggunakan IndoBERT dan SVM | IndoBERT, SVM, InSet Lexicon | IndoBERT menghasilkan F1-score 90,1%, lebih tinggi dibandingkan SVM (82,3%) | Melakukan perbandingan antara model deep learning dan machine learning klasik | Domain e-commerce berbeda dari domain perbankan, sehingga generalisasi mungkin terbatas |

Tabel 2.1 Ringkasan Penelitian Terdahulu

Berdasarkan tabel di atas, dapat dilihat bahwa penelitian terdahulu telah banyak menggunakan IndoBERT dan InSet Lexicon dalam analisis sentimen pada berbagai domain, termasuk mobile banking dan aplikasi pemerintah. Penelitian ini mengambil pendekatan yang serupa dengan menggunakan InSet Lexicon untuk pelabelan otomatis dan IndoBERT untuk klasifikasi sentimen, namun berfokus pada aplikasi JakOne Mobile yang merupakan layanan perbankan digital milik pemerintah daerah yang belum pernah menjadi objek penelitian serupa sebelumnya.

## 2.14 Kerangka Pemikiran

Kerangka pemikiran penelitian ini menggambarkan alur kerja secara sistematis dari tahap awal hingga tahap akhir penelitian. Tahap pertama adalah pengumpulan data, yaitu mengambil ulasan pengguna aplikasi JakOne Mobile dari Google Play Store menggunakan teknik web scraping. Data yang terkumpul kemudian melewati tahap text preprocessing yang mencakup pembersihan teks, penghapusan karakter tidak relevan, tokenisasi, dan normalisasi kata.

Setelah data bersih, dilakukan pelabelan sentimen secara otomatis menggunakan InSet Lexicon untuk menghasilkan label positif, negatif, atau netral pada setiap ulasan. Data berlabel tersebut kemudian dibagi menjadi data latih dan data uji dengan proporsi yang telah ditentukan. Selanjutnya, model IndoBERT dilatih (fine-tuning) menggunakan data latih agar dapat mempelajari pola sentimen dalam ulasan berbahasa Indonesia.

Tahap terakhir adalah evaluasi model menggunakan data uji dengan metrik accuracy, precision, recall, F1-score macro average, dan confusion matrix. Hasil evaluasi digunakan untuk mengukur seberapa baik model IndoBERT dalam mengklasifikasikan sentimen ulasan pengguna JakOne Mobile. Kerangka pemikiran ini memastikan bahwa setiap tahapan penelitian saling terhubung dan dilakukan secara sistematis.
