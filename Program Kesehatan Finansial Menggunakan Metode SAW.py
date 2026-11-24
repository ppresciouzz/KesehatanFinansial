import csv

AMBANG_TABUNGAN = 10
AMBANG_UTANG = 20

BOBOT_TABUNGAN = 0.5
BOBOT_UTANG = 0.5

FILE_AKUN = "akun.csv"
FILE_DATA = "data_penilaian.csv"

GARIS_RANKING = "--------------------------------------------------------------------------------"
GARIS_TABEL = "------------------------------------------------------------------------------------------"

KOLOM_AKUN = ["username", "password"]
KOLOM_DATA = ["username", "kelompok", "pendapatan", "tabungan", "utang",
              "rasio_tabungan", "rasio_utang", "level"]

KELOMPOK = {"1": "Mahasiswa", "2": "Pekerja", "3": "Wirausaha", "4": "Lainnya"}

KETERANGAN_LEVEL = {
    "A": "Tabungan tinggi, utang rendah (terbaik :D)",
    "B": "Tabungan rendah, utang rendah (baik :) )",
    "C": "Tabungan tinggi, utang tinggi (berisiko :/ )",
    "D": "Tabungan rendah, utang tinggi (terburuk :O)",
}

TIPS_KELOMPOK = {
    "Mahasiswa": "Atur uang saku per minggu dan hindari paylater atau pinjaman online, jangan boros ya bang.",
    "Pekerja": "Sisihkan tabungan di awal gajian, bukan dari sisa akhir bulan, nanti keteteran.",
    "Wirausaha": "Pisahkan keuangan pribadi dari keuangan usaha agar rasio lebih akurat ya, nanti minus loh.",
    "Lainnya": "Catat pemasukan dan pengeluaran rutin agar mudah dipantau, perbanyak tabungan kamu.",
}


def siapkan_berkas():
    for nama, kolom in ((FILE_AKUN, KOLOM_AKUN), (FILE_DATA, KOLOM_DATA)):
        f = open(nama, "a")
        f.close()
        f = open(nama, "r")
        isi = f.read()
        f.close()
        if isi == "":
            f = open(nama, "w", newline="")
            penulis = csv.DictWriter(f, fieldnames=kolom)
            penulis.writeheader()
            f.close()


def baca_csv(nama):
    f = open(nama, "r")
    hasil = []
    for baris in csv.DictReader(f):
        hasil.append(baris)
    f.close()
    return hasil


def daftar_akun():
    print("\n=== DAFTAR AKUN ===")
    username = input("Username baru: ").strip()
    if len(username) < 3:
        print("Username minimal 3 karakter.")
        return
    for akun in baca_csv(FILE_AKUN):
        if akun["username"].lower() == username.lower():
            print("Username sudah dipakai.")
            return
    password = input("Password: ").strip()
    if len(password) < 4:
        print("Password minimal 4 karakter.")
        return
    if password != input("Ulangi password: ").strip():
        print("Password tidak sama.")
        return
    f = open(FILE_AKUN, "a", newline="")
    penulis = csv.DictWriter(f, fieldnames=KOLOM_AKUN)
    penulis.writerow({"username": username, "password": password})
    f.close()
    print("Akun berhasil dibuat. Silakan login.")


def login():
    print("\n=== LOGIN ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    for akun in baca_csv(FILE_AKUN):
        if akun["username"].lower() == username.lower():
            if akun["password"] == password:
                return akun["username"]
    return None


def proses_login():
    while True:
        user = login()
        if user:
            print(f"\nLogin berhasil. Selamat datang, {user}!")
            return user
        print("\nUsername atau password salah.")
        while True:
            print("1. Coba login lagi")
            print("2. Daftar akun")
            print("3. Kembali")
            pilihan = input("Pilih: ").strip()
            if pilihan == "1":
                break
            elif pilihan == "2":
                daftar_akun()
                break
            elif pilihan == "3":
                return None
            else:
                print("Pilihan tidak dikenal.")


def hitung_rasio(bagian, pendapatan):
    return bagian / pendapatan


def tentukan_level(pendapatan, tabungan, utang):
    if tabungan * 100 >= AMBANG_TABUNGAN * pendapatan:
        if utang * 100 >= AMBANG_UTANG * pendapatan:
            return "C"
        else:
            return "A"
    else:
        if utang * 100 >= AMBANG_UTANG * pendapatan:
            return "D"
        else:
            return "B"


def angka_valid(teks):
    if len(teks) == 0:
        return False
    for huruf in teks:
        if huruf not in "0123456789":
            return False
    return True


def baca_angka(pesan, harus_positif):
    while True:
        teks = input(pesan).strip()
        if angka_valid(teks):
            nilai = int(teks)
            if harus_positif:
                if nilai == 0:
                    print("  Nilai harus lebih dari 0.")
                    continue
            return nilai
        print("  Masukkan angka bulat saja, tanpa titik, koma, minus, atau huruf.")


def data_terbaru():
    hasil = {}
    for baris in baca_csv(FILE_DATA):
        hasil[baris["username"]] = baris
    return hasil


def pilih_kelompok():
    print("Pilih kelompok:")
    for kode in KELOMPOK:
        print(f"  {kode}. {KELOMPOK[kode]}")
    while True:
        pilihan = input("Pilih kelompok: ").strip()
        if pilihan in KELOMPOK:
            return KELOMPOK[pilihan]
        print("  Pilihan tidak dikenal.")


def menu_hitung(user):
    print("\n=== MENU 1: RASIO TABUNGAN DAN RASIO PEMBAYARAN UTANG ===")
    kelompok = pilih_kelompok()

    print("\nIsi data keuangan PER TAHUN (angka bulat, dalam rupiah).")
    if kelompok == "Mahasiswa":
        pendapatan = baca_angka("Uang Saku per tahun    : ", True)
    else:
        pendapatan = baca_angka("Pendapatan kotor per tahun    : ", True)
    tabungan = baca_angka("Pendapatan yang ditabung       : ", False)
    utang = baca_angka("Total pembayaran utang per tahun: ", False)

    rasio_tabungan = hitung_rasio(tabungan, pendapatan)
    rasio_utang = hitung_rasio(utang, pendapatan)
    level = tentukan_level(pendapatan, tabungan, utang)

    f = open(FILE_DATA, "a", newline="")
    penulis = csv.DictWriter(f, fieldnames=KOLOM_DATA)
    penulis.writerow({"username": user, "kelompok": kelompok,
                      "pendapatan": pendapatan, "tabungan": tabungan,
                      "utang": utang, "rasio_tabungan": rasio_tabungan,
                      "rasio_utang": rasio_utang, "level": level})
    f.close()

    print("\n--- HASIL ---")
    print(f"Kelompok       : {kelompok}")
    print(f"Rasio tabungan : {round(rasio_tabungan * 100, 2)}%  (ambang {AMBANG_TABUNGAN}%)")
    print(f"Rasio utang    : {round(rasio_utang * 100, 2)}%  (ambang {AMBANG_UTANG}%)")
    print(f"Level          : {level} - {KETERANGAN_LEVEL[level]}")
    print("Hasil sudah disimpan.")


def nilai_level(level):
    if level == "A":
        return 1
    elif level == "B":
        return 2
    elif level == "C":
        return 3
    else:
        return 4


def hitung_saw(daftar):
    maks_tabungan = 0
    min_utang = 0
    for r in daftar:
        t = float(r["rasio_tabungan"])
        u = float(r["rasio_utang"])
        if t > maks_tabungan:
            maks_tabungan = t
        if u > 0:
            if min_utang == 0:
                min_utang = u
            elif u < min_utang:
                min_utang = u
    for r in daftar:
        t = float(r["rasio_tabungan"])
        u = float(r["rasio_utang"])
        if maks_tabungan > 0:
            r_tabungan = t / maks_tabungan
        else:
            r_tabungan = 0
        if u == 0:
            r_utang = 1
        else:
            r_utang = min_utang / u
        r["r_tabungan"] = r_tabungan
        r["r_utang"] = r_utang
        r["skor"] = BOBOT_TABUNGAN * r_tabungan + BOBOT_UTANG * r_utang
    return daftar


def lebih_baik(a, b):
    if a["skor"] != b["skor"]:
        return a["skor"] > b["skor"]
    return nilai_level(a["level"]) < nilai_level(b["level"])


def urutkan(daftar):
    n = len(daftar)
    i = 0
    while i < n:
        terbaik = i
        j = i + 1
        while j < n:
            if lebih_baik(daftar[j], daftar[terbaik]):
                terbaik = j
            j += 1
        sementara = daftar[i]
        daftar[i] = daftar[terbaik]
        daftar[terbaik] = sementara
        i += 1
    return daftar


def tampilkan_ranking(daftar, user, judul):
    print(f"\n--- {judul} ---")
    print("No   Username       Kelompok   Level  Tab%     Utang%   R-Tab   R-Utang  Skor")
    print(GARIS_RANKING)
    posisi = 0
    nomor = 1
    for r in daftar:
        teks_tabungan = str(round(float(r["rasio_tabungan"]) * 100, 2)) + "%"
        teks_utang = str(round(float(r["rasio_utang"]) * 100, 2)) + "%"
        tanda = ""
        if r["username"] == user:
            tanda = "  <-- Anda"
            posisi = nomor
        print(f"{nomor:<5}{r['username'][:13]:<15}{r['kelompok']:<11}{r['level']:<7}{teks_tabungan:<9}{teks_utang:<9}{round(r['r_tabungan'], 4):<8}{round(r['r_utang'], 4):<9}{round(r['skor'], 4)}{tanda}")
        nomor += 1
    print(GARIS_RANKING)
    if posisi > 0:
        print(f"Peringkat Anda: {posisi} dari {len(daftar)} pengguna.")
    else:
        print("Anda belum termasuk dalam ranking ini.")
    print(f"Metode SAW: Skor = {BOBOT_TABUNGAN} x R-Tab + {BOBOT_UTANG} x R-Utang")
    print("R-Tab = tabungan / tabungan tertinggi (benefit).")
    print("R-Utang = utang terendah (selain 0) / utang (cost); utang 0 bernilai 1.")


def ranking_global(user):
    terbaru = data_terbaru()
    daftar = []
    for nama in terbaru:
        daftar.append(terbaru[nama])
    if len(daftar) == 0:
        print("Belum ada data penilaian.")
        return
    daftar = hitung_saw(daftar)
    daftar = urutkan(daftar)
    tampilkan_ranking(daftar, user, "RANKING GLOBAL (SAW)")


def ranking_kelompok(user):
    kelompok = pilih_kelompok()
    terbaru = data_terbaru()
    daftar = []
    for nama in terbaru:
        if terbaru[nama]["kelompok"] == kelompok:
            daftar.append(terbaru[nama])
    if len(daftar) == 0:
        print(f"Belum ada data di kelompok {kelompok}.")
        return
    daftar = hitung_saw(daftar)
    daftar = urutkan(daftar)
    tampilkan_ranking(daftar, user, f"RANKING KELOMPOK {kelompok} (SAW)")


def menu_perangkingan(user):
    while True:
        print("\n=== MENU 2: PERANGKINGAN (METODE SAW) ===")
        print("1. Ranking global (semua pengguna)")
        print("2. Ranking per kelompok")
        print("3. Kembali")
        pilihan = input("Pilih: ").strip()
        if pilihan == "1":
            ranking_global(user)
        elif pilihan == "2":
            ranking_kelompok(user)
        elif pilihan == "3":
            return
        else:
            print("Pilihan tidak dikenal.")


def menu_rekomendasi(user):
    print("\n=== MENU 3: REKOMENDASI TINDAKAN ===")
    terbaru = data_terbaru()
    if user not in terbaru:
        print("Anda belum punya data. Isi Menu 1 terlebih dahulu.")
        return
    saya = terbaru[user]

    pendapatan = int(saya["pendapatan"])
    tabungan = int(saya["tabungan"])
    utang = int(saya["utang"])
    level = tentukan_level(pendapatan, tabungan, utang)
    print(f"Level Anda saat ini: {level} - {KETERANGAN_LEVEL[level]}\n")

    kebutuhan_tabungan = AMBANG_TABUNGAN * pendapatan
    target_tabungan = int(kebutuhan_tabungan / 100)
    if kebutuhan_tabungan % 100 != 0:
        target_tabungan += 1
    if target_tabungan > tabungan:
        tambah_tabungan = target_tabungan - tabungan
    else:
        tambah_tabungan = 0

    batas_utang = AMBANG_UTANG * pendapatan
    utang_maks = int(batas_utang / 100)
    if batas_utang % 100 == 0:
        utang_maks -= 1
    if utang > utang_maks:
        kurangi_utang = utang - utang_maks
    else:
        kurangi_utang = 0

    if level == "A":
        print("Pertahankan level A:")
        print(f"  - Pertahankan tabungan minimal Rp {target_tabungan} per tahun dan jaga utang maksimal Rp {utang_maks}.")
        print("  - Siapkan dana darurat agar tidak perlu berutang saat ada kebutuhan mendadak.")
    elif level == "B":
        print("Untuk naik ke level A, naikkan tabungan:")
        print(f"  - Tambah tabungan minimal Rp {tambah_tabungan} per tahun (target Rp {target_tabungan}, yaitu {AMBANG_TABUNGAN}% pendapatan).")
        print("  - Pertahankan utang tetap di bawah batas.")
    elif level == "C":
        print("Untuk naik ke level A, turunkan utang:")
        print(f"  - Kurangi pembayaran utang minimal Rp {kurangi_utang} per tahun (batas utang {AMBANG_UTANG}% pendapatan).")
        print("  - Prioritaskan melunasi utang berbunga tinggi lebih dahulu.")
        print("  - Pertahankan tabungan agar tetap di atas ambang.")
    else:
        print("Untuk naik dari level D, lakukan dua hal:")
        print(f"  1. Turunkan utang minimal Rp {kurangi_utang} per tahun (naik ke level B).")
        print(f"  2. Tambah tabungan minimal Rp {tambah_tabungan} per tahun (naik ke level A).")
        print("  Mulailah dari utang, karena beban cicilan membatasi kemampuan menabung.")

    print(f"\nTips untuk {saya['kelompok']}: {TIPS_KELOMPOK[saya['kelompok']]}")


def menu_tabel():
    print("\n=== MENU 4: TABEL DATA SEMUA AKUN ===")
    semua_akun = baca_csv(FILE_AKUN)
    data = baca_csv(FILE_DATA)
    print(f"Total akun: {len(semua_akun)} | Total penilaian: {len(data)}")
    hitung = {}
    if len(data) == 0:
        print("Belum ada data penilaian.")
    else:
        print(GARIS_TABEL)
        print("No  Username       Ke  Kelompok   Pendapatan   Tabungan   Utang      Tab%    Utang%  Level")
        print(GARIS_TABEL)
        nomor = 1
        for r in data:
            nama = r["username"]
            if nama in hitung:
                hitung[nama] += 1
            else:
                hitung[nama] = 1
            teks_tabungan = str(round(float(r["rasio_tabungan"]) * 100, 2)) + "%"
            teks_utang = str(round(float(r["rasio_utang"]) * 100, 2)) + "%"
            print(f"{nomor:<4}{nama[:13]:<15}{hitung[nama]:<4}{r['kelompok']:<11}{r['pendapatan']:<13}{r['tabungan']:<11}{r['utang']:<11}{teks_tabungan:<8}{teks_utang:<8}{r['level']}")
            nomor += 1
        print(GARIS_TABEL)
        print("Ke = urutan penilaian milik akun tersebut. Pendapatan, tabungan, dan utang per tahun (Rp).")

    tanpa_data = ""
    for akun in semua_akun:
        if akun["username"] not in hitung:
            tanpa_data = tanpa_data + akun["username"] + ", "
    if tanpa_data != "":
        print("Akun yang belum punya data: " + tanpa_data[:len(tanpa_data) - 2])


def menu_utama(user):
    while True:
        print(f"\n==== MENU UTAMA (pengguna: {user}) ====")
        print("1. Hitung rasio tabungan dan rasio pembayaran utang")
        print("2. Perangkingan (global dan kelompok)")
        print("3. Rekomendasi tindakan selanjutnya")
        print("4. Tabel data semua akun")
        print("5. Logout")
        pilihan = input("Pilih: ").strip()
        if pilihan == "1":
            menu_hitung(user)
        elif pilihan == "2":
            menu_perangkingan(user)
        elif pilihan == "3":
            menu_rekomendasi(user)
        elif pilihan == "4":
            menu_tabel()
        elif pilihan == "5":
            print("\nAnda benar2 ingin logout?")
            pilihan1 =input("Ketik 'ya' untuk logout, ketik apapun untuk batal: ").strip().lower()
            if pilihan1 != "ya":
                print("Logout dibatalkan.")
                continue
            print("Anda telah logout ya.")
            return
        else:
            print("Ketik 1-5 aja ya.")


def main():
    siapkan_berkas()
    while True:
        print("\n==== PENILAIAN KESEJAHTERAAN FINANSIAL ====")
        print("Haloo! Selamat datang di program penilaian kesejahteraan finansial kami dari kelompok 8A")
        print( "1.Sagiv Albova Masri (2610931017) \n2.Kaila Nazwa Putri Rizani (2610933042) \n3.Felania Mutri Sari (2610932008)")
        print("Pilih menu:")
        print("1. Login")
        print("2. Daftar akun")
        print("3. Keluar")
        pilihan = input("Pilih: ").strip()
        if pilihan == "1":
            user = proses_login()
            if user:
                menu_utama(user)
        elif pilihan == "2":
            daftar_akun()
        elif pilihan == "3":
            print("Terima kasih.")
            break
        else:
            print("Pilihan tidak dikenal.")


main()
