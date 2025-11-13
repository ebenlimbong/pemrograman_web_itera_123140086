# Tugas Praktikum: Program Pengelolaan Data Nilai Mahasiswa

# Membuat data mahasiswa menggunakan array of object
mahasiswa = [
    {"nama": "Andi Wijaya", "NIM": "2023001", "nilai_uts": 85, "nilai_uas": 90, "nilai_tugas": 88},
    {"nama": "Budi Santoso", "NIM": "2023002", "nilai_uts": 75, "nilai_uas": 78, "nilai_tugas": 80},
    {"nama": "Citra Dewi", "NIM": "2023003", "nilai_uts": 92, "nilai_uas": 88, "nilai_tugas": 90},
    {"nama": "Dewi Lestari", "NIM": "2023004", "nilai_uts": 65, "nilai_uas": 68, "nilai_tugas": 70},
    {"nama": "Eko Prasetyo", "NIM": "2023005", "nilai_uts": 55, "nilai_uas": 58, "nilai_tugas": 60}
]

# Fungsi hitung nilai akhir
def hitung_nilai_akhir(mhs):
    """Menghitung nilai akhir berdasarkan bobot: UTS 30%, UAS 40%, Tugas 30%"""
    return (mhs["nilai_uts"] * 0.3) + (mhs["nilai_uas"] * 0.4) + (mhs["nilai_tugas"] * 0.3)

# Fungsi menentukan grade
def tentukan_grade(nilai_akhir):
    """Menentukan grade berdasarkan nilai akhir"""
    if nilai_akhir >= 80:
        return 'A'
    elif nilai_akhir >= 70:
        return 'B'
    elif nilai_akhir >= 60:
        return 'C'
    elif nilai_akhir >= 50:
        return 'D'
    else:
        return 'E'

# Fungsi menampilkan data dalam format tabel
def tampilkan_tabel():
    """Menampilkan semua data mahasiswa dalam format tabel"""
    print("\n" + "="*80)
    print(f"{'No':<3} {'Nama':<20} {'NIM':<10} {'UTS':<5} {'UAS':<5} {'Tugas':<6} {'Akhir':<6} {'Grade':<6}")
    print("="*80)
    for i, mhs in enumerate(mahasiswa, 1):
        nilai_akhir = hitung_nilai_akhir(mhs)
        grade = tentukan_grade(nilai_akhir)
        print(f"{i:<3} {mhs['nama']:<20} {mhs['NIM']:<10} {mhs['nilai_uts']:<5} "
              f"{mhs['nilai_uas']:<5} {mhs['nilai_tugas']:<6} {nilai_akhir:<6.2f} {grade:<6}")
    print("="*80)

# Fungsi mencari mahasiswa dengan nilai tertinggi/terendah
def cari_mahasiswa_extreme(tipe="tinggi"):
    # Mencari mahasiswa dengan nilai akhir tertinggi atau terendah
    if not mahasiswa:
        return None
    if tipe == "tinggi":
        mhs_terbaik = max(mahasiswa, key=lambda x: hitung_nilai_akhir(x))
        return mhs_terbaik, "tertinggi"
    else:
        mhs_terburuk = min(mahasiswa, key=lambda x: hitung_nilai_akhir(x))
        return mhs_terburuk, "terendah"

# Fungsi input data mahasiswa baru
def tambah_mahasiswa():
    # Menambahkan data mahasiswa baru ke list
    print("\n--- Input Data Mahasiswa Baru ---")
    nama = input("Masukkan nama mahasiswa: ").strip()
    nim = input("Masukkan NIM: ").strip()
    try:
        uts = float(input("Masukkan nilai UTS: "))
        uas = float(input("Masukkan nilai UAS: "))
        tugas = float(input("Masukkan nilai Tugas: "))
    except ValueError:
        print(" Nilai harus berupa angka!")
        return

    # Validasi nilai yang di input
    if not (0 <= uts <= 100 and 0 <= uas <= 100 and 0 <= tugas <= 100):
        print(" Nilai harus antara 0-100!")
        return

    mahasiswa_baru = {
        "nama": nama,
        "NIM": nim,
        "nilai_uts": uts,
        "nilai_uas": uas,
        "nilai_tugas": tugas
    }
    mahasiswa.append(mahasiswa_baru)
    print(f" Mahasiswa {nama} berhasil ditambahkan!")

# Fungsi filter mahasiswa berdasarkan grade
def filter_berdasarkan_grade():
    """Menampilkan daftar mahasiswa berdasarkan grade yang dipilih"""
    grade_input = input("Masukkan grade yang ingin difilter (A/B/C/D/E): ").upper().strip()
    if grade_input not in ['A', 'B', 'C', 'D', 'E']:
        print(" Grade tidak valid!")
        return

    filtered = []
    for mhs in mahasiswa:
        nilai_akhir = hitung_nilai_akhir(mhs)
        grade = tentukan_grade(nilai_akhir)
        if grade == grade_input:
            filtered.append(mhs)

    if not filtered:
        print(f" Tidak ada mahasiswa dengan grade {grade_input}.")
        return

    print(f"\n--- Daftar Mahasiswa dengan Grade {grade_input} ---")
    print(f"{'No':<3} {'Nama':<20} {'NIM':<10} {'Nilai Akhir':<10} {'Grade':<6}")
    print("-"*60)
    for i, mhs in enumerate(filtered, 1):
        nilai_akhir = hitung_nilai_akhir(mhs)
        print(f"{i:<3} {mhs['nama']:<20} {mhs['NIM']:<10} {nilai_akhir:<10.2f} {grade_input:<6}")

# Fungsi hitung rata-rata nilai kelas
def hitung_rata_rata_kelas():
    # Hitung rata rata nilai akhir seluruh siswa 
    if not mahasiswa:
        print(" Belum ada data mahasiswa.")
        return 0.0

    total_nilai = sum(hitung_nilai_akhir(mhs) for mhs in mahasiswa)
    rata_rata = total_nilai / len(mahasiswa)
    print(f"\n Rata-rata nilai kelas: {rata_rata:.2f}")
    return rata_rata

# Menu utama
def menu_utama():
    # Menu awal tampilan 
    while True:
        print("\n" + "="*50)
        print("       PROGRAM PENGELOLAAN DATA NILAI MAHASISWA")
        print("="*50)
        print("1. Tampilkan Semua Data Mahasiswa")
        print("2. Tambah Data Mahasiswa Baru")
        print("3. Cari Mahasiswa Nilai Tertinggi")
        print("4. Cari Mahasiswa Nilai Terendah")
        print("5. Filter Mahasiswa Berdasarkan Grade")
        print("6. Hitung Rata-rata Nilai Kelas")
        print("7. Keluar")
        print("="*50)

        pilihan = input("Pilih menu (1-7): ").strip()

        if pilihan == '1':
            tampilkan_tabel()
        elif pilihan == '2':
            tambah_mahasiswa()
        elif pilihan == '3':
            mhs, tipe = cari_mahasiswa_extreme("tinggi")
            if mhs:
                nilai_akhir = hitung_nilai_akhir(mhs)
                grade = tentukan_grade(nilai_akhir)
                print(f"\nMahasiswa dengan nilai {tipe}:")
                print(f"Nama: {mhs['nama']}")
                print(f"NIM: {mhs['NIM']}")
                print(f"Nilai Akhir: {nilai_akhir:.2f}")
                print(f"Grade: {grade}")
            else:
                print(" Data mahasiswa kosong.")
        elif pilihan == '4':
            mhs, tipe = cari_mahasiswa_extreme("rendah")
            if mhs:
                nilai_akhir = hitung_nilai_akhir(mhs)
                grade = tentukan_grade(nilai_akhir)
                print(f"\n Mahasiswa dengan nilai {tipe}:")
                print(f"Nama: {mhs['nama']}")
                print(f"NIM: {mhs['NIM']}")
                print(f"Nilai Akhir: {nilai_akhir:.2f}")
                print(f"Grade: {grade}")
            else:
                print(" Data mahasiswa kosong.")
        elif pilihan == '5':
            filter_berdasarkan_grade()
        elif pilihan == '6':
            hitung_rata_rata_kelas()
        elif pilihan == '7':
            print("\n Terima kasih telah menggunakan program ini!")
            break
        else:
            print(" Pilihan tidak valid. Silakan pilih 1-7.")

# Jalankan program
if __name__ == "__main__":
    menu_utama()