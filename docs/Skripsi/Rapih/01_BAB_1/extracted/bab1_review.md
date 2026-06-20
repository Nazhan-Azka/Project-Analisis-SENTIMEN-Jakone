# Ekstrak BAB 1 - BAB1_Skripsi_JakOne.docx

> Catatan: file ini adalah hasil ekstraksi teks dari DOCX asli untuk kebutuhan review. DOCX asli tidak diubah.

## 1. PENDAHULUAN

## 1.1 Latar Belakang

Perkembangan teknologi digital yang berlangsung dengan cepat telah mendorong transformasi besar dalam sektor perbankan di Indonesia. Layanan perbankan kini tidak lagi mengharuskan nasabah untuk datang langsung ke kantor cabang, melainkan dapat diakses kapan saja dan di mana saja melalui perangkat smartphone. Bank Indonesia mencatat bahwa transaksi pembayaran digital di Indonesia terus mengalami pertumbuhan signifikan, di mana pada Februari 2026 volume transaksi mencapai 4,67 miliar transaksi atau tumbuh 40,35% secara tahunan (Kontan, 2026).Angka ini mencerminkan betapa pesatnya adopsi layanan perbankan digital oleh masyarakat Indonesia dan menunjukkan bahwa mobile banking telah menjadi bagian yang tidak terpisahkan dari kehidupan keuangan sehari-hari.

Salah satu aplikasi mobile banking milik pemerintah daerah yang turut berkembang dalam ekosistem digital ini adalah JakOne Mobile, produk unggulan Bank DKI. Aplikasi ini terus menunjukkan peningkatan penggunaan seiring dengan pertumbuhan transaksi digital di Indonesia dan kebutuhan masyarakat akan layanan perbankan yang praktis. JakOne Mobile menyediakan berbagai fitur seperti pembukaan rekening secara online, deposito, transfer dana, hingga pembayaran QRIS yang mendukung ekosistem transaksi non-tunai. Keberagaman fitur tersebut menjadikan aplikasi ini sebagai salah satu kanal digital utama yang digunakan nasabah dalam melakukan aktivitas perbankan sehari-hari. Dengan demikian, JakOne Mobile memiliki peran penting dalam mendukung transformasi digital layanan perbankan, khususnya di lingkungan pemerintah daerah.

Di balik pertumbuhan pengguna yang terus meningkat, aspek keamanan menjadi perhatian yang tidak dapat diabaikan dalam layanan perbankan digital, karena semakin luasnya adopsi teknologi juga meningkatkan potensi ancaman siber yang dapat mengeksploitasi kelemahan sistem. Pada Maret 2025, layanan JakOne Mobile mengalami gangguan signifikan yang menyebabkan nasabah tidak dapat melakukan transfer antarbank maupun pembayaran melalui QRIS, terutama saat momen Idulfitri 1446 Hijriah ketika kebutuhan transaksi meningkat, sehingga berdampak langsung pada aktivitas finansial masyarakat dan menimbulkan ketidaknyamanan bagi pengguna. Pada periode yang sama, muncul dugaan peretasan pada sistem internal Bank DKI yang dimanfaatkan oleh pihak tidak bertanggung jawab untuk melakukan transaksi ilegal melalui layanan BI-Fast hingga menimbulkan kerugian dalam jumlah besar, yang sekaligus mengindikasikan adanya kelemahan dalam pengelolaan akses, sistem kontrol, serta monitoring transaksi. Rangkaian kejadian tersebut menunjukkan bahwa gangguan operasional dan ancaman keamanan dapat saling berkaitan, sehingga diperlukan evaluasi menyeluruh serta penguatan sistem keamanan, baik dari sisi teknologi maupun tata kelola, guna melindungi data nasabah dan menjaga kepercayaan masyarakat terhadap layanan perbankan digital.

Banyaknya data ulasan pengguna yang tersebar di Google Play Store dalam bentuk teks tidak terstruktur membuat analisis secara manual menjadi tidak efisien dan tidak terukur. Oleh karena itu, penelitian ini difokuskan yang menjadi perhatian utama masyarakat dan kemudahan transaksi. Untuk mengolah data tersebut digunakan metode analisis sentimen agar dapat mengetahui kecendurungan opisi positif maupun negatif. Metode Indobert dipilih karena pada berbagai penelitian sebelumnya menunjukkan kinerja yang baik dalam pengolahan teks kata berbahasa Indonesia, terutama karena mampu memahami konteks kata secara bidirectional dan telah dilatih pada korpus bahasa Indonesia dalam skala besar.

Penelitian ini hadir untuk mengisi celah tersebut dengan berfokus secara khusus pada analisis  aplikasi JakOne Mobile menggunakan metode IndoBERT. IndoBERT dipilih karena merupakan model pre-trained berbasis arsitektur BERT yang dilatih khusus menggunakan korpus bahasa Indonesia, sehingga mampu memahami konteks, nuansa, dan struktur kalimat dalam ulasan berbahasa Indonesia dengan lebih baik dibandingkan metode klasik. Dengan menerapkan IndoBERT secara khusus pada ulasan JakOne Mobile, penelitian ini diharapkan mampu memberikan informasi bermanfaat berbasis data yang bermanfaat bagi Bank DKI sebagai bahan evaluasi dan pertimbangan strategis dalam meningkatkan kepercayaan dan kualitas layanan digital .

Berdasarkan uraian di atas, rumusan masalah dalam penelitian ini adalah bagaimana metode IndoBERT dapat digunakan untuk mengklasifikasikan sentimen ulasan pengguna serta bagaimana distribusi sentimen positif, negatif, dan netral dari ulasan tersebut.

## 1.2 Ruang Lingkup

Agar penelitian ini lebih terarah dan terukur, terdapat beberapa batasan yang ditetapkan dalam pelaksanaannya. Batasan-batasan tersebut meliputi aspek sumber data, bahasa, waktu pengambilan data, topik ulasan yang dianalisis, serta jumlah data yang digunakan. Penetapan ruang lingkup ini bertujuan untuk mempertajam fokus penelitian sehingga hasil yang diperoleh dapat menjawab permasalahan yang telah dirumuskan secara tepat dan tidak melebar ke aspek di luar pembahasan.

Adapun ruang lingkup penelitian ini adalah sebagai berikut:

Data ulasan yang digunakan bersumber dari platform Google Play Store pada aplikasi JakOne Mobile milik Bank DKI Jakarta.

Ulasan yang dianalisis hanya ulasan yang ditulis dalam bahasa Indonesia, sehingga ulasan dalam bahasa lain tidak diikutsertakan dalam proses analisis.

Periode pengambilan data ulasan dibatasi dari tahun 2022 hingga 2026, dengan total data awal sebanyak 14.000 ulasan.

Metode yang digunakan dalam penelitian ini adalah IndoBERT untuk proses klasifikasi sentimen, dengan kategori label positif, negatif, dan netral.

## 1.3 Tujuan Penelitian

Penelitian ini dilakukan dengan beberapa tujuan yang mengacu pada rumusan masalah yang telah dipaparkan sebelumnya. Tujuan-tujuan tersebut disusun secara sistematis agar setiap proses penelitian dapat diukur ketercapaiannya dan menghasilkan kontribusi yang bermakna, baik secara akademis maupun praktis bagi pengembangan aplikasi JakOne Mobile.

Adapun tujuan dari penelitian ini adalah sebagai berikut:

Mengklasifikasikan sentimen ulasan pengguna aplikasi JakOne Mobile di Google Play Store ke dalam kategori positif, negatif, dan netral menggunakan metode IndoBERT.

Mengevaluasi performa model IndoBERT dalam mengklasifikasikan sentimen ulasan berbahasa Indonesia pada domain aplikasi mobile banking berdasarkan metrik akurasi, precision, recall, dan F1-score.

Menganalisis distribusi sentimen pengguna terkait aplikasi JakOne Mobile guna memberikan gambaran menyeluruh mengenai persepsi nasabah terhadap fitur dan sistem yang tersedia.

Memberikan rekomendasi berbasis data kepada pihak Bank DKI sebagai bahan evaluasi dan pengembangan fitur pada aplikasi JakOne Mobile ke depannya.

## 1.4 Sistematika Penulisan

Sistematika penulisan dalam penelitian ini terdiri dari lima bab yang disusun secara berurutan dan saling berkesinambungan. Bab 1 merupakan Pendahuluan yang memuat latar belakang permasalahan, ruang lingkup penelitian, tujuan penelitian, serta sistematika penulisan. Pada bagian ini dijelaskan alasan pemilihan topik, batasan penelitian, serta gambaran umum mengenai apa yang ingin dicapai dalam penelitian ini.

## Bab 2 merupakan Tinjauan Pustaka yang memaparkan landasan teori dan penelitian terdahulu yang mendukung penelitian ini. Teori-teori yang dibahas mencakup konsep analisis sentimen, natural language processing (NLP), model IndoBERT, serta ulasan mengenai aplikasi mobile banking. Selain itu, dipaparkan pula perbandingan penelitian sejenis yang telah dilakukan sebelumnya sebagai dasar untuk menunjukkan kebaruan penelitian ini.

## Bab 3 merupakan Metode Penelitian yang menjelaskan tahapan dan alur penelitian secara rinci. Bagian ini mencakup uraian mengenai sumber dan teknik pengumpulan data ulasan dari Google Play Store, proses preprocessing teks, tahap pelabelan data, arsitektur model IndoBERT yang digunakan, serta metode evaluasi yang diterapkan untuk mengukur performa model klasifikasi sentimen.

## Bab 4 merupakan Hasil dan Pembahasan yang menyajikan temuan dari penelitian secara menyeluruh. Pada bab ini dipaparkan hasil klasifikasi sentimen ulasan pengguna JakOne Mobile, distribusi sentimen yang diperoleh, serta evaluasi performa model IndoBERT berdasarkan metrik yang telah ditetapkan. Selain itu, dibahas pula implikasi dari hasil penelitian terhadap pengembangan layanan aplikasi.

## Bab 5 merupakan Penutup yang berisi simpulan dari seluruh hasil penelitian yang telah dilakukan serta saran yang ditujukan bagi pihak Bank DKI maupun bagi penelitian selanjutnya. Simpulan disusun berdasarkan jawaban atas tujuan penelitian yang telah ditetapkan pada Bab 1, sedangkan saran diberikan sebagai masukan konstruktif untuk pengembangan lebih lanjut di masa mendatang.
