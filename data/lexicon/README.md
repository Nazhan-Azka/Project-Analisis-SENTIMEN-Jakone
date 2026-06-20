# Lexicon

Folder ini berisi lexicon yang digunakan dalam proses labelling sentimen.

## active

Berisi file lexicon yang digunakan pada proses labelling revisi terbaru.

- `lexicon_v3_positive.tsv`: lexicon positif hasil revisi v3.
- `lexicon_v3_negative.tsv`: lexicon negatif hasil revisi v3.
- `kata_aspek_domain.txt`: daftar kata aspek domain mobile banking/keamanan yang tidak digunakan sebagai skor sentimen.

## archive

Berisi file lexicon lama dan draft yang digunakan pada proses pengembangan lexicon.

- `positive.tsv` dan `negative.tsv`: lexicon awal.
- `positive_cleaned.tsv` dan `negative_cleaned.tsv`: lexicon hasil cleaning awal.
- `custom_positive.tsv` dan `custom_negative.tsv`: tambahan kata domain JakOne Mobile.
- `lexicon_final_positive.tsv` dan `lexicon_final_negative.tsv`: lexicon final sebelum audit v3.

Lexicon utama yang digunakan untuk labelling revisi adalah file di folder `active`.
