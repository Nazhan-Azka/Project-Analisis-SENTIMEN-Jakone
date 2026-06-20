# Audit Labeling Lexicon JakOne Mobile

Audit ini dibuat otomatis dari dataset final, lexicon positif/negatif, dan aturan labeling berbasis skor. Dataset asli, lexicon asli, model, dan dashboard tidak diubah.

## Ringkasan Eksekutif
- Total data diaudit: 14.172
- Distribusi label saat ini: positif=7.475. negatif=5.558. netral=1.139
- Total kandidat label bermasalah: 2.629
- Kandidat high-confidence: 654
- Kandidat medium-confidence: 1.975
- Label netral dengan skor 0: 1.139
- Netral skor 0 yang terindikasi positif: 303
- Netral skor 0 yang terindikasi negatif: 88
- Kasus konflik skor tinggi dengan final mendekati 0: 1.905

## Kategori Masalah Terbesar
- positive_pattern: 859 kandidat
- negative_pattern: 780 kandidat
- negation_pattern: 547 kandidat
- neutral_zero: 293 kandidat
- conflict_score: 150 kandidat

## Kata Umum Lexicon Yang Paling Perlu Ditinjau
- `aplikasi`: pos=nan, neg=-4.0, freq_doc=6002, rekomendasi=kandidat netralisasi
- `transaksi`: pos=4.0, neg=nan, freq_doc=1747, rekomendasi=kandidat netralisasi
- `saldo`: pos=2.0, neg=nan, freq_doc=459, rekomendasi=kandidat netralisasi
- `pengguna`: pos=1.0, neg=nan, freq_doc=188, rekomendasi=kandidat netralisasi
- `sistem`: pos=nan, neg=-4.0, freq_doc=158, rekomendasi=kandidat netralisasi
- `layanan`: pos=3.0, neg=nan, freq_doc=149, rekomendasi=kandidat netralisasi
- `jakone`: pos=nan, neg=nan, freq_doc=2151, rekomendasi=aman
- `bank`: pos=nan, neg=nan, freq_doc=1968, rekomendasi=aman
- `mobile`: pos=nan, neg=nan, freq_doc=1432, rekomendasi=aman
- `fitur`: pos=nan, neg=nan, freq_doc=1196, rekomendasi=aman
- `update`: pos=nan, neg=nan, freq_doc=526, rekomendasi=aman
- `login`: pos=nan, neg=nan, freq_doc=520, rekomendasi=aman

## Frasa Positif Dengan Salah Label Terbanyak
- `bagus`: total=2018, suspect_non_positive=580, positif=1438, negatif=490, netral=90
- `keren`: total=1103, suspect_non_positive=270, positif=833, negatif=162, netral=108
- `aplikasi mudah`: total=571, suspect_non_positive=102, positif=469, negatif=74, netral=28
- `sangat membantu`: total=722, suspect_non_positive=93, positif=629, negatif=41, netral=52
- `lancar`: total=367, suspect_non_positive=86, positif=281, negatif=77, netral=9
- `mantap`: total=783, suspect_non_positive=78, positif=705, negatif=38, netral=40
- `cepat`: total=797, suspect_non_positive=77, positif=720, negatif=64, netral=13
- `memudahkan`: total=553, suspect_non_positive=75, positif=478, negatif=63, netral=12
- `mudah digunakan`: total=582, suspect_non_positive=68, positif=514, negatif=49, netral=19
- `berguna`: total=199, suspect_non_positive=49, positif=150, negatif=45, netral=4

## Frasa Negatif Dengan Salah Label Terbanyak
- `ribet`: total=789, suspect_non_negative=487, positif=450, negatif=302, netral=37
- `lambat`: total=449, suspect_non_negative=214, positif=196, negatif=235, netral=18
- `lemot`: total=439, suspect_non_negative=210, positif=192, negatif=229, netral=18
- `error`: total=643, suspect_non_negative=109, positif=91, negatif=534, netral=18
- `eror`: total=308, suspect_non_negative=53, positif=41, negatif=255, netral=12
- `parah`: total=360, suspect_non_negative=50, positif=37, negatif=310, netral=13
- `payah`: total=169, suspect_non_negative=48, positif=34, negatif=121, netral=14
- `kecewa`: total=110, suspect_non_negative=33, positif=30, negatif=77, netral=3
- `buruk`: total=188, suspect_non_negative=23, positif=16, negatif=165, netral=7
- `transaksi gagal`: total=34, suspect_non_negative=19, positif=16, negatif=15, netral=3

## Pasangan Kata Yang Sering Saling Meniadakan Pada Skor 0
- positif `mudah` vs negatif `aplikasi`: 93 kasus
- positif `banget` vs negatif `aplikasi`: 91 kasus
- positif `bagus` vs negatif `aplikasi`: 83 kasus
- positif `membantu` vs negatif `aplikasi`: 58 kasus
- positif `transaksi` vs negatif `aplikasi`: 58 kasus
- positif `lengkap` vs negatif `aplikasi`: 33 kasus
- positif `banget` vs negatif `tidak`: 32 kasus
- positif `lebih` vs negatif `aplikasi`: 32 kasus
- positif `bayar` vs negatif `aplikasi`: 30 kasus
- positif `tampilan` vs negatif `aplikasi`: 26 kasus

## Contoh 10 Kandidat Paling Jelas
1. current=positif, suggested=negatif, confidence=high, pattern=tidak bisa login
   - clean_review: kok tidak bisa login ya aktivasi
   - reason: negative_pattern: label conflicts with clear negative phrase
2. current=positif, suggested=negatif, confidence=high, pattern=tidak bisa login
   - clean_review: sebwlumnya pakai apl iphone iphone rusak pindah android kenapa tidak bisa login ya min udah klik ya punya rekening disuruh bikin rek balik balik
   - reason: negative_pattern: label conflicts with clear negative phrase
3. current=positif, suggested=negatif, confidence=high, pattern=tidak bisa login
   - clean_review: tidak bisa login gmna aneh bngt ya
   - reason: negative_pattern: label conflicts with clear negative phrase
4. current=positif, suggested=negatif, confidence=high, pattern=tidak bisa login
   - clean_review: knp hanlbis diperbarui tidak bisa login ya alasannya jaringan internet padahal pakai wifi jaringanpun stabil
   - reason: negative_pattern: label conflicts with clear negative phrase
5. current=positif, suggested=negatif, confidence=high, pattern=tidak bisa login
   - clean_review: ganti nomor telpon udah bank dki verifikasi mengganti nomor telpon jakone tidak bisa login aktivasi ulang hadehhh aneh
   - reason: negative_pattern: label conflicts with clear negative phrase
6. current=positif, suggested=negatif, confidence=high, pattern=tidak bisa login
   - clean_review: mohon diperbaiki sistemnya kenapa tidak bisa login tiba tiba bahkan setelah chat cs solusinya kantor cabang
   - reason: negative_pattern: label conflicts with clear negative phrase
7. current=positif, suggested=negatif, confidence=high, pattern=tidak bisa login
   - clean_review: tidak bisa login diarahkan pembukaan rekening mulu padahal udah klik ya pas pertanyaan apakah memiliki rekening
   - reason: negative_pattern: label conflicts with clear negative phrase
8. current=positif, suggested=negatif, confidence=high, pattern=tidak bisa login
   - clean_review: knp pas update kok tidak bisa login sampaikan mendownload play store aneh
   - reason: negative_pattern: label conflicts with clear negative phrase
9. current=positif, suggested=negatif, confidence=high, pattern=tidak bisa login
   - clean_review: minta tolong kenapa tidak bisa login setelah ganti hp padahal nomor telepon unseur name benr sandi nomer tlpon bntr verivikasi dapet usser kode ribett bagt si ya allah
   - reason: negative_pattern: label conflicts with clear negative phrase
10. current=netral, suggested=negatif, confidence=high, pattern=tidak bisa login
   - clean_review: setelah notif transaksi bisa digunakan setelah lampu aplikasi berwarna hijau hiih abis maintenance tidak bisa login alhasil akun terkunci hadeuh
   - reason: negative_pattern: label conflicts with clear negative phrase

## Rekomendasi Refinement
- Aman dikoreksi otomatis: kandidat `high` dengan pola positif/negatif sangat eksplisit dan tanpa sinyal campuran kuat. Tetap simpan audit trail.
- Perlu validasi manual: kandidat `medium`, konflik skor, dan pola dengan konteks campuran seperti keluhan yang juga mengandung kata positif.
- Sebaiknya tidak diubah otomatis: kandidat ambigu, review sangat pendek tanpa konteks, dan review dengan sentimen campuran.
- Revisi lexicon: netralisasi atau turunkan bobot kata domain umum seperti `aplikasi`, `bank`, `transaksi`, `saldo`, `akun`, `login`, `otp`, `sistem`, `update`, dan `fitur` jika terbukti memberi kontribusi sentimen yang tidak stabil.
- Rule negasi: aturan negasi token langsung sudah ada, tetapi perlu diperluas untuk frasa domain seperti `tidak bisa login`, `otp tidak masuk`, `saldo tidak masuk`, `transaksi gagal`, dan variasi slang.
- Phrase-level rules: tambahkan prioritas frasa sebelum skor token tunggal, misalnya `mudah digunakan` positif dan `tidak bisa login` negatif, agar kata umum tidak meniadakan frasa yang jelas.
- Dataset refined layak dibuat untuk eksperimen training ulang setelah kandidat high-confidence diaudit cepat dan kandidat medium divalidasi manual.

## File Output
- `data/audit/lexicon_common_terms_audit.csv`
- `data/audit/positive_pattern_audit.csv`
- `data/audit/negative_pattern_audit.csv`
- `data/audit/negation_audit.csv`
- `data/audit/neutral_score_zero_audit.csv`
- `data/audit/conflict_score_audit.csv`
- `data/audit/label_refinement_candidates.csv`
- `data/audit/audit_summary.md`