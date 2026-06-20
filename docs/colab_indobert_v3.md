# Panduan Google Colab IndoBERT V3

Dokumen ini menjelaskan cara menjalankan fine-tuning dan evaluation IndoBERT v3 baseline di Google Colab menggunakan GPU.

## 1. Siapkan Project di Google Colab

Ada dua cara umum:

1. Upload folder project ke Google Drive, misalnya ke:

   ```text
   /content/drive/MyDrive/Project Skripsi Analisis Sentimen Jakone Indobert
   ```

2. Clone repository jika project sudah ada di GitHub:

   ```bash
   !git clone <URL_REPOSITORY>
   ```

Jika memakai Google Drive, mount drive terlebih dahulu:

```python
from google.colab import drive
drive.mount('/content/drive')
```

## 2. Masuk ke Folder Project

Sesuaikan path dengan lokasi project di Google Drive atau hasil clone.

```python
%cd /content/drive/MyDrive/nama_project
```

Contoh:

```python
%cd "/content/drive/MyDrive/Project Skripsi Analisis Sentimen Jakone Indobert"
```

## 3. Install Dependency

File `requirements.txt` berada di root project, jadi jalankan:

```bash
!pip install -r requirements.txt
```

Jika Colab meminta restart runtime setelah instalasi, restart runtime lalu masuk kembali ke folder project.

## 4. Pastikan GPU Aktif

Di Colab, pilih menu:

```text
Runtime > Change runtime type > Hardware accelerator > GPU
```

Lalu cek dengan:

```python
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
```

Jika `torch.cuda.is_available()` bernilai `False`, berarti GPU belum aktif dan training akan sangat lambat.

## 5. Jalankan Fine-Tuning

Jalankan dari root project:

```bash
!python src/06_modeling/07_finetune_indobert.py
```

Script akan memakai dataset:

```text
data/final/06_jakone_modeling_master_v3.csv
```

Model hasil fine-tuning akan disimpan ke:

```text
models/indobert_v3_baseline/
```

## 6. Jalankan Evaluation

Setelah fine-tuning selesai, jalankan:

```bash
!python src/07_evaluation/08_evaluate_indobert.py
```

Evaluation memakai data `split_set == "test"` dari dataset v3.

## 7. Output Penting

File dan folder penting yang dihasilkan:

- `models/indobert_v3_baseline/`
- `models/indobert_v3_baseline/label_mapping.json`
- `outputs/modeling/indobert_v3_baseline/training_config.json`
- `outputs/modeling/indobert_v3_baseline/validation_metrics.json`
- `outputs/modeling/indobert_v3_baseline/training_log.json`
- `outputs/evaluation/indobert_v3_baseline/test_metrics.json`
- `outputs/evaluation/indobert_v3_baseline/classification_report.csv`
- `outputs/evaluation/indobert_v3_baseline/confusion_matrix.csv`
- `outputs/evaluation/indobert_v3_baseline/test_predictions.csv`

## 8. Catatan

- Baseline v3 pertama memakai `USE_CLASS_WEIGHT = False`.
- Jika ingin eksperimen dengan class weight, ubah `USE_CLASS_WEIGHT = True` di `src/06_modeling/07_finetune_indobert.py`.
- Jika folder `models/indobert_v3_baseline/` sudah berisi model, script fine-tuning akan berhenti agar model lama tidak tertimpa.
