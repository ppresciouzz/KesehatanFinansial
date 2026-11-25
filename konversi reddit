import csv
import os
import sys

csv.field_size_limit(10 ** 9)

KOLOM_AKUN = ["username", "password"]
KOLOM_DATA = ["username", "kelompok", "pendapatan", "tabungan", "utang",
              "rasio_tabungan", "rasio_utang", "level"]
AMBANG_TABUNGAN = 10
AMBANG_UTANG = 20


def angka(teks):
    try:
        return float(teks)
    except (TypeError, ValueError):
        return None


def tentukan_kelompok(baris):
    if baris["edu_status"] in ("Full time student", "Part time student"):
        return "Mahasiswa"
    if baris["ft_status"] == "For Myself (Self-Employed)":
        return "Wirausaha"
    if baris["ft_status"] == "For an Organization (Employed)":
        return "Pekerja"
    return "Lainnya"


def tentukan_level(pendapatan, tabungan, utang):
    if tabungan * 100 >= AMBANG_TABUNGAN * pendapatan:
        if utang * 100 >= AMBANG_UTANG * pendapatan:
            return "C"
        return "A"
    if utang * 100 >= AMBANG_UTANG * pendapatan:
        return "D"
    return "B"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    buang_na = "--buang-na" in sys.argv
    lokasi = os.path.dirname(os.path.abspath(__file__))
    sumber = args[0] if len(args) >= 1 else os.path.join(lokasi, "reddit_finance.csv")
    folder = args[1] if len(args) >= 2 else os.path.join(lokasi, "hasil_konversi")
    if len(args) > 2:
        print("Argumen terlalu banyak.\n")
        print(__doc__)
        return
    if not os.path.exists(sumber):
        print(f"Berkas dataset tidak ditemukan: {sumber}")
        print("Letakkan reddit_finance.csv di folder yang sama dengan skrip ini, atau beri jalurnya sebagai argumen.")
        return
    os.makedirs(folder, exist_ok=True)

    with open(sumber, encoding="utf-8", errors="replace", newline="") as f:
        baris_dataset = list(csv.DictReader(f))

    akun, data = [], []
    dibuang_pendapatan = dibuang_na = 0
    for r in baris_dataset:
        pendapatan = angka(r["2020_gross_inc"])
        if pendapatan is None or pendapatan <= 0:
            dibuang_pendapatan += 1
            continue
        tabungan = angka(r["2020_invst_save"])
        utang = angka(r["2020_debt_repay"])
        if buang_na and (tabungan is None or utang is None):
            dibuang_na += 1
            continue
        pendapatan = int(round(pendapatan))
        tabungan = int(round(tabungan or 0))
        utang = int(round(utang or 0))
        username = "resp" + r[""]
        akun.append({"username": username, "password": username + "123"})
        data.append({
            "username": username,
            "kelompok": tentukan_kelompok(r),
            "pendapatan": pendapatan,
            "tabungan": tabungan,
            "utang": utang,
            "rasio_tabungan": tabungan / pendapatan,
            "rasio_utang": utang / pendapatan,
            "level": tentukan_level(pendapatan, tabungan, utang),
        })

    with open(os.path.join(folder, "akun.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=KOLOM_AKUN)
        w.writeheader()
        w.writerows(akun)
    with open(os.path.join(folder, "data_penilaian.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=KOLOM_DATA)
        w.writeheader()
        w.writerows(data)

    print(f"Baris dataset        : {len(baris_dataset)}")
    print(f"Dibuang (tanpa pendapatan): {dibuang_pendapatan}")
    if buang_na:
        print(f"Dibuang (NA tabungan/utang): {dibuang_na}")
    print(f"Akun & data ditulis  : {len(data)} baris di folder '{folder}'")
    for lv in "ABCD":
        print(f"  Level {lv}: {sum(1 for d in data if d['level'] == lv)}")


main()
