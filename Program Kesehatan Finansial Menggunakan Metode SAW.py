import csv
import os

AMBANG_TABUNGAN, AMBANG_UTANG = 10, 20
BOBOT_TABUNGAN, BOBOT_UTANG = 0.5, 0.5
FILE_AKUN, FILE_DATA, FILE_CONTOH = "akun.csv", "data_penilaian.csv", "data_contoh_reddit.csv"
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
GARIS = "-" * 80


class DataKeuangan:

    def __init__(self, username, kelompok, pendapatan, tabungan, utang):
        self.username, self.kelompok = username, kelompok
        self.pendapatan, self.tabungan, self.utang = pendapatan, tabungan, utang
        self.rasio_tabungan, self.rasio_utang = tabungan / pendapatan, utang / pendapatan
        tab_tinggi = tabungan * 100 >= AMBANG_TABUNGAN * pendapatan
        utang_tinggi = utang * 100 >= AMBANG_UTANG * pendapatan
        self.level = "ABCD"[(2 if utang_tinggi else 0) + (0 if tab_tinggi else 1)]
        self.r_tabungan = self.r_utang = self.skor = 0

    @classmethod
    def dari_baris(cls, b):
        return cls(b["username"], b["kelompok"], int(b["pendapatan"]), int(b["tabungan"]), int(b["utang"]))


class Penyimpanan:

    def __init__(self):
        for nama, kolom in ((FILE_AKUN, KOLOM_AKUN), (FILE_DATA, KOLOM_DATA)):
            if not os.path.exists(nama) or os.path.getsize(nama) == 0:
                with open(nama, "w", newline="") as f:
                    csv.DictWriter(f, fieldnames=kolom).writeheader()
        if os.path.exists(FILE_CONTOH):
            ada = {b["username"] for b in self._baca(FILE_DATA)}
            for b in self._baca(FILE_CONTOH):
                if b["username"] not in ada:
                    self.simpan_data(DataKeuangan.dari_baris(b))

    @staticmethod
    def _baca(nama):
        with open(nama, "r", newline="") as f:
            return list(csv.DictReader(f))

    @staticmethod
    def _tulis(nama, kolom, baris):
        with open(nama, "a", newline="") as f:
            csv.DictWriter(f, fieldnames=kolom).writerow(baris)

    def username_dipakai(self, username):
        return any(a["username"].lower() == username.lower() for a in self._baca(FILE_AKUN))

    def tambah_akun(self, username, password):
        self._tulis(FILE_AKUN, KOLOM_AKUN, {"username": username, "password": password})

    def simpan_data(self, d):
        self._tulis(FILE_DATA, KOLOM_DATA, {
            "username": d.username, "kelompok": d.kelompok, "pendapatan": d.pendapatan,
            "tabungan": d.tabungan, "utang": d.utang, "rasio_tabungan": d.rasio_tabungan,
            "rasio_utang": d.rasio_utang, "level": d.level})

    def data_terbaru(self, kelompok=None):
        hasil = {b["username"]: DataKeuangan.dari_baris(b) for b in self._baca(FILE_DATA)}
        return {u: d for u, d in hasil.items() if kelompok is None or d.kelompok == kelompok}


class PerankinganSAW:

    @staticmethod
    def hitung(daftar):
        maks_tab = max(d.rasio_tabungan for d in daftar)
        min_utang = min((d.rasio_utang for d in daftar if d.rasio_utang > 0), default=0)
        for d in daftar:
            d.r_tabungan = d.rasio_tabungan / maks_tab if maks_tab > 0 else 0
            d.r_utang = 1 if d.rasio_utang == 0 else min_utang / d.rasio_utang
            d.skor = BOBOT_TABUNGAN * d.r_tabungan + BOBOT_UTANG * d.r_utang
        daftar.sort(key=lambda d: (-d.skor, d.level))


class Aplikasi:

    @staticmethod
    def baca_angka(pesan, positif):
        while True:
            teks = input(pesan).strip()
            angka = teks.isascii() and teks.isdigit()
            if angka and not (positif and int(teks) == 0):
                return int(teks)
            print("  Nilai harus lebih dari 0." if angka
                  else "  Masukkan angka bulat saja, tanpa titik, koma, minus, atau huruf.")

    @staticmethod
    def pilih_kelompok():
        print("Pilih kelompok:")
        for kode, nama in KELOMPOK.items():
            print(f"  {kode}. {nama}")
        while True:
            pilihan = input("Pilih kelompok: ").strip()
            if pilihan in KELOMPOK:
                return KELOMPOK[pilihan]
            print("  Pilihan tidak dikenal.")

    def daftar_akun(self):
        print("\n=== DAFTAR AKUN ===")
        username = input("Username baru: ").strip()
        if len(username) < 3:
            return print("Username minimal 3 karakter.")
        if self.db.username_dipakai(username):
            return print("Username sudah dipakai.")
        password = input("Password: ").strip()
        if len(password) < 4:
            return print("Password minimal 4 karakter.")
        if password != input("Ulangi password: ").strip():
            return print("Password tidak sama.")
        self.db.tambah_akun(username, password)
        print("Akun berhasil dibuat. Silakan login.")

    def proses_login(self):
        while True:
            print("\n=== LOGIN ===")
            username, password = input("Username: ").strip(), input("Password: ").strip()
            self.user = None
            for a in self.db._baca(FILE_AKUN):
                if a["username"].lower() == username.lower() and a["password"] == password:
                    self.user = a["username"]
                    break
            if self.user:
                print(f"\nLogin berhasil. Selamat datang, {self.user}!")
                return True
            print("\nUsername atau password salah.")
            while True:
                pilihan = input("1. Coba login lagi\n2. Daftar akun\n3. Kembali\nPilih: ").strip()
                if pilihan == "3":
                    return False
                if pilihan in ("1", "2"):
                    if pilihan == "2":
                        self.daftar_akun()
                    break
                print("Pilihan tidak dikenal.")

    def menu_perangkingan(self):
        while True:
            pilihan = input("\n=== MENU 2: PERANGKINGAN (METODE SAW) ===\n1. Ranking global (semua pengguna)\n"
                            "2. Ranking per kelompok\n3. Kembali\nPilih: ").strip()
            if pilihan == "3":
                return
            if pilihan not in ("1", "2"):
                print("Pilihan tidak dikenal.")
                continue
            kelompok = None if pilihan == "1" else self.pilih_kelompok()
            daftar = list(self.db.data_terbaru(kelompok).values())
            if not daftar:
                print("Belum ada data penilaian." if kelompok is None else f"Belum ada data di kelompok {kelompok}.")
                continue
            PerankinganSAW.hitung(daftar)
            print(f"\n--- {'RANKING GLOBAL (SAW)' if kelompok is None else f'RANKING KELOMPOK {kelompok} (SAW)'} ---")
            print("No   Username       Kelompok   Level  Tab%     Utang%   R-Tab   R-Utang  Skor")
            print(GARIS)
            posisi = 0
            for no, d in enumerate(daftar, 1):
                tab, utg = f"{round(d.rasio_tabungan * 100, 2)}%", f"{round(d.rasio_utang * 100, 2)}%"
                tanda = "  <-- Anda" if d.username == self.user else ""
                if tanda:
                    posisi = no
                print(f"{no:<5}{d.username[:13]:<15}{d.kelompok:<11}{d.level:<7}{tab:<9}{utg:<9}"
                      f"{round(d.r_tabungan, 4):<8}{round(d.r_utang, 4):<9}{round(d.skor, 4)}{tanda}")
            print(GARIS)
            print(f"Peringkat Anda: {posisi} dari {len(daftar)} pengguna." if posisi
                  else "Anda belum termasuk dalam ranking ini.")
            print(f"Metode SAW: Skor = {BOBOT_TABUNGAN} x R-Tab + {BOBOT_UTANG} x R-Utang\n"
                  "R-Tab = tabungan / tabungan tertinggi (benefit).\n"
                  "R-Utang = utang terendah (selain 0) / utang (cost); utang 0 bernilai 1.")

    def menu_rekomendasi(self):
        print("\n=== MENU 3: REKOMENDASI TINDAKAN ===")
        saya = self.db.data_terbaru().get(self.user)
        if saya is None:
            return print("Anda belum punya data. Isi Menu 1 terlebih dahulu.")
        target = -(-AMBANG_TABUNGAN * saya.pendapatan // 100)
        tambah = max(0, target - saya.tabungan)
        utang_maks = (AMBANG_UTANG * saya.pendapatan - 1) // 100
        kurang = max(0, saya.utang - utang_maks)
        saran = {
            "A": ["Pertahankan level A:",
                  f"  - Pertahankan tabungan minimal Rp {target} per tahun dan jaga utang maksimal Rp {utang_maks}.",
                  "  - Siapkan dana darurat agar tidak perlu berutang saat ada kebutuhan mendadak."],
            "B": ["Untuk naik ke level A, naikkan tabungan:",
                  f"  - Tambah tabungan minimal Rp {tambah} per tahun (target Rp {target}, yaitu {AMBANG_TABUNGAN}% pendapatan).",
                  "  - Pertahankan utang tetap di bawah batas."],
            "C": ["Untuk naik ke level A, turunkan utang:",
                  f"  - Kurangi pembayaran utang minimal Rp {kurang} per tahun (batas utang {AMBANG_UTANG}% pendapatan).",
                  "  - Prioritaskan melunasi utang berbunga tinggi lebih dahulu.",
                  "  - Pertahankan tabungan agar tetap di atas ambang."],
            "D": ["Untuk naik dari level D, lakukan dua hal:",
                  f"  1. Turunkan utang minimal Rp {kurang} per tahun (naik ke level B).",
                  f"  2. Tambah tabungan minimal Rp {tambah} per tahun (naik ke level A).",
                  "  Mulailah dari utang, karena beban cicilan membatasi kemampuan menabung."],
        }[saya.level]
        print(f"Level Anda saat ini: {saya.level} - {KETERANGAN_LEVEL[saya.level]}\n")
        print("\n".join(saran + [f"\nTips untuk {saya.kelompok}: {TIPS_KELOMPOK[saya.kelompok]}"]))

    def menu_utama(self):
        while True:
            print(f"\n==== MENU UTAMA (pengguna: {self.user}) ====")
            pilihan = input("1. Hitung rasio tabungan dan rasio pembayaran utang\n2. Perangkingan (global dan kelompok)\n"
                            "3. Rekomendasi tindakan selanjutnya\n4. Logout\nPilih: ").strip()
            if pilihan == "1":
                print("\n=== MENU 1: RASIO TABUNGAN DAN RASIO PEMBAYARAN UTANG ===")
                kelompok = self.pilih_kelompok()
                print("\nIsi data keuangan PER TAHUN (angka bulat, dalam rupiah).")
                label = "Uang Saku per tahun    : " if kelompok == "Mahasiswa" else "Pendapatan kotor per tahun    : "
                pendapatan = self.baca_angka(label, True)
                tabungan = self.baca_angka("Pendapatan yang ditabung       : ", False)
                utang = self.baca_angka("Total pembayaran utang per tahun: ", False)
                data = DataKeuangan(self.user, kelompok, pendapatan, tabungan, utang)
                self.db.simpan_data(data)
                print("\n--- HASIL ---")
                print(f"Kelompok       : {kelompok}")
                print(f"Rasio tabungan : {round(data.rasio_tabungan * 100, 2)}%  (ambang {AMBANG_TABUNGAN}%)")
                print(f"Rasio utang    : {round(data.rasio_utang * 100, 2)}%  (ambang {AMBANG_UTANG}%)")
                print(f"Level          : {data.level} - {KETERANGAN_LEVEL[data.level]}")
                print("Hasil sudah disimpan.")
            elif pilihan == "2":
                self.menu_perangkingan()
            elif pilihan == "3":
                self.menu_rekomendasi()
            elif pilihan == "4":
                print("\nAnda benar2 ingin logout?")
                if input("Ketik 'ya' untuk logout, ketik apapun untuk batal: ").strip().lower() == "ya":
                    print("Anda telah logout ya.")
                    self.user = None
                    return
                print("Logout dibatalkan.")
            else:
                print("Ketik 1-4 aja ya.")

    def jalankan(self):
        self.db, self.user = Penyimpanan(), None
        while True:
            print("\n==== PENILAIAN KESEJAHTERAAN FINANSIAL ====")
            print("\n Haloo! Selamat datang di program penilaian kesejahteraan finansial kami dari kelompok 8A")
            print("1.Sagiv Albova Masri (2610931017) \n2.Kaila Nazwa Putri Rizani (2610933042) \n3.Felania Mutri Sari (2610932008)")
            pilihan = input("Pilih menu:\n1. Login\n2. Daftar akun\n3. Keluar\nPilih: ").strip()
            if pilihan == "1":
                if self.proses_login():
                    self.menu_utama()
            elif pilihan == "2":
                self.daftar_akun()
            elif pilihan == "3":
                return print("Terima kasih.")
            else:
                print("Pilihan tidak dikenal.")


Aplikasi().jalankan()
