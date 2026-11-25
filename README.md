# PROGRAM PENILAIAN KESEJAHTERAAN FINANSIAL MENGGUNAKAN METODE SIMPLE ADDITIVE WEIGHTING (SAW)

## 1. Deskripsi Proyek

Program Penilaian Kesejahteraan Finansial merupakan aplikasi berbasis Command Line Interface (CLI) yang dikembangkan menggunakan bahasa pemrograman Python. Aplikasi ini dirancang untuk membantu pengguna mengevaluasi kondisi kesejahteraan finansial berdasarkan tiga komponen utama, yaitu pendapatan, tabungan, dan pembayaran utang.

Program ini menerapkan metode **Simple Additive Weighting (SAW)** sebagai metode pengambilan keputusan untuk melakukan penilaian dan perangkingan kondisi finansial pengguna. Hasil penilaian diklasifikasikan ke dalam empat kategori, yaitu A, B, C, dan D, berdasarkan rasio tabungan dan rasio pembayaran utang terhadap pendapatan tahunan.

Selain menyediakan perhitungan dan perangkingan, aplikasi ini juga memberikan rekomendasi tindakan berdasarkan hasil evaluasi finansial pengguna. Dengan demikian, pengguna dapat memperoleh gambaran mengenai kondisi keuangannya serta mengetahui langkah yang dapat dilakukan untuk meningkatkan kesejahteraan finansial.

Proyek ini dikembangkan sebagai bagian dari tugas akademik Kelompok 8A.

## 2. Tujuan Pengembangan

Tujuan pengembangan program ini adalah:

1. Membantu pengguna mengevaluasi kondisi kesejahteraan finansial berdasarkan pendapatan, tabungan, dan pembayaran utang.
2. Menghitung rasio tabungan dan rasio pembayaran utang secara otomatis.
3. Mengklasifikasikan kondisi finansial pengguna ke dalam empat kategori berdasarkan kriteria yang telah ditentukan.
4. Menerapkan metode SAW untuk melakukan perangkingan kesejahteraan finansial.
5. Memberikan rekomendasi tindakan berdasarkan kategori hasil penilaian.
6. Menyediakan perbandingan kondisi finansial melalui perangkingan global dan perangkingan berdasarkan kelompok pengguna.

## 3. Fitur Aplikasi

### 3.1 Registrasi dan Autentikasi Pengguna

Aplikasi menyediakan fitur pengelolaan akun yang meliputi:
- Registrasi akun pengguna baru.
- Validasi panjang username dan password.
- Pemeriksaan username untuk mencegah penggunaan nama akun yang sama.
- Autentikasi pengguna melalui proses login.
- Fitur logout untuk mengakhiri sesi pengguna.

### 3.2 Perhitungan Rasio Keuangan

Pengguna diminta memasukkan data keuangan tahunan yang terdiri atas:
- Pendapatan atau uang saku tahunan.
- Jumlah tabungan tahunan.
- Total pembayaran utang tahunan.

Berdasarkan data tersebut, program menghitung dua indikator utama.

**A. Rasio Tabungan**

Rasio tabungan menunjukkan persentase pendapatan yang dialokasikan untuk tabungan.

Rumus:

Rasio Tabungan = (Tabungan / Pendapatan) × 100%

**B. Rasio Pembayaran Utang**

Rasio pembayaran utang menunjukkan persentase pendapatan yang digunakan untuk membayar utang.

Rumus:

Rasio Pembayaran Utang = (Pembayaran Utang / Pendapatan) × 100%

### 3.3 Klasifikasi Kesejahteraan Finansial

Program mengklasifikasikan kondisi finansial pengguna berdasarkan dua indikator, yaitu rasio tabungan dan rasio pembayaran utang.

| Kategori | Kondisi Tabungan | Kondisi Utang | Keterangan |
|---|---|---|---|
| A | Tinggi (≥ 10%) | Rendah (< 20%) | Terbaik |
| B | Rendah (< 10%) | Rendah (< 20%) | Baik |
| C | Tinggi (≥ 10%) | Tinggi (≥ 20%) | Berisiko |
| D | Rendah (< 10%) | Tinggi (≥ 20%) | Terburuk |

Ambang batas klasifikasi yang digunakan:
- Rasio tabungan sebesar 10% dari pendapatan.
- Rasio pembayaran utang sebesar 20% dari pendapatan.

### 3.4 Perangkingan Menggunakan Metode SAW

Program menerapkan metode Simple Additive Weighting (SAW) untuk menentukan peringkat kesejahteraan finansial pengguna.

Terdapat dua kriteria penilaian yang digunakan:

| Kriteria | Jenis | Bobot |
|---|---|---|
| Rasio Tabungan | Benefit | 0,5 |
| Rasio Pembayaran Utang | Cost | 0,5 |

**Normalisasi Kriteria**

1. Kriteria Benefit (Rasio Tabungan)

   R-Tabungan = Rasio Tabungan / Rasio Tabungan Tertinggi

2. Kriteria Cost (Rasio Pembayaran Utang)

   R-Utang = Rasio Utang Positif Terendah / Rasio Utang

   Apabila rasio utang bernilai nol, nilai normalisasi ditetapkan sebesar 1.

**Perhitungan Nilai Preferensi**

Nilai akhir dihitung menggunakan persamaan:

Skor SAW = (0,5 × R-Tabungan) + (0,5 × R-Utang)

Pengguna dengan nilai preferensi lebih tinggi akan memperoleh posisi peringkat yang lebih baik. Apabila terdapat nilai skor yang sama, kategori level digunakan sebagai kriteria pembanding.

Fitur perangkingan terdiri atas:
- Perangkingan global yang mencakup seluruh pengguna.
- Perangkingan berdasarkan kelompok pengguna.
- Penampilan nilai normalisasi dan skor akhir.
- Informasi posisi peringkat pengguna.

### 3.5 Rekomendasi Tindakan

Aplikasi memberikan rekomendasi berdasarkan kategori kesejahteraan finansial pengguna.

| Kategori | Rekomendasi |
|---|---|
| A | Mempertahankan kondisi tabungan dan pembayaran utang serta mempersiapkan dana darurat. |
| B | Meningkatkan jumlah tabungan hingga mencapai ambang batas yang ditentukan. |
| C | Mengurangi beban pembayaran utang dengan tetap mempertahankan tingkat tabungan. |
| D | Mengurangi pembayaran utang dan meningkatkan jumlah tabungan. |

Selain rekomendasi berdasarkan kategori, aplikasi juga memberikan tips pengelolaan keuangan berdasarkan kelompok pengguna.

### 3.6 Pengelompokan Pengguna

Pengguna dikelompokkan ke dalam empat kategori:

1. Mahasiswa
2. Pekerja
3. Wirausaha
4. Lainnya

### 3.7 Penyimpanan dan Pengelolaan Data

Aplikasi menggunakan format CSV sebagai media penyimpanan data.

Data yang dikelola meliputi:
- Informasi akun pengguna.
- Kelompok pengguna.
- Pendapatan tahunan.
- Jumlah tabungan tahunan.
- Pembayaran utang tahunan.
- Rasio tabungan.
- Rasio pembayaran utang.
- Kategori kesejahteraan finansial.

Sistem menggunakan data penilaian terbaru dari setiap username untuk proses perangkingan.

## 4. Teknologi yang Digunakan

Teknologi dan metode yang digunakan dalam pengembangan aplikasi ini meliputi:

| Teknologi/Metode | Kegunaan |
|---|---|
| Python | Bahasa pemrograman utama aplikasi. |
| CSV | Format penyimpanan dan pengelolaan data. |
| Simple Additive Weighting (SAW) | Metode pengambilan keputusan dan perangkingan. |
| Object-Oriented Programming (OOP) | Pendekatan pemrograman dalam struktur aplikasi versi final. |

Aplikasi menggunakan modul bawaan Python, sehingga tidak memerlukan instalasi pustaka eksternal.

## 5. Struktur Repositori

```text
Penilaian-Kesejahteraan-Finansial/
│
├── Program Kesehatan Finansial Menggunakan Metode SAW Final(25 November 2026).py
│
├── konversi_reddit.py
│
├── reddit_finance.csv
│
├── data_contoh_reddit.csv
│
├── akun.csv
│
├── data_penilaian.csv
│
├── hasil_konversi/
│   ├── akun.csv
│   └── data_penilaian.csv
│
└── README.md
```

Keterangan:
- `Program Kesehatan Finansial Menggunakan Metode SAW Final(25 November 2026).py`: Program utama untuk melakukan penilaian kesejahteraan finansial.
- `konversi_reddit.py`: Skrip untuk mengonversi dataset Reddit menjadi format data yang sesuai dengan aplikasi.
- `reddit_finance.csv`: Dataset sumber yang digunakan dalam proses konversi.
- `data_contoh_reddit.csv`: Dataset contoh yang digunakan untuk mengisi data penilaian awal.
- `akun.csv`: File penyimpanan informasi akun pengguna yang dibuat secara otomatis.
- `data_penilaian.csv`: File penyimpanan hasil penilaian finansial pengguna yang dibuat secara otomatis.
- `hasil_konversi/`: Direktori penyimpanan hasil proses konversi dataset.

## 6. Persyaratan Sistem

Untuk menjalankan aplikasi, diperlukan:

- Python versi 3.8 atau lebih baru.
- Sistem operasi Windows, Linux, atau macOS.
- Terminal atau Command Prompt.
- Git (opsional).

Tidak diperlukan instalasi pustaka eksternal karena aplikasi menggunakan modul bawaan Python.

## 7. Instalasi dan Penggunaan

### 7.1 Clone Repositori

Jalankan perintah berikut melalui terminal:

```bash
git clone https://github.com/USERNAME/REPOSITORY-NAME.git
```

Ganti `USERNAME` dan `REPOSITORY-NAME` dengan informasi repositori GitHub yang digunakan.

### 7.2 Masuk ke Direktori Proyek

```bash
cd REPOSITORY-NAME
```

### 7.3 Menjalankan Program Utama

Jalankan perintah berikut:

```bash
python "Program Kesehatan Finansial Menggunakan Metode SAW Final(25 November 2026).py"
```

Apabila menggunakan sistem yang memerlukan perintah `python3`, jalankan:

```bash
python3 "Program Kesehatan Finansial Menggunakan Metode SAW Final(25 November 2026).py"
```

### 7.4 Menggunakan Aplikasi

Setelah program dijalankan, pengguna akan ditampilkan menu awal yang terdiri atas:

1. Login
2. Daftar akun
3. Keluar

Pengguna yang belum memiliki akun dapat melakukan registrasi terlebih dahulu. Setelah berhasil login, pengguna dapat mengakses fitur perhitungan rasio keuangan, perangkingan, rekomendasi tindakan, dan pengelolaan data sesuai menu yang tersedia.

## 8. Pengolahan Dataset Reddit

Proyek ini menyediakan skrip `konversi_reddit.py` untuk mengolah dataset keuangan Reddit (`reddit_finance.csv`).

Untuk menjalankan proses konversi, gunakan perintah:

```bash
python konversi_reddit.py
```

Secara default, hasil konversi akan disimpan dalam direktori `hasil_konversi`.

Skrip juga menyediakan opsi `--buang-na` untuk mengabaikan baris yang tidak memiliki nilai tabungan atau pembayaran utang.

```bash
python konversi_reddit.py --buang-na
```

Hasil konversi terdiri atas:
- `akun.csv`
- `data_penilaian.csv`

**Catatan:** Hasil konversi disimpan di direktori `hasil_konversi`, sedangkan program utama membaca file `akun.csv` dan `data_penilaian.csv` dari direktori kerja. Oleh karena itu, pindahkan kedua file hasil konversi ke direktori kerja program utama apabila ingin menggunakannya secara langsung.

File `data_contoh_reddit.csv` dapat digunakan sebagai data contoh. Apabila tersedia, program utama akan memasukkan data tersebut ke dalam `data_penilaian.csv` ketika aplikasi pertama kali diinisialisasi, dengan mengabaikan username yang sudah memiliki data.

## 9. Batasan dan Catatan Penggunaan

Beberapa hal yang perlu diperhatikan dalam penggunaan aplikasi:

1. Seluruh data keuangan dimasukkan dalam satuan rupiah per tahun.
2. Nilai pendapatan harus lebih besar dari nol.
3. Nilai tabungan dan pembayaran utang harus berupa bilangan bulat nonnegatif.
4. Perangkingan menggunakan data penilaian terbaru dari setiap username.
5. Dataset contoh digunakan untuk mendukung pengujian fitur aplikasi.
6. Hasil penilaian merupakan evaluasi berdasarkan kriteria dan bobot yang telah ditetapkan, bukan merupakan penilaian profesional terhadap kondisi keuangan seseorang.
7. Pada versi ini, password disimpan dalam bentuk teks biasa pada file CSV. Oleh karena itu, aplikasi belum ditujukan untuk pengelolaan informasi akun yang bersifat sensitif.

## 10. Anggota Kelompok

**Kelompok 8A**

| No. | Nama | NIM |
|---|---|---|
| 1 | Sagiv Albova Masri | 2610931017 |
| 2 | Kaila Nazwa Putri Rizani | 2610933042 |
| 3 | Felania Mutri Sari | 2610932008 |

## 11. Lisensi

Proyek ini dikembangkan untuk keperluan akademik dan pembelajaran. Penggunaan, pengembangan, serta distribusi ulang program mengikuti ketentuan yang ditetapkan oleh pemilik repositori.





# FINANCIAL WELL-BEING ASSESSMENT PROGRAM USING THE SIMPLE ADDITIVE WEIGHTING (SAW) METHOD

## 1. Project Description

The Financial Well-Being Assessment Program is a Command Line Interface (CLI) application developed using the Python programming language. This application is designed to help users evaluate their financial well-being based on three main components: income, savings, and debt repayments.

The program implements the **Simple Additive Weighting (SAW)** method as a decision-making technique to assess and rank users' financial conditions. The assessment results are classified into four categories: A, B, C, and D, based on the savings ratio and debt repayment ratio relative to annual income.

In addition to financial calculations and rankings, the application provides recommendations based on users' financial assessment results. This enables users to understand their financial conditions and identify potential actions to improve their financial well-being.

This project was developed as part of Group 8A's academic assignment.

## 2. Development Objectives

The objectives of this project are:

1. To help users evaluate their financial well-being based on income, savings, and debt repayments.
2. To automatically calculate savings and debt repayment ratios.
3. To classify users' financial conditions into four categories based on predefined criteria.
4. To implement the SAW method for financial well-being ranking.
5. To provide recommendations based on financial assessment categories.
6. To compare users' financial conditions through global and group-based rankings.

## 3. Application Features

### 3.1 User Registration and Authentication

The application provides account management features, including:
- New user registration.
- Username and password length validation.
- Username availability checking to prevent duplicate accounts.
- User authentication through a login system.
- Logout functionality to terminate user sessions.

### 3.2 Financial Ratio Calculation

Users are required to enter the following annual financial information:
- Annual income or allowance.
- Total annual savings.
- Total annual debt repayments.

Based on the provided information, the application calculates two main indicators.

**A. Savings Ratio**

The savings ratio represents the percentage of income allocated to savings.

Formula:

Savings Ratio = (Savings / Income) × 100%

**B. Debt Repayment Ratio**

The debt repayment ratio represents the percentage of income used for debt repayments.

Formula:

Debt Repayment Ratio = (Debt Repayments / Income) × 100%

### 3.3 Financial Well-Being Classification

The application classifies users' financial conditions based on two indicators: savings ratio and debt repayment ratio.

| Category | Savings Condition | Debt Condition | Description |
|---|---|---|---|
| A | High (≥ 10%) | Low (< 20%) | Best |
| B | Low (< 10%) | Low (< 20%) | Good |
| C | High (≥ 10%) | High (≥ 20%) | Risky |
| D | Low (< 10%) | High (≥ 20%) | Worst |

The classification thresholds are:
- Savings ratio: 10% of income.
- Debt repayment ratio: 20% of income.

### 3.4 Ranking Using the SAW Method

The application implements the Simple Additive Weighting (SAW) method to determine users' financial well-being rankings.

Two assessment criteria are applied:

| Criteria | Type | Weight |
|---|---|---|
| Savings Ratio | Benefit | 0.5 |
| Debt Repayment Ratio | Cost | 0.5 |

**Criteria Normalization**

1. Benefit Criterion (Savings Ratio)

   R-Savings = Savings Ratio / Highest Savings Ratio

2. Cost Criterion (Debt Repayment Ratio)

   R-Debt = Lowest Positive Debt Ratio / Debt Ratio

   If the debt ratio equals zero, its normalized value is assigned 1.

**Preference Value Calculation**

The final score is calculated using the following equation:

SAW Score = (0.5 × R-Savings) + (0.5 × R-Debt)

Users with higher preference values receive better ranking positions. If two users have identical scores, their financial classification levels are used as the secondary comparison criterion.

The ranking features include:
- Global ranking across all users.
- Ranking based on user categories.
- Display of normalized values and final scores.
- Individual ranking position information.

### 3.5 Action Recommendations

The application provides recommendations according to each user's financial well-being category.

| Category | Recommendation |
|---|---|
| A | Maintain savings and debt repayment conditions while preparing an emergency fund. |
| B | Increase savings until the predefined threshold is reached. |
| C | Reduce debt repayment obligations while maintaining the savings level. |
| D | Reduce debt repayments and increase savings. |

In addition to category-based recommendations, the application provides financial management tips according to user categories.

### 3.6 User Classification

Users are divided into four categories:

1. Students
2. Employees
3. Entrepreneurs
4. Others

### 3.7 Data Storage and Management

The application uses CSV files as its data storage format.

The stored information includes:
- User account information.
- User categories.
- Annual income.
- Annual savings.
- Annual debt repayments.
- Savings ratio.
- Debt repayment ratio.
- Financial well-being category.

The ranking process uses the latest assessment record for each username.

## 4. Technologies Used

The technologies and methods used in this application include:

| Technology/Method | Purpose |
|---|---|
| Python | Main programming language. |
| CSV | Data storage and management format. |
| Simple Additive Weighting (SAW) | Decision-making and ranking method. |
| Object-Oriented Programming (OOP) | Programming approach used in the final application structure. |

The application uses Python's built-in modules and does not require external library installations.

## 5. Repository Structure

```text
Financial-Well-Being-Assessment/
│
├── Program Kesehatan Finansial Menggunakan Metode SAW Final(25 November 2026).py
│
├── konversi_reddit.py
│
├── reddit_finance.csv
│
├── data_contoh_reddit.csv
│
├── akun.csv
│
├── data_penilaian.csv
│
├── hasil_konversi/
│   ├── akun.csv
│   └── data_penilaian.csv
│
└── README.md
```

File descriptions:
- `Program Kesehatan Finansial Menggunakan Metode SAW Final(25 November 2026).py`: Main application for assessing financial well-being.
- `konversi_reddit.py`: Script for converting the Reddit dataset into a format compatible with the application.
- `reddit_finance.csv`: Source dataset used in the conversion process.
- `data_contoh_reddit.csv`: Sample dataset used to initialize assessment records.
- `akun.csv`: Automatically generated file for storing user account information.
- `data_penilaian.csv`: Automatically generated file for storing users' financial assessment results.
- `hasil_konversi/`: Directory containing the converted dataset files.

## 6. System Requirements

The following requirements are necessary to run the application:

- Python version 3.8 or newer.
- Windows, Linux, or macOS operating system.
- Terminal or Command Prompt.
- Git (optional).

No external Python libraries are required because the application uses built-in Python modules.

## 7. Installation and Usage

### 7.1 Clone the Repository

Run the following command in your terminal:

```bash
git clone https://github.com/USERNAME/REPOSITORY-NAME.git
```

Replace `USERNAME` and `REPOSITORY-NAME` with the corresponding GitHub repository information.

### 7.2 Navigate to the Project Directory

```bash
cd REPOSITORY-NAME
```

### 7.3 Run the Main Application

Execute the following command:

```bash
python "Program Kesehatan Finansial Menggunakan Metode SAW Final(25 November 2026).py"
```

If your system requires the `python3` command, use:

```bash
python3 "Program Kesehatan Finansial Menggunakan Metode SAW Final(25 November 2026).py"
```

### 7.4 Using the Application

After launching the program, users will be presented with the initial menu:

1. Login
2. Register
3. Exit

Users who do not have an account must register first. After successfully logging in, they can access the financial ratio calculation, ranking, action recommendation, and data management features.

## 8. Reddit Dataset Processing

This project provides the `konversi_reddit.py` script to process the Reddit financial dataset (`reddit_finance.csv`).

To execute the conversion process, run:

```bash
python konversi_reddit.py
```

By default, the converted files are stored in the `hasil_konversi` directory.

The script also provides the `--buang-na` option to exclude records with missing savings or debt repayment values.

```bash
python konversi_reddit.py --buang-na
```

The conversion process generates two files:
- `akun.csv`
- `data_penilaian.csv`

**Note:** The conversion results are stored in the `hasil_konversi` directory, whereas the main application reads `akun.csv` and `data_penilaian.csv` from its working directory. Therefore, move both converted files into the main application's working directory if you intend to use them directly.

The `data_contoh_reddit.csv` file can be used as sample data. When available, the main application imports its records into `data_penilaian.csv` during initialization while skipping usernames that already have assessment records.

## 9. Limitations and Usage Notes

The following points should be considered when using the application:

1. All financial data must be entered in Indonesian Rupiah (IDR) per year.
2. Income must be greater than zero.
3. Savings and debt repayment values must be non-negative integers.
4. The ranking process uses the latest assessment record for each username.
5. The sample dataset is provided to support application testing.
6. Assessment results are based on predefined criteria and weights and should not be considered professional financial evaluations.
7. In this version, passwords are stored as plain text in CSV files. Therefore, the application is not intended for managing sensitive account information.

## 10. Project Members

**Group 8A**

| No. | Name | Student ID |
|---|---|---|
| 1 | Sagiv Albova Masri | 2610931017 |
| 2 | Kaila Nazwa Putri Rizani | 2610933042 |
| 3 | Felania Mutri Sari | 2610932008 |

## 11. License

This project was developed for academic and educational purposes. The use, development, and redistribution of this application are subject to the conditions established by the repository owner.
