# Source Pipeline

Folder `src/` berisi script pipeline penelitian analisis sentimen ulasan pengguna aplikasi JakOne Mobile terkait aspek keamanan menggunakan IndoBERT.

## Struktur Folder

- `01_data_collection`: pengambilan data ulasan.
- `02_preprocessing`: pembersihan dan preprocessing teks.
- `03_lexicon`: download, checking, dan revisi lexicon.
- `04_labeling`: proses labelling berbasis lexicon dan validasi manual.
- `05_dataset`: split dataset untuk modeling.
- `06_modeling`: fine-tuning IndoBERT.
- `07_evaluation`: evaluasi model IndoBERT.
- `08_visualization`: visualisasi dan analisis hasil.

## Contoh Menjalankan Pipeline

Jalankan perintah dari root project.

```bash
python src/01_data_collection/01_collect_reviews.py
python src/02_preprocessing/02_preprocess_data.py
python src/03_lexicon/05b_revise_lexicon_v2.py
python src/04_labeling/04c_labeling_inset_v3.py
python src/04_labeling/05c_validasi_v3.py
python src/05_dataset/06_split_dataset.py
python src/06_modeling/07_finetune_indobert.py
python src/07_evaluation/08_evaluate_indobert.py
python src/08_visualization/09_visualization_analysis.py
```

Lexicon aktif untuk labelling revisi berada di `data/lexicon/active/`.
