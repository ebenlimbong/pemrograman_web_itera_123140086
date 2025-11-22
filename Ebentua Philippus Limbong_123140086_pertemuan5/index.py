# Mengimpor ABC (Abstract Base Class) dan abstractmethod untuk membuat kelas abstrak
from abc import ABC, abstractmethod


# KELAS ABSTRACT DASAR ITEM
class ItemPerpustakaan(ABC):
    """
    Kelas abstrak yang menjadi dasar semua item perpustakaan.
    Memiliki atribut judul (protected) dan id_item (private)
    """

    def __init__(self, judul, id_item):
        self._judul = judul              # atribut protected
        self.__id_item = id_item         # atribut private

    @property
    def judul(self):
        """Menggunakan property decorator untuk mengakses judul"""
        return self._judul

    @property
    def id_item(self):
        """Menggunakan property decorator untuk mengakses ID item"""
        return self.__id_item

    @abstractmethod
    def deskripsi(self):
        """
        Method abstrak yang wajib diimplementasikan oleh semua subclass.
        Digunakan untuk menampilkan deskripsi dari setiap item.
        """
        pass


# SUBCLASS 1: Buku
class Buku(ItemPerpustakaan):
    """Subclass dari ItemPerpustakaan untuk item berupa buku."""

    def __init__(self, judul, id_item, penulis):
        # Memanggil konstruktor parent class menggunakan super()
        super().__init__(judul, id_item)
        self.penulis = penulis

    def deskripsi(self):
        """Mengimplementasikan method abstrak dari parent"""
        return f"Buku | Judul: {self.judul} | Penulis: {self.penulis} | ID: {self.id_item}"


# SUBCLASS 2: Majalah
class Majalah(ItemPerpustakaan):
    """Subclass dari ItemPerpustakaan untuk item berupa majalah."""

    def __init__(self, judul, id_item, edisi):
        super().__init__(judul, id_item)
        self.edisi = edisi

    def deskripsi(self):
        """Implementasi method abstrak (polymorphism)"""
        return f"Majalah | Judul: {self.judul} | Edisi: {self.edisi} | ID: {self.id_item}"


# SUBCLASS 3: Jurnal Ilmiah
class JurnalIlmiah(ItemPerpustakaan):
    """Subclass untuk item berupa jurnal ilmiah."""

    def __init__(self, judul, id_item, bidang_studi, tahun_terbit):
        super().__init__(judul, id_item)
        self.bidang_studi = bidang_studi
        self.tahun_terbit = tahun_terbit

    def deskripsi(self):
        """Polymorphism: menampilkan deskripsi khusus jurnal"""
        return (
            f"Jurnal Ilmiah | Judul: {self.judul} | Bidang: {self.bidang_studi} | "
            f"Tahun: {self.tahun_terbit} | ID: {self.id_item}"
        )


# SUBCLASS 4: Surat Kabar
class SuratKabar(ItemPerpustakaan):
    """Subclass untuk item berupa surat kabar."""

    def __init__(self, judul, id_item, tanggal_terbit):
        super().__init__(judul, id_item)
        self.tanggal_terbit = tanggal_terbit

    def deskripsi(self):
        """Polymorphism: deskripsi khusus surat kabar"""
        return (
            f"Surat Kabar | Judul: {self.judul} | Tanggal Terbit: {self.tanggal_terbit} | "
            f"ID: {self.id_item}"
        )


# KELAS PENGELOLA PERPUSTAKAAN
class Perpustakaan:
    """
    Class untuk mengelola koleksi item perpustakaan.
    Menyimpan daftar item, menambah item, menampilkan item, dan mencari item.
    """

    def __init__(self):
        self.koleksi = []  # menampung semua item perpustakaan

    def tambah_item(self, item):
        """Menambahkan item baru ke dalam koleksi perpustakaan"""
        self.koleksi.append(item)
        print(f"Item '{item.judul}' berhasil ditambahkan ke perpustakaan.")

    def tampilkan_item(self):
        """Menampilkan semua item yang ada di perpustakaan"""
        if not self.koleksi:
            print("Belum ada item dalam perpustakaan.")
            return

        print("Daftar Item Perpustakaan:")
        for item in self.koleksi:
            # Setiap item memanggil deskripsi() sesuai jenis objeknya (polymorphism)
            print("- " + item.deskripsi())

    def cari_item(self, kata_kunci):
        """
        Mencari item berdasarkan judul atau id item.
        kata_kunci bisa berupa string judul atau angka ID.
        """
        hasil = []
        for item in self.koleksi:
            if kata_kunci.lower() in item.judul.lower() or kata_kunci == str(item.id_item):
                hasil.append(item)
        return hasil

# BAGIAN UTAMA PROGRAM
if __name__ == "__main__":
    # Membuat objek perpustakaan
    perpustakaan = Perpustakaan()

    # Membuat berbagai item menggunakan 4 subclass
    buku1 = Buku("Pemrograman Python", 101, "Budi Santoso")
    majalah1 = Majalah("Teknologi Modern", 202, "Edisi 45")
    jurnal1 = JurnalIlmiah("Kecerdasan Buatan", 303, "Informatika", 2021)
    suratkabar1 = SuratKabar("Berita Harian", 404, "12-05-2024")

    # Menambahkan item ke perpustakaan
    perpustakaan.tambah_item(buku1)
    perpustakaan.tambah_item(majalah1)
    perpustakaan.tambah_item(jurnal1)
    perpustakaan.tambah_item(suratkabar1)

    print()
    # Menampilkan semua item
    perpustakaan.tampilkan_item()

    print()
    # Contoh pencarian
    kata = "Python"
    hasil = perpustakaan.cari_item(kata)
    print(f"Hasil pencarian '{kata}':")
    for item in hasil:
        print(item.deskripsi())
