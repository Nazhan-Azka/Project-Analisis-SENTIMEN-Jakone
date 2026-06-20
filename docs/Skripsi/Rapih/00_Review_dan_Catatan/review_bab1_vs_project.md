# Review BAB 1 vs Kondisi Project

## Ringkasan Kesesuaian

BAB 1 sudah cukup sesuai pada tingkat umum karena membahas mobile banking, JakOne Mobile, pentingnya keamanan, ulasan pengguna, analisis sentimen, dan penggunaan IndoBERT. Namun, BAB 1 belum sepenuhnya selaras dengan kondisi project saat ini karena fokus aspek keamanan belum dinyatakan secara eksplisit dan pipeline penelitian yang sudah dikerjakan belum tercermin lengkap.

Bagian yang paling perlu diperkuat adalah penegasan bahwa penelitian tidak menganalisis seluruh fitur JakOne Mobile secara umum, tetapi berfokus pada ulasan yang terkait aspek keamanan dan akses layanan, seperti OTP, login, akun, verifikasi, transaksi, password, error keamanan, kendala akses, dan transaksi.

## Sumber Project yang Dibandingkan

- `README.md`
- `docs/colab_indobert_v3.md`
- `data/audit/refinement_highconf_summary.md`
- `outputs/evaluation/test_metrics_summary.json`
- `outputs/evaluation/test_classification_report.csv`
- `outputs/evaluation/test_confusion_matrix.csv`
- `outputs/evaluation/indobert_v3_baseline/test_metrics.json`
- `outputs/evaluation/indobert_v3_baseline/classification_report.csv`
- `outputs/evaluation/indobert_v3_baseline/confusion_matrix.csv`
- `outputs/modeling/indobert_v3_baseline/training_config.json`
- `outputs/modeling/indobert_v3_baseline/training_log.json`
- `dashboard/app.py`

Catatan: file yang diminta dengan nama `outputs/evaluation/test_metrics.json`, `outputs/evaluation/classification_report.csv`, dan `outputs/evaluation/confusion_matrix.csv` tidak ditemukan di path root tersebut. File yang tersedia adalah `test_metrics_summary.json`, `test_classification_report.csv`, `test_confusion_matrix.csv`, serta versi v3 baseline di folder `outputs/evaluation/indobert_v3_baseline/`.

## Latar Belakang

Status: sudah sesuai sebagian, tetapi perlu revisi.

Kesesuaian:
- BAB 1 sudah menjelaskan pertumbuhan mobile banking dan relevansi JakOne Mobile.
- BAB 1 sudah menyinggung aspek keamanan dan gangguan layanan sebagai alasan penelitian.
- BAB 1 sudah menyebut ulasan Google Play Store sebagai data teks tidak terstruktur.
- BAB 1 sudah menyebut IndoBERT sebagai metode yang relevan untuk teks Bahasa Indonesia.

Perlu diperbaiki:
- Fokus aspek keamanan masih belum tegas. BAB 1 masih terbaca sebagai analisis sentimen aplikasi JakOne Mobile secara umum.
- Ada kalimat yang kurang lengkap: "penelitian ini difokuskan yang menjadi perhatian utama masyarakat dan kemudahan transaksi."
- Ada typo: "kecendurungan opisi" seharusnya "kecenderungan opini".
- Ada repetisi alasan memilih IndoBERT pada dua paragraf berurutan.
- Perlu ditambahkan konteks bahwa project sudah memakai ulasan terkait isu keamanan/akses/transaksi, bukan hanya ulasan umum.

## Rumusan Masalah

Status: belum lengkap.

Rumusan masalah saat ini hanya menyebut:
- bagaimana IndoBERT mengklasifikasikan sentimen ulasan pengguna;
- bagaimana distribusi sentimen positif, negatif, dan netral.

Perlu ditambahkan:
- rumusan masalah tentang aspek keamanan pada ulasan JakOne Mobile;
- rumusan masalah tentang performa model IndoBERT berdasarkan metrik evaluasi;
- rumusan masalah tentang kendala class imbalance, terutama kelas netral.

Contoh rumusan masalah tambahan:
- Bagaimana distribusi sentimen pengguna terhadap aspek keamanan aplikasi JakOne Mobile berdasarkan ulasan Google Play Store?
- Bagaimana performa model IndoBERT dalam mengklasifikasikan sentimen positif, negatif, dan netral pada ulasan pengguna JakOne Mobile?
- Apa saja isu keamanan atau akses layanan yang dominan muncul pada ulasan pengguna JakOne Mobile?

## Batasan / Ruang Lingkup

Status: sudah ada, tetapi belum cukup sesuai dengan project.

Yang sudah sesuai:
- sumber data dari Google Play Store;
- bahasa ulasan adalah Bahasa Indonesia;
- periode data 2022 sampai 2026;
- metode klasifikasi menggunakan IndoBERT;
- label sentimen positif, negatif, dan netral.

Yang perlu ditambahkan:
- dataset final aktif menggunakan kolom `review`, `label`, dan `split_set`;
- fokus penelitian pada aspek keamanan, akses, dan transaksi;
- pelabelan awal dilakukan menggunakan lexicon;
- label sudah melalui validasi/perbaikan;
- data dibagi menjadi train, validation, dan test;
- baseline menggunakan `indobenchmark/indobert-base-p1`;
- penelitian tidak membahas audit keamanan teknis sistem Bank DKI, penetrasi sistem, forensik digital, atau analisis log internal.

## Tujuan Penelitian

Status: sudah cukup sesuai, tetapi perlu diarahkan ke aspek keamanan.

Yang sudah sesuai:
- mengklasifikasikan sentimen menjadi positif, negatif, dan netral;
- mengevaluasi performa model dengan accuracy, precision, recall, dan F1-score;
- menganalisis distribusi sentimen;
- memberi rekomendasi berbasis data.

Yang perlu ditambahkan:
- tujuan eksplisit untuk mengidentifikasi isu dominan terkait keamanan, login, OTP, verifikasi, akun, password, akses, error keamanan, dan transaksi;
- tujuan untuk menjelaskan keterbatasan model pada kelas minoritas/netral.

## Manfaat Penelitian

Status: belum terlihat sebagai subbab khusus di hasil ekstraksi BAB 1.

BAB 1 saat ini memiliki subbab Latar Belakang, Ruang Lingkup, Tujuan Penelitian, dan Sistematika Penulisan. Subbab Manfaat Penelitian belum muncul, padahal diminta dalam struktur review dan lazim ada pada BAB 1.

Manfaat yang perlu ditambahkan:
- manfaat akademis: referensi penerapan IndoBERT untuk analisis sentimen ulasan mobile banking berbahasa Indonesia;
- manfaat praktis: masukan bagi Bank DKI untuk memahami isu keamanan dan akses yang sering dikeluhkan pengguna;
- manfaat metodologis: contoh pipeline mulai dari preprocessing, lexicon labeling, validasi label, fine-tuning IndoBERT, evaluasi, sampai visualisasi dashboard.

## Hal Project yang Sudah Dikerjakan tetapi Belum Tertulis di BAB 1

- Preprocessing teks Bahasa Indonesia sudah dilakukan.
- Pelabelan awal menggunakan lexicon sudah dilakukan.
- Validasi/perbaikan label sudah dilakukan.
- Refinement high-confidence pernah dibuat dengan 692 perubahan label, tetapi catatan audit menyarankan tetap hati-hati karena beberapa perubahan dapat terpengaruh pola negasi seperti "tidak berguna".
- Split dataset train/validation/test sudah dilakukan.
- Dataset final aktif untuk v3 memakai `data/final/06_jakone_modeling_master_v3.csv`.
- Kolom aktif untuk modeling adalah `review`, `label`, dan `split_set`.
- Fine-tuning IndoBERT sudah dilakukan.
- Baseline v3 memakai `indobenchmark/indobert-base-p1`.
- Konfigurasi baseline v3: 2 epoch, batch size 8, learning rate 2e-5, max length 128, seed 42, tanpa class weight.
- Distribusi train pada konfigurasi v3: negatif 3.684, netral 917, positif 6.736.
- Distribusi validation pada konfigurasi v3: negatif 460, netral 115, positif 842.
- Evaluasi tersedia dalam dua set output: output lama di root `outputs/evaluation/` dan output v3 baseline di `outputs/evaluation/indobert_v3_baseline/`.
- Output v3 baseline yang terbaca menunjukkan test accuracy 0,9316 dan macro F1 0,8774.
- Output root lama menunjukkan test accuracy 0,8949 dan macro F1 0,8192.
- Konteks dari pengguna menyebut hasil baseline sekitar accuracy 0,9457 dan macro F1 0,6313; angka ini belum ditemukan pada file yang dibaca, sehingga perlu dipastikan sumber output finalnya sebelum dimasukkan ke BAB 1.
- Dashboard Streamlit sudah dibuat dengan halaman Overview, Dataset, Labeling, Training IndoBERT, Evaluasi Model, Analisis Kesalahan, Keyword Issue & Word Cloud, dan Demo Prediksi.
- Dashboard membaca dataset, model, training log, metrics, classification report, confusion matrix, predictions, keyword issue, word cloud, dan model untuk demo prediksi.

## Bagian BAB 1 yang Perlu Ditambahkan

1. Subbab Manfaat Penelitian.
2. Penegasan fokus aspek keamanan pada Latar Belakang.
3. Rumusan masalah yang eksplisit menyebut aspek keamanan dan performa model.
4. Batasan masalah tentang data, label, split, model baseline, dan ruang lingkup non-teknis keamanan.
5. Penjelasan singkat bahwa penelitian menggunakan pipeline lexicon labeling, validasi label, fine-tuning IndoBERT, evaluasi, dan dashboard visualisasi.
6. Keterbatasan awal bahwa kelas netral lebih sulit dikenali karena jumlah data lebih sedikit dan sifat kalimat netral lebih ambigu.

## Saran Kalimat Tambahan Siap Tempel

### Tambahan untuk Latar Belakang

Penelitian ini secara khusus berfokus pada ulasan pengguna JakOne Mobile yang berkaitan dengan aspek keamanan dan akses layanan, seperti OTP, login, akun, verifikasi, transaksi, password, error keamanan, kendala akses, serta transaksi digital. Fokus ini dipilih karena aspek keamanan dalam mobile banking berhubungan langsung dengan kepercayaan pengguna, kelancaran transaksi, dan persepsi nasabah terhadap kualitas layanan digital perbankan.

Selain menganalisis kecenderungan sentimen secara umum, penelitian ini juga memperhatikan isu-isu dominan yang muncul dalam ulasan pengguna. Dengan demikian, hasil penelitian tidak hanya menunjukkan apakah ulasan bersentimen positif, negatif, atau netral, tetapi juga dapat memberikan gambaran mengenai jenis permasalahan yang paling sering dibahas oleh pengguna terkait keamanan dan akses aplikasi JakOne Mobile.

### Tambahan untuk Rumusan Masalah

Berdasarkan latar belakang tersebut, rumusan masalah dalam penelitian ini adalah:

1. Bagaimana distribusi sentimen pengguna terhadap aspek keamanan aplikasi JakOne Mobile berdasarkan ulasan Google Play Store?
2. Bagaimana performa model IndoBERT dalam mengklasifikasikan ulasan pengguna JakOne Mobile ke dalam sentimen positif, negatif, dan netral?
3. Isu keamanan dan akses layanan apa saja yang dominan muncul dalam ulasan pengguna JakOne Mobile?

### Tambahan untuk Batasan Masalah

Penelitian ini dibatasi pada analisis sentimen ulasan pengguna aplikasi JakOne Mobile yang diperoleh dari Google Play Store dan ditulis dalam Bahasa Indonesia. Fokus analisis diarahkan pada ulasan yang berkaitan dengan aspek keamanan dan akses layanan, seperti OTP, login, akun, verifikasi, transaksi, password, error keamanan, dan kendala akses. Penelitian ini tidak melakukan audit keamanan sistem, pengujian penetrasi, analisis log internal, maupun investigasi teknis terhadap infrastruktur Bank DKI.

Dataset yang digunakan dalam proses pemodelan memuat kolom utama `review`, `label`, dan `split_set`. Label sentimen terdiri dari tiga kelas, yaitu positif, negatif, dan netral. Pelabelan awal dilakukan dengan pendekatan lexicon, kemudian dilakukan validasi dan perbaikan label sebelum dataset digunakan untuk fine-tuning model IndoBERT.

### Tambahan untuk Tujuan Penelitian

Mengidentifikasi isu dominan yang muncul dalam ulasan pengguna terkait aspek keamanan dan akses layanan aplikasi JakOne Mobile, seperti OTP, login, akun, verifikasi, transaksi, password, error keamanan, dan kendala akses.

Menganalisis keterbatasan hasil klasifikasi, khususnya pada kelas netral yang memiliki jumlah data lebih sedikit dan karakteristik ulasan yang lebih ambigu dibandingkan kelas positif dan negatif.

### Draft Subbab Manfaat Penelitian

Manfaat penelitian ini terdiri dari manfaat akademis dan manfaat praktis. Secara akademis, penelitian ini diharapkan dapat menjadi referensi penerapan model IndoBERT dalam analisis sentimen ulasan aplikasi mobile banking berbahasa Indonesia, khususnya pada konteks keamanan dan akses layanan digital.

Secara praktis, hasil penelitian ini diharapkan dapat memberikan masukan bagi Bank DKI dalam memahami persepsi pengguna terhadap aplikasi JakOne Mobile. Informasi mengenai distribusi sentimen, isu keamanan yang dominan, serta pola keluhan pengguna dapat digunakan sebagai bahan pertimbangan dalam evaluasi dan pengembangan layanan digital.

Selain itu, penelitian ini juga menghasilkan dashboard visualisasi yang dapat membantu penyajian hasil analisis secara lebih informatif, mencakup distribusi dataset, hasil training, evaluasi model, analisis keyword issue, word cloud, dan demo prediksi sentimen.

## Catatan Konsistensi yang Perlu Dipastikan

- Judul di konteks pengguna adalah "Analisis sentimen ulasan pengguna aplikasi JakOne Mobile terkait aspek keamanan menggunakan IndoBERT"; BAB 1 perlu mengikuti fokus ini.
- README masih memuat beberapa informasi lama, misalnya model `indobert-base-p2` dan dataset `jakone_modeling_master.csv`, sedangkan konfigurasi v3 memakai `indobenchmark/indobert-base-p1` dan `data/final/06_jakone_modeling_master_v3.csv`.
- File evaluasi v3 baseline yang tersedia menunjukkan accuracy 0,9316 dan macro F1 0,8774. Angka accuracy 0,9457 dan macro F1 0,6313 dari konteks pengguna belum ditemukan pada file yang dibaca.
- Jika angka 0,9457 dan 0,6313 adalah hasil final yang akan dipakai di skripsi, perlu ditunjukkan file sumbernya atau disimpan sebagai output final agar BAB 1, BAB 4, README, dan dashboard konsisten.

