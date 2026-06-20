# Ringkasan Artifact IndoBERT untuk BAB 4

Dokumen ini dirangkum dari artifact project lokal: dataset final, konfigurasi training, log training, evaluasi test, prediksi test, dan output analisis keyword.

## A. Konfigurasi Pelatihan Model
| Parameter | Nilai |
| --- | --- |
| Nama model | indobenchmark/indobert-base-p1 |
| Arsitektur model | BertForSequenceClassification |
| max_length | 128 |
| batch_size | 8 |
| learning_rate | 2e-05 |
| jumlah epoch | 2 |
| optimizer | AdamW (default Hugging Face Trainer) |
| loss function | CrossEntropyLoss; class weight nonaktif |
| random seed | 42 |
| scheduler | Linear scheduler dengan warmup_ratio=0.1 (default Trainer) |
| weight_decay | 0.01 |
| metric_for_best_model | macro_f1 |
| load_best_model_at_end | True |
| device saat training | cuda |

Catatan: optimizer dan scheduler mengikuti implementasi default `transformers.Trainer` berdasarkan parameter `learning_rate`, `weight_decay`, dan `warmup_ratio` pada script fine-tuning.

## B. Pembagian Dataset
Total dataset yang digunakan untuk modeling adalah **14.172 ulasan**.

| Split | Jumlah Data | Persentase |
| --- | --- | --- |
| train | 11337 | 80.00% |
| val | 1417 | 10.00% |
| test | 1418 | 10.01% |

Rasio pembagian data mendekati **80:10:10**; berdasarkan jumlah aktual: **11337:1417:1418**.

Distribusi label per split:
| Split | Negatif | Netral | Positif | Total |
| --- | --- | --- | --- | --- |
| train | 3684 | 917 | 6736 | 11337 |
| val | 460 | 115 | 842 | 1417 |
| test | 461 | 114 | 843 | 1418 |

## C. Hasil Training per Epoch
Train Loss pada tabel berikut dihitung sebagai rata-rata nilai `loss` yang tercatat pada log step training dalam masing-masing epoch.

| Epoch | Train Loss | Validation Loss | Validation Accuracy | Validation Macro F1 | Validation Macro Precision | Validation Macro Recall | Validation Weighted F1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.4298 | 0.3408 | 0.8998 | 0.8442 | 0.8447 | 0.8463 | 0.9003 |
| 2 | 0.2323 | 0.3064 | 0.9195 | 0.8681 | 0.8863 | 0.8543 | 0.9185 |

## D. Informasi Model Terbaik
| Informasi | Nilai |
| --- | --- |
| Best epoch | 2 |
| Best validation accuracy | 0.9195 |
| Best validation macro F1 | 0.8681 |
| Best validation loss | 0.3064 |
| Best model checkpoint | /content/drive/MyDrive/Draf Skripsi/Project Skripsi Analisis Sentimen Jakone Indobert/outputs/modeling/indobert_v3_baseline/checkpoints/checkpoint-2836 |

## E. Evaluasi Model pada Data Test
| Metrik | Nilai |
| --- | --- |
| Accuracy test | 0.9316 |
| Macro Precision | 0.8928 |
| Macro Recall | 0.8669 |
| Macro F1 | 0.8774 |
| Weighted Precision | 0.9325 |
| Weighted Recall | 0.9316 |
| Weighted F1 | 0.9309 |
| Jumlah data test | 1418 |

### Classification Report
| Label | Precision | Recall | F1-score | Support |
| --- | --- | --- | --- | --- |
| negatif | 0.8787 | 0.9588 | 0.9170 | 461.0000 |
| netral | 0.8229 | 0.6930 | 0.7524 | 114.0000 |
| positif | 0.9768 | 0.9490 | 0.9627 | 843.0000 |
| accuracy | 0.9316 | 0.9316 | 0.9316 | 0.9316 |
| macro avg | 0.8928 | 0.8669 | 0.8774 | 1418.0000 |
| weighted avg | 0.9325 | 0.9316 | 0.9309 | 1418.0000 |

### Confusion Matrix
Baris menunjukkan label aktual, sedangkan kolom menunjukkan label prediksi model.

| Aktual / Prediksi | Negatif | Netral | Positif |
| --- | --- | --- | --- |
| actual_negatif | 442 | 10 | 9 |
| actual_netral | 25 | 79 | 10 |
| actual_positif | 36 | 7 | 800 |

## F. Error Analysis
### Contoh Prediksi Benar
| Review | True Label | Pred Label | Confidence | Prob Negatif | Prob Netral | Prob Positif |
| --- | --- | --- | --- | --- | --- | --- |
| ya lumayan bagus | positif | positif | 0.9993 | 0.0003 | 0.0003 | 0.9993 |
| bagus happy | positif | positif | 0.9993 | 0.0003 | 0.0003 | 0.9993 |
| topup gopay ilang ovo ilang dana ilang shoppe pay gagal transfer bank laen tidak bisa error bulan perhatian lebih lanjut | negatif | negatif | 0.9986 | 0.9986 | 0.0009 | 0.0005 |
| transfer m banking error cek ambil duit atm pakai kartu error gagal ksni ksni ni bank tidak jelas stiap bulan pasti service error sinyal bagus bagus mang aplik… | negatif | negatif | 0.9986 | 0.9986 | 0.0008 | 0.0006 |
| ngga | netral | netral | 0.9880 | 0.0049 | 0.9880 | 0.0071 |
| lag | netral | netral | 0.9874 | 0.0055 | 0.9874 | 0.0071 |

### Contoh Prediksi Salah
| Review | True Label | Pred Label | Confidence | Prob Negatif | Prob Netral | Prob Positif |
| --- | --- | --- | --- | --- | --- | --- |
| bank tidak tidak bisa transfer bca | positif | negatif | 0.9983 | 0.9983 | 0.0012 | 0.0005 |
| bintang isi e walet bermasalah belum pemberitahuan berhasil saldo berkurang cek mutasi e walet proses nunggu semaleman saldonya belum terkirim mutasi proses la… | positif | negatif | 0.9983 | 0.9983 | 0.0010 | 0.0007 |
| jelek banget sumpah bukanya mempermudah mempersulit wkwkwkww haaaaaaaaaaa | positif | negatif | 0.9977 | 0.9977 | 0.0016 | 0.0007 |
| knp aplikasi bank dki tidak fitur transfer bank tidak jls banget | positif | negatif | 0.9977 | 0.9977 | 0.0015 | 0.0008 |
| lampu indikator nya sumpah bikin ribet lho transaksinya | positif | negatif | 0.9972 | 0.9972 | 0.0019 | 0.0009 |
| daftr ko gagal kemaren dateng cs bank dki udah ngisi data daftar jakone katanya suruh nunggu 1x24 giliran ganti hari daftar suruh ganti email padahal email did… | positif | negatif | 0.9971 | 0.9971 | 0.0016 | 0.0013 |
| mbanking kocak ape ape lambat transfer terima transfer kadang bisa kadang kagak kebanyakan kagak bisanye hade hadehh | positif | negatif | 0.9968 | 0.9968 | 0.0020 | 0.0012 |
| kenapa mempunyai rekening terdaftar disuruh memasukan data tolong kenapa susah mendaftar jakone mobile | netral | negatif | 0.9966 | 0.9966 | 0.0025 | 0.0009 |

### Contoh Kasus Ambigu atau Sulit
Contoh berikut dipilih dari prediksi dengan margin probabilitas paling kecil antar kelas tertinggi, sehingga model relatif kurang yakin membedakan kelas.

| Review | True Label | Pred Label | Confidence | Prob Negatif | Prob Netral | Prob Positif |
| --- | --- | --- | --- | --- | --- | --- |
| baguss | positif | netral | 0.4993 | 0.0065 | 0.4993 | 0.4943 |
| kapan aplikasi nya biaa berjalan normal | netral | positif | 0.4806 | 0.0499 | 0.4696 | 0.4806 |
| tidak bisa masuk setelah ganti nomer | netral | netral | 0.4181 | 0.4043 | 0.4181 | 0.1776 |
| transfer jakone mobile transaksi proses 24jam saldo belum balik aplikasi gajelas | positif | positif | 0.4975 | 0.0308 | 0.4717 | 0.4975 |
| woii minn gua bikin akun stak foto gimna make wifi pdhl berkali kg bisa payah | netral | positif | 0.4382 | 0.4057 | 0.1561 | 0.4382 |
| aplikasi horor transfer 75ribu rekening dki saldo 70rebu cs selisih 5ribu disuruh kekantor cabang gw tarik tunai gocap atm bca info atm bca uang tidak keluar n… | negatif | negatif | 0.5059 | 0.5059 | 0.0219 | 0.4722 |
| kenapa ya setiap verifikasi foto muncul kode 7009 akhirnya tidak bisa2 k tahap selanjutnya infokan ig tidak tanggepan | positif | negatif | 0.4760 | 0.4760 | 0.0859 | 0.4381 |
| jackone mobile melakukan transaksi tidak bisa mohon penjelasannya terima kasih | positif | positif | 0.4805 | 0.4413 | 0.0782 | 0.4805 |

Ringkasan pola kesalahan: kelas `netral` memiliki recall paling rendah dibanding kelas lain, sehingga sebagian ulasan netral lebih sering tertarik ke kelas negatif atau positif. Pada confusion matrix, 25 data netral diprediksi negatif dan 10 data netral diprediksi positif.

## G. Word Cloud dan Analisis Kata
Top keyword berikut berasal dari `outputs/analysis/indobert_v3_baseline/keyword_issue_by_label_v3.csv`. Persentase menunjukkan proporsi kemunculan keyword terhadap jumlah data pada label terkait.

### Top 20 Kata Sentimen Positif
| No | Kata | Frekuensi | Persentase dalam Label |
| --- | --- | --- | --- |
| 1 | transaksi | 1489 | 17.68 |
| 2 | transfer | 552 | 6.55 |
| 3 | rekening | 402 | 4.77 |
| 4 | aman | 357 | 4.24 |
| 5 | qris | 345 | 4.10 |
| 6 | saldo | 192 | 2.28 |
| 7 | otp | 157 | 1.86 |
| 8 | login | 108 | 1.28 |
| 9 | kode | 108 | 1.28 |
| 10 | error | 96 | 1.14 |
| 11 | akun | 91 | 1.08 |
| 12 | verifikasi | 87 | 1.03 |
| 13 | gagal | 48 | 0.57 |
| 14 | password | 35 | 0.42 |
| 15 | hilang | 27 | 0.32 |
| 16 | blokir | 14 | 0.17 |
| 17 | pin | 13 | 0.15 |
| 18 | penipuan | 3 | 0.04 |
| 19 | fraud | 0 | 0.00 |
| 20 | bobol | 0 | 0.00 |

### Top 20 Kata Sentimen Negatif
| No | Kata | Frekuensi | Persentase dalam Label |
| --- | --- | --- | --- |
| 1 | transfer | 924 | 20.07 |
| 2 | error | 598 | 12.99 |
| 3 | login | 451 | 9.79 |
| 4 | gagal | 413 | 8.97 |
| 5 | transaksi | 361 | 7.84 |
| 6 | saldo | 352 | 7.64 |
| 7 | otp | 351 | 7.62 |
| 8 | rekening | 292 | 6.34 |
| 9 | verifikasi | 233 | 5.06 |
| 10 | kode | 229 | 4.97 |
| 11 | qris | 137 | 2.98 |
| 12 | hilang | 125 | 2.71 |
| 13 | akun | 97 | 2.11 |
| 14 | password | 88 | 1.91 |
| 15 | aman | 29 | 0.63 |
| 16 | pin | 28 | 0.61 |
| 17 | blokir | 27 | 0.59 |
| 18 | penipuan | 4 | 0.09 |
| 19 | fraud | 0 | 0.00 |
| 20 | bobol | 0 | 0.00 |

### Top 20 Kata Sentimen Netral
| No | Kata | Frekuensi | Persentase dalam Label |
| --- | --- | --- | --- |
| 1 | otp | 99 | 8.64 |
| 2 | transfer | 62 | 5.41 |
| 3 | kode | 58 | 5.06 |
| 4 | login | 50 | 4.36 |
| 5 | rekening | 44 | 3.84 |
| 6 | transaksi | 31 | 2.71 |
| 7 | verifikasi | 22 | 1.92 |
| 8 | saldo | 22 | 1.92 |
| 9 | gagal | 14 | 1.22 |
| 10 | qris | 11 | 0.96 |
| 11 | akun | 11 | 0.96 |
| 12 | password | 7 | 0.61 |
| 13 | error | 7 | 0.61 |
| 14 | blokir | 6 | 0.52 |
| 15 | aman | 4 | 0.35 |
| 16 | hilang | 3 | 0.26 |
| 17 | pin | 1 | 0.09 |
| 18 | penipuan | 0 | 0.00 |
| 19 | fraud | 0 | 0.00 |
| 20 | bobol | 0 | 0.00 |

### Top Keyword Keseluruhan
| No | Kata | Total | Negatif | Netral | Positif | Persentase Total |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | transaksi | 1881 | 361 | 31 | 1489 | 13.27 |
| 2 | transfer | 1538 | 924 | 62 | 552 | 10.85 |
| 3 | rekening | 738 | 292 | 44 | 402 | 5.21 |
| 4 | error | 701 | 598 | 7 | 96 | 4.95 |
| 5 | login | 609 | 451 | 50 | 108 | 4.30 |
| 6 | otp | 607 | 351 | 99 | 157 | 4.28 |
| 7 | saldo | 566 | 352 | 22 | 192 | 3.99 |
| 8 | qris | 493 | 137 | 11 | 345 | 3.48 |
| 9 | gagal | 475 | 413 | 14 | 48 | 3.35 |
| 10 | kode | 395 | 229 | 58 | 108 | 2.79 |
| 11 | aman | 390 | 29 | 4 | 357 | 2.75 |
| 12 | verifikasi | 342 | 233 | 22 | 87 | 2.41 |
| 13 | akun | 199 | 97 | 11 | 91 | 1.40 |
| 14 | hilang | 155 | 125 | 3 | 27 | 1.09 |
| 15 | password | 130 | 88 | 7 | 35 | 0.92 |
| 16 | blokir | 47 | 27 | 6 | 14 | 0.33 |
| 17 | pin | 42 | 28 | 1 | 13 | 0.30 |
| 18 | penipuan | 7 | 4 | 0 | 3 | 0.05 |
| 19 | fraud | 0 | 0 | 0 | 0 | 0.00 |
| 20 | bobol | 0 | 0 | 0 | 0 | 0.00 |

## Sumber Artifact
- `outputs/modeling/indobert_v3_baseline/training_config.json`
- `outputs/modeling/indobert_v3_baseline/checkpoints/checkpoint-2836/trainer_state.json`
- `outputs/modeling/indobert_v3_baseline/validation_metrics.json`
- `outputs/evaluation/indobert_v3_baseline/test_metrics.json`
- `outputs/evaluation/indobert_v3_baseline/classification_report.csv`
- `outputs/evaluation/indobert_v3_baseline/confusion_matrix.csv`
- `outputs/evaluation/indobert_v3_baseline/test_predictions.csv`
- `outputs/analysis/indobert_v3_baseline/keyword_issue_by_label_v3.csv`
- `data/final/06_jakone_modeling_master_v3.csv`