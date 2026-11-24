# KesehatanFinansial
# Program Penilaian Kesejahteraan Finansial (Metode SAW)

Program Python berbasis terminal untuk menilai kesejahteraan finansial pengguna dari
rasio tabungan dan rasio pembayaran utang terhadap pendapatan, lalu memberi level,
peringkat (metode SAW), dan rekomendasi tindakan.

Dibuat oleh Kelompok 8A:

1. Sagiv Albova Masri
2. Kaila Nazwa Putri Rizani
3. Felania Mutri Sari

## Fitur

- Daftar akun dan login (username tidak membedakan huruf besar/kecil).
- **Menu 1 - Hitung rasio:** input pendapatan, tabungan, dan pembayaran utang per tahun, lalu program menghitung rasio dan level (A-D) dan menyimpannya.
- **Menu 2 - Perangkingan:** ranking global dan per kelompok (Mahasiswa, Pekerja, Wirausaha, Lainnya) dengan metode SAW.
- **Menu 3 - Rekomendasi:** saran tindakan sesuai level, beserta tips per kelompok.
- **Menu 4 - Tabel data:** seluruh data penilaian semua akun.

## Cara menjalankan

Kebutuhan: Python 3.8 atau lebih baru. Tidak ada library tambahan.

```
python program_kesejahteraan_finansial_saw.py
```

Saat pertama dijalankan, program membuat sendiri `akun.csv` dan `data_penilaian.csv`
di folder tempat program dijalankan.

## Level penilaian

| Level | Tabungan | Utang | Arti |
|---|---|---|---|
| A | >= 10% pendapatan | < 20% pendapatan | Terbaik |
| B | < 10% | < 20% | Baik |
| C | >= 10% | >= 20% | Berisiko |
| D | < 10% | >= 20% | Terburuk |

## Metode SAW

- R-Tab = rasio tabungan / rasio tabungan tertinggi (kriteria benefit).
- R-Utang = rasio utang terendah (selain 0) / rasio utang (kriteria cost); utang 0 bernilai 1.
- Skor = 0.5 x R-Tab + 0.5 x R-Utang.
- Skor yang sama dibedakan oleh level (A lebih baik dari B, dan seterusnya).

## Struktur repositori

```
Program Kesehatan Finansial Menggunakan Metode SAW.py   program utama
docs/                                                   racing satu baris data dan 98 test case (Word)
tools/konversi_reddit.py                                mengubah dataset reddit_finance.csv ke format program
.gitignore                                              mengecualikan data pengguna (akun dan hasil penilaian)
```

## Catatan data

- `akun.csv` menyimpan password apa adanya (teks biasa), karena itu berkas data tidak ikut di-commit (lihat `.gitignore`). Jangan mengunggah data akun asli.
- Untuk mencoba dengan data banyak, letakkan `reddit_finance.csv` di folder `tools/`, jalankan `python tools/konversi_reddit.py`, lalu salin `akun.csv` dan `data_penilaian.csv` dari `tools/hasil_konversi/` ke folder program.
