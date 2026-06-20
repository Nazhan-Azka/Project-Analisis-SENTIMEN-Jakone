# Refinement High-Confidence Summary

- Master input: `data/final/jakone_modeling_master.csv`
- Candidate input: `data/audit/label_refinement_candidates.csv`
- Refined output: `data/final/06_jakone_modeling_refined_highconf.csv`
- Changes output: `data/audit/refinement_highconf_changes.csv`
- Total rows: 14,172
- High-confidence candidate rows: 654
- Unique high-confidence match keys: 654
- Master rows matched by high-confidence keys: 692
- Label changes applied: 692

## Transition Counts
- positif_ke_negatif: 44
- positif_ke_netral: 0
- netral_ke_positif: 262
- netral_ke_negatif: 90
- negatif_ke_positif: 296
- negatif_ke_netral: 0

## Label Distribution Before
- positif: 7,475
- negatif: 5,558
- netral: 1,139

## Label Distribution After
- positif: 7,989
- negatif: 5,396
- netral: 787

## Validation
- row_count_unchanged: PASS
- no_invalid_labels: PASS
- split_set_unchanged: PASS
- review_unchanged: PASS
- only_high_confidence_changed: PASS
- unchanged_source_original: PASS
- changed_source_refinement: PASS

## Notes
- Koreksi otomatis hanya memakai kandidat `confidence_level = high`. Kandidat medium tidak dipakai.
- Karena kandidat audit tidak memiliki `review_id`, pencocokan dilakukan dengan key exact-match dari kolom yang tersedia: `review`, `clean_review`, `label`, `lexicon_score`.
- Beberapa key kandidat high-confidence cocok ke baris duplikat identik di master; baris duplikat tersebut diberi koreksi yang sama.

## 20 Clear Change Examples
| row_index | review_id | review | clean_review | lexicon_score | label_original | label | evidence_pattern | refinement_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8510 | 097fddbf-419c-442a-afb3-57a49d1e092b | Aplikasi bobrok, yang bikin tolol.. verifikasi wajah gagal terus, bobrok aplikasi tidak berguna, bagusan yang lama !!!!!!!! Buang buang pulsa doang buat kode otp.. tolol.. !!! | aplikasi bobrok bikin tolol verifikasi wajah gagal bobrok aplikasi tidak berguna bagusan buang buang pulsa doang kode otp tolol | -51.0 | negatif | positif | berguna | positive_pattern: label conflicts with clear positive phrase |
| 9394 | 75705bc1-8407-4300-9b2f-8e7174e70a81 | 1. Sering down gabisa diakses terutama di tanggal periode penggajian 2. Mutasi rekening tidak menampilkan informasi detail tujuan transfer keluar ke siapa, jadi kalau bukti transfer lupa di download atau di SS jadi gabisa tracking riwayat mutasi terutama jika mau komplain refund 3. e- ekening koran baru ada saat sudah 1 bulan full berlalu, kalau ada kendala transaksi di awal/tengah bulan dan butuh rekening koran jadi harus ke bank (mau tidak mau), dan ini membuat e-rekening korang tidak berguna. | 1 down tidak bisa diakses terutama tanggal periode penggajian 2 mutasi rekening tidak menampilkan informasi detail tujuan transfer keluar bukti transfer lupa download ss tidak bisa tracking riwayat mutasi terutama komplain refund 3 e ekening koran 1 bulan full berlalu kendala transaksi bulan butuh rekening koran bank tidak membuat e rekening korang tidak berguna | -39.0 | negatif | positif | berguna | positive_pattern: label conflicts with clear positive phrase |
| 9477 | 4ec7c71e-9872-4344-a18c-3c3aa9ea62f6 | 1) Tak bisa transfer antar bank yg berbeda, padahal lagi diperlukan banget untuk Idul Fitri. 2) Tak lagi tersedia gopay, padahal dulu ada, bagaimana caranya mau berkeliling Idul Fitri dgn ojek online? 3) Percuma ada fitur mutasi tapi mutasi masuk/keluar nggak ke detect. 4) Percuma nelpon CS kalo ada masalah, karena selain tekor pulsa, masalahpun tak selesai. 5) Qris tak berguna, tak bisa untuk pembelian. Aplikasi sering eror. Sampah. IT ganti aje. ATM DKI pun jauh dari rumah | 1 tak bisa transfer antar bank berbeda padahal diperlukan banget idul fitri 2 tak tersedia gopay padahal caranya berkeliling idul fitri ojek online 3 percuma fitur mutasi mutasi masuk keluar tidak detect 4 percuma nelpon cs masalah tekor pulsa masalahpun tak selesai 5 qris tak berguna tak bisa pembelian aplikasi error sampah it ganti aje atm dki jauh rumah | -35.0 | negatif | positif | berguna | positive_pattern: label conflicts with clear positive phrase |
| 10495 | 84ce8c98-6104-446f-ae02-dcbde682c742 | aplikasi ga berguna masa ga bisa transper k bank lain mana sedang d butuh kan hari raya ...buat apa aplikasi ini ga bisa d pergunakan | aplikasi tidak berguna masa tidak bisa transper k bank d butuh hari raya aplikasi tidak bisa d pergunakan | -33.0 | negatif | positif | berguna | positive_pattern: label conflicts with clear positive phrase |
| 821 | 25b1fc65-f018-4377-ab56-2f2247a13384 | apk makin kesini jadi ga jelas transfer ke bank lain ga bisa uang elektroniknya jg ga ada gopay dan dana atau ovo koq jadi bikin customer ga nyaman pakai jakone tolong dong kembalikan apk jakone seperti dulu makin kesini bukan memudahkan malah tambah susah | aplikasi kesini tidak jelas transfer bank tidak bisa uang elektroniknya jg tidak gopay dana ovo koq bikin customer tidak nyaman pakai jakone tolong kembalikan aplikasi jakone kesini bukan memudahkan tambah susah | -32.0 | negatif | positif | nyaman | positive_pattern: label conflicts with clear positive phrase |
| 4976 | e801cd57-6161-4bff-ba60-aaf76adbfedf | Baru download, baru mau daftar, setiap mau daftar gak bisa bisa. Tertulis "Kami tidak dapat memproses permintaan anda, silakan coba kembali (911) Kenapa? 😔 ini aplikasi udah banyak yang memberi rate satu dan memberi keluhan, tapi sepertinya keluhan para pengguna tidak didengarkan, apakah aplikasi ini memang tidak berguna? 😔 | download daftar setiap daftar tidak bisa bisa tertulis tidak memproses permintaan silakan coba 911 kenapa aplikasi udah memberi rate memberi keluhan sepertinya keluhan pengguna tidak didengarkan apakah aplikasi tidak berguna | -31.0 | negatif | positif | berguna | positive_pattern: label conflicts with clear positive phrase |
| 689 | 1a7c23cd-3620-4486-b8f7-4edce7cc40d9 | Banyak masalah, transfer sesama pengguna via qris gak bisa, tiap waktu ada aja hambatan buat transfer, sebagai user aplikasi ini gak nyaman Terpaksa pake aplikasinya | masalah transfer sesama pengguna via qris tidak bisa hambatan transfer user aplikasi tidak nyaman terpaksa pakai aplikasi | -29.0 | negatif | positif | nyaman | positive_pattern: label conflicts with clear positive phrase |
| 9429 | 0c10f4bf-d1cf-4ea7-b1fa-8a25cee78a44 | mbanking tak berguna klau bukan karena hibah g gue pakai ini. dikeadaan begini butuh uang login pun tak bisa. tolong dibenahi . 2 Minggu saya login g bisa2 juga. dimana tanggung jawabnya ini.???????????? | mbanking tak berguna klau bukan hibah tidak gue pakai dikeadaan butuh uang login tak bisa tolong dibenahi 2 minggu login tidak bisa2 dimana tanggung jawabnya | -26.0 | negatif | positif | berguna | positive_pattern: label conflicts with clear positive phrase |
| 13275 | 4f62105e-3f06-4727-ac7e-0a1fc7e2db16 | mobile banking paling ga berguna, tf antar bank gabisa, top up ewallet gabisa, tarik cardless gabisa, semuanya serba gabisa, hadehh | mobile banking tidak berguna transfer antar bank tidak bisa top up ewallet tidak bisa tarik cardless tidak bisa semuanya serba tidak bisa hadehh | -26.0 | negatif | positif | berguna | positive_pattern: label conflicts with clear positive phrase |
| 11217 | d25409ba-a115-4afb-926b-83f051fb2e44 | kenapa tidak bisa TF dana lgi sia sia daftar ternyata tidak bisa TF dana apk tidak berguna | kenapa tidak bisa transfer dana lgi sia sia daftar ternyata tidak bisa transfer dana aplikasi tidak berguna | -25.0 | negatif | positif | berguna | positive_pattern: label conflicts with clear positive phrase |
| 12646 | 0da1122d-561f-436b-8576-2661eb0f9bf7 | aplikasi g berguna,udh di download kgk bisa dbuka,loading trz smpai keluar tulisan timeout trz stuck, g buat kgk nh pdhl aplikasi org jakarta | aplikasi tidak berguna download kgk bisa dbuka loading trz smpai keluar tulisan timeout trz stuck tidak kgk nh pdhl aplikasi org jakarta | -25.0 | negatif | positif | berguna | positive_pattern: label conflicts with clear positive phrase |
| 3117 | d5a55841-3b1f-407d-8e28-2179a1fbb63a | ngga akan simpan uang di bank ini lagi, aplikasi perbankan paling tidak berguna yg pernah saya pakai. Tidak bisa transfer ke bank lain , e-wallet cuma bisa jakone pay, jak card, shopeepay dan dana. hadeh | ngga simpan uang bank aplikasi perbankan tidak berguna pakai tidak bisa transfer bank e wallet bisa jakone pay jak card shopeepay dana hadeh | -24.0 | negatif | positif | berguna | positive_pattern: label conflicts with clear positive phrase |
| 12241 | 4fbc680b-bff6-4674-b510-5f2d0e732c9c | aneh bgt gak bisa transfer antar bank, cuma bisa ke sesama bank DKI aja. introvert lu jadi bank!!! top ovo, gopay aja gak bisa katro banget ini aplikasi.. bikin susah gak memudahkan, yg bikin aplikasi ruwet kayanya pikirannya. | aneh banget tidak bisa transfer antar bank bisa sesama bank dki introvert lu bank top ovo gopay tidak bisa katro banget aplikasi bikin susah tidak memudahkan bikin aplikasi ruwet kayanya pikirannya | -24.0 | negatif | positif | memudahkan | positive_pattern: label conflicts with clear positive phrase |
| 7018 | fbfcaa4f-e567-4a0a-a8c7-3d06c5a8ab80 | G bisa cek saldo jakcard .. saat di cek loading terus .. fitur cek saldo jakcard jd g berguna .. hmm kecewa | tidak bisa cek saldo jakcard cek loading fitur cek saldo jakcard tidak berguna hmm kecewa | -23.0 | negatif | positif | berguna | positive_pattern: label conflicts with clear positive phrase |
| 6217 | 86a70d12-a18c-4fff-9176-8cff6bdc8968 | PAYAH, hubungi call center cuma ngabisin pulsa, bantuan 0%, masalah ga selesai, perkara login jakone mobile doang ribet banget, seharusnya tinggal login doang kalo udah punya rekening nya, kaya bank lain dong, gampang, tinggal login, kenapa harus dateng kecabang, ribet poll, tidak memudahkan pengguna, BANK YANG BURUK. | payah hubungi call center ngabisin pulsa bantuan 0 masalah tidak selesai perkara login jakone mobile doang ribet banget seharusnya tinggal login doang udah punya rekening nya kaya bank gampang tinggal login kenapa dateng kecabang ribet poll tidak memudahkan pengguna bank buruk | -22.0 | negatif | positif | memudahkan | positive_pattern: label conflicts with clear positive phrase |
| 10554 | 8840b9bb-2db7-42f0-87d9-ac69be05cdc0 | Bank DKI tidak berguna tanpa ada kesalahan ketika mau masuk login keterangan nya password di blokir | bank dki tidak berguna kesalahan masuk login keterangan nya password blokir | -21.0 | negatif | positif | berguna | positive_pattern: label conflicts with clear positive phrase |
| 10164 | 3bc0731e-dfea-4841-8e0b-fce65df4815f | tengah malam token habis, m-banking gak berguna sama sekali buat topup, klo bukan karena ada perlunya aja udah hapus nih, nanya ke CS online atau KCP juga ga guna ini scorenya 11/100 | malam token habis m banking tidak berguna topup klo bukan perlunya udah hapus nih nanya cs online kcp tidak scorenya 11 100 | -20.0 | negatif | positif | berguna | positive_pattern: label conflicts with clear positive phrase |
| 2842 | d0157b6e-c38a-4b77-91e7-440a06582cbd | apk error ga berguna | aplikasi error tidak berguna | -19.0 | negatif | positif | berguna | positive_pattern: label conflicts with clear positive phrase |
| 10008 | 2e956a98-1436-4dc6-8f61-c2860141aa67 | Sejauh ini pake aplikasi jakone mempermudah banget, banyak banget fitur fitur yang menarik dan user friendly. Selain itu aplikasi nya ga gampang eror jadi makin nyaman deh pake aplikasi ini. | sejauh pakai aplikasi jakone mempermudah banget banget fitur fitur menarik user friendly aplikasi nya tidak gampang error nyaman deh pakai aplikasi | -19.0 | negatif | positif | nyaman | positive_pattern: label conflicts with clear positive phrase |
| 12102 | dbd9efc8-a72e-4996-89fd-fdeea8dc9a60 | Gak berguna lemot aplksi apaan kyak gini. Malah sinyal kami yang dibilang masalah dan coba lagi. Sistem yang diatur harus di perbaiki pihak dki nya. Kirain cuma saya ternyata msih banyak yang diluar sana mengalami permasalahan yang sama | tidak berguna lambat aplksi apaan kyak gini sinyal dibilang masalah coba sistem diatur perbaiki pihak dki nya kirain ternyata msih diluar mengalami permasalahan | -19.0 | negatif | positif | berguna | positive_pattern: label conflicts with clear positive phrase |

## Recommendation
Dataset refined high-confidence layak dipakai untuk eksperimen training ulang IndoBERT sebagai varian pembanding, karena perubahan dibatasi pada kandidat high-confidence, jumlah baris dan split tetap utuh, serta label akhir valid. Namun, dataset ini belum sebaiknya dianggap final tanpa evaluasi tambahan: beberapa perubahan `negatif -> positif` masih terlihat berasal dari pola positif yang muncul dalam konteks negasi, misalnya `tidak berguna`, `tidak nyaman`, atau `tidak memudahkan`. Tetap bandingkan performa terhadap dataset asli, simpan model lama sebagai baseline, dan prioritaskan spot-check/manual review pada perubahan `negatif -> positif` sebelum menjadikan dataset ini sumber training utama.
