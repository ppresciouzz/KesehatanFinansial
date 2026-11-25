import csv
import os

AMBANG_TABUNGAN = 10
AMBANG_UTANG = 20
BOBOT_TABUNGAN = 0.5
BOBOT_UTANG = 0.5
FILE_AKUN = "akun.csv"
FILE_DATA = "data_penilaian.csv"
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
GARIS_RANKING = "-" * 80


def baca_csv(nama):
    with open(nama, "r", newline="") as f:
        return list(csv.DictReader(f))

def tulis_baris(nama, kolom, baris):
    with open(nama, "a", newline="") as f:
        csv.DictWriter(f, fieldnames=kolom).writerow(baris)

def siapkan_berkas():
    for nama, kolom in ((FILE_AKUN, KOLOM_AKUN), (FILE_DATA, KOLOM_DATA)):
        if not os.path.exists(nama) or os.path.getsize(nama) == 0:
            with open(nama, "w", newline="") as f:
                csv.DictWriter(f, fieldnames=kolom).writeheader()

def daftar_akun():
    print("\n=== DAFTAR AKUN ===")
    username = input("Username baru: ").strip()
    if len(username) < 3:
        print("Username minimal 3 karakter.")
        return
    if any(a["username"].lower() == username.lower() for a in baca_csv(FILE_AKUN)):
        print("Username sudah dipakai.")
        return
    password = input("Password: ").strip()
    if len(password) < 4:
        print("Password minimal 4 karakter.")
        return
    if password != input("Ulangi password: ").strip():
        print("Password tidak sama.")
        return
    tulis_baris(FILE_AKUN, KOLOM_AKUN, {"username": username, "password": password})
    print("Akun berhasil dibuat. Silakan login.")

def proses_login():
    while True:
        print("\n=== LOGIN ===")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        for akun in baca_csv(FILE_AKUN):
            if akun["username"].lower() == username.lower() and akun["password"] == password:
                print(f"\nLogin berhasil. Selamat datang, {akun['username']}!")
                return akun["username"]
        print("\nUsername atau password salah.")
        while True:
            print("1. Coba login lagi\n2. Daftar akun\n3. Kembali")
            pilihan = input("Pilih: ").strip()
            if pilihan == "1":
                break
            elif pilihan == "2":
                daftar_akun()
                break
            elif pilihan == "3":
                return None
            print("Pilihan tidak dikenal.")

def baca_angka(pesan, harus_positif):
    while True:
        teks = input(pesan).strip()
        if teks.isascii() and teks.isdigit():
            nilai = int(teks)
            if harus_positif and nilai == 0:
                print("  Nilai harus lebih dari 0.")
                continue
            return nilai
        print("  Masukkan angka bulat saja, tanpa titik, koma, minus, atau huruf.")

def pilih_kelompok():
    print("Pilih kelompok:")
    for kode, nama in KELOMPOK.items():
        print(f"  {kode}. {nama}")
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

    rasio_tabungan = tabungan / pendapatan
    rasio_utang = utang / pendapatan
    tab_tinggi = tabungan * 100 >= AMBANG_TABUNGAN * pendapatan
    utang_tinggi = utang * 100 >= AMBANG_UTANG * pendapatan
    level = "ABCD"[(2 if utang_tinggi else 0) + (0 if tab_tinggi else 1)]

    tulis_baris(FILE_DATA, KOLOM_DATA, {
        "username": user, "kelompok": kelompok, "pendapatan": pendapatan,
        "tabungan": tabungan, "utang": utang, "rasio_tabungan": rasio_tabungan,
        "rasio_utang": rasio_utang, "level": level})

    print("\n--- HASIL ---")
    print(f"Kelompok       : {kelompok}")
    print(f"Rasio tabungan : {round(rasio_tabungan * 100, 2)}%  (ambang {AMBANG_TABUNGAN}%)")
    print(f"Rasio utang    : {round(rasio_utang * 100, 2)}%  (ambang {AMBANG_UTANG}%)")
    print(f"Level          : {level} - {KETERANGAN_LEVEL[level]}")
    print("Hasil sudah disimpan.")

def ranking(user, kelompok=None):
    terbaru = {b["username"]: b for b in baca_csv(FILE_DATA)}
    daftar = [r for r in terbaru.values() if kelompok is None or r["kelompok"] == kelompok]
    if not daftar:
        print("Belum ada data penilaian." if kelompok is None
              else f"Belum ada data di kelompok {kelompok}.")
        return

    maks_tabungan = max(float(r["rasio_tabungan"]) for r in daftar)
    min_utang = min((float(r["rasio_utang"]) for r in daftar if float(r["rasio_utang"]) > 0),
                    default=0)
    for r in daftar:
        t, u = float(r["rasio_tabungan"]), float(r["rasio_utang"])
        r["r_tabungan"] = t / maks_tabungan if maks_tabungan > 0 else 0
        r["r_utang"] = 1 if u == 0 else min_utang / u
        r["skor"] = BOBOT_TABUNGAN * r["r_tabungan"] + BOBOT_UTANG * r["r_utang"]

    daftar.sort(key=lambda r: (-r["skor"], "ABCD".index(r["level"])))

    judul = "RANKING GLOBAL (SAW)" if kelompok is None else f"RANKING KELOMPOK {kelompok} (SAW)"
    print(f"\n--- {judul} ---")
    print("No   Username       Kelompok   Level  Tab%     Utang%   R-Tab   R-Utang  Skor")
    print(GARIS_RANKING)
    posisi = 0
    for nomor, r in enumerate(daftar, 1):
        tab = str(round(float(r["rasio_tabungan"]) * 100, 2)) + "%"
        utg = str(round(float(r["rasio_utang"]) * 100, 2)) + "%"
        tanda = ""
        if r["username"] == user:
            tanda = "  <-- Anda"
            posisi = nomor
        print(f"{nomor:<5}{r['username'][:13]:<15}{r['kelompok']:<11}{r['level']:<7}{tab:<9}{utg:<9}"
              f"{round(r['r_tabungan'], 4):<8}{round(r['r_utang'], 4):<9}{round(r['skor'], 4)}{tanda}")
    print(GARIS_RANKING)
    if posisi > 0:
        print(f"Peringkat Anda: {posisi} dari {len(daftar)} pengguna.")
    else:
        print("Anda belum termasuk dalam ranking ini.")
    print(f"Metode SAW: Skor = {BOBOT_TABUNGAN} x R-Tab + {BOBOT_UTANG} x R-Utang")
    print("R-Tab = tabungan / tabungan tertinggi (benefit).")
    print("R-Utang = utang terendah (selain 0) / utang (cost); utang 0 bernilai 1.")

def menu_perangkingan(user):
    while True:
        print("\n=== MENU 2: PERANGKINGAN (METODE SAW) ===")
        print("1. Ranking global (semua pengguna)\n2. Ranking per kelompok\n3. Kembali")
        pilihan = input("Pilih: ").strip()
        if pilihan == "1":
            ranking(user)
        elif pilihan == "2":
            ranking(user, pilih_kelompok())
        elif pilihan == "3":
            return
        else:
            print("Pilihan tidak dikenal.")

def menu_rekomendasi(user):
    print("\n=== MENU 3: REKOMENDASI TINDAKAN ===")
    saya = {b["username"]: b for b in baca_csv(FILE_DATA)}.get(user)
    if saya is None:
        print("Anda belum punya data. Isi Menu 1 terlebih dahulu.")
        return
    pendapatan, tabungan, utang = int(saya["pendapatan"]), int(saya["tabungan"]), int(saya["utang"])
    level = saya["level"]
    print(f"Level Anda saat ini: {level} - {KETERANGAN_LEVEL[level]}\n")

    target_tabungan = -(-AMBANG_TABUNGAN * pendapatan // 100)
    tambah_tabungan = max(0, target_tabungan - tabungan)
    utang_maks = (AMBANG_UTANG * pendapatan - 1) // 100
    kurangi_utang = max(0, utang - utang_maks)

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

def menu_utama(user):
    while True:
        print(f"\n==== MENU UTAMA (pengguna: {user}) ====")
        print("1. Hitung rasio tabungan dan rasio pembayaran utang")
        print("2. Perangkingan (global dan kelompok)")
        print("3. Rekomendasi tindakan selanjutnya")
        print("4. Logout")
        pilihan = input("Pilih: ").strip()
        if pilihan == "1":
            menu_hitung(user)
        elif pilihan == "2":
            menu_perangkingan(user)
        elif pilihan == "3":
            menu_rekomendasi(user)
        elif pilihan == "4":
            print("\nAnda benar2 ingin logout?")
            if input("Ketik 'ya' untuk logout, ketik apapun untuk batal: ").strip().lower() != "ya":
                print("Logout dibatalkan.")
                continue
            print("Anda telah logout ya.")
            return
        else:
            print("Ketik 1-4 aja ya.")

def main():
    siapkan_berkas()
    while True:
        print("\n==== PENILAIAN KESEJAHTERAAN FINANSIAL ====")
        print("\n Haloo! Selamat datang di program penilaian kesejahteraan finansial kami dari kelompok 8A")
        print("1.Sagiv Albova Masri (2610931017) \n2.Kaila Nazwa Putri Rizani (2610933042) \n3.Felania Mutri Sari (2610932008)")
        print("Pilih menu:\n1. Login\n2. Daftar akun\n3. Keluar")
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
