from abc import ABC, abstractmethod

class Lokasi(ABC):
    def __init__(self, nama: str, latitude: float, longitude: float):
        self.nama = str(nama) if nama else "Tanpa Nama"
        try:
            self.latitude = float(latitude)
            self.longitude = float(longitude)
        except (ValueError, TypeError):
            self.latitude = 0.0
            self.longitude = 0.0

    def get_koordinat(self) -> tuple:
        return (self.latitude, self.longitude)

    @abstractmethod
    def get_info_popup(self) -> str:
        pass

    def __repr__(self) -> str:
        return f"{type(self).__name__}(nama='{self.nama}', lat={self.latitude:.4f}, lon={self.longitude:.4f})"

class TempatWisata(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, jenis: str, deskripsi: str):
        super().__init__(nama, latitude, longitude)
        self.jenis_wisata = str(jenis) if jenis else "Umum"
        self.deskripsi = str(deskripsi) if deskripsi else "Tidak ada deskripsi."

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>{self.jenis_wisata}</i><br><br>{self.deskripsi}"


class Kuliner(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, deskripsi: str):
        super().__init__(nama, latitude, longitude)
        self.deskripsi = str(deskripsi) if deskripsi else "Tempat Kuliner"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Kuliner</i><br><br>{self.deskripsi}"


class TempatIbadah(Lokasi):
    def __init__(self, nama: str, latitude: float, longitude: float, agama: str, deskripsi: str):
        super().__init__(nama, latitude, longitude)
        self.agama = str(agama) if agama else "Umum"
        self.deskripsi = str(deskripsi) if deskripsi else "Tempat Ibadah"

    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Tempat Ibadah ({self.agama})</i><br><br>{self.deskripsi}"


if __name__ == "__main__":
    print("--- Struktur Kelas OOP ---")
    
    lokasi_wisata = TempatWisata("Lawang Sewu", -6.9840, 110.4105, "Wisata Sejarah", "Bangunan kuno peninggalan Belanda.")
    lokasi_kuliner = Kuliner("Lumpia Gang Lombok", -6.9718, 110.4255, "Lumpia legendaris di Semarang.")
    lokasi_ibadah = TempatIbadah("Masjid Agung JAwa Tengah", -6.9892, 110.4452, "Islam", "Masjid dengan payung raksasa.")
    
    daftar_tempat = [lokasi_wisata, lokasi_kuliner, lokasi_ibadah]
    
    for tempat in daftar_tempat:
        print("\n" + "="*40)
        print(f"Representasi Objek : {tempat}")
        print(f"Nama Tempat        : {tempat.nama}")
        print(f"Koordinat Geografis: {tempat.get_koordinat()}")
        print(f"Format HTML Popup  : {tempat.get_info_popup()}")
        
    print("\n--- Pengujian Struktur Kelas Selesai dan Berhasil ---")