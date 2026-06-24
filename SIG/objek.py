import pandas as pd
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
    
# file_csv = 'lokasi_semarang.csv'

def baca_data_lokasi(nama_file : str) -> pd.DataFrame:

    print(f"Mencoba membaca file CSV: {nama_file}")
    try:
        dataframe = pd.read_csv(nama_file)
        print(" -> File CSV berhasil dibaca.")
        return dataframe
    except FileNotFoundError:
        print(f" -> ERROR: File '{nama_file}' tidak ditemukan")
        return None
    except pd.errors.EmptyDataError:
        print(f" -> ERROR: File '{nama_file}' kosong")
        return None
    except Exception as e:
        print(f" -> ERROR: Terjadi kesalahan saat membaca file: {type(e).__name__} - {e}")
        return None
    
def objek_lokasi(dataframe: pd.DataFrame) -> list:
    list_objek = []
    if dataframe is None or dataframe.empty:
        print(" -> DataFrame kosong atau tidak valid. Tidak ada objek yang dibuat")
        return list_objek
    
    print("\nMembuat objek dari DataFrame...")
    for index, row in dataframe.iterrows():
        nama = row.get('nama', None)
        lat = row.get('latitude', None)
        lon = row.get('longitude', None)
        tipe = row.get('tipe', 'Lainnya')
        deskripsi = row.get('deskripsi', '')
        objek = None

        if nama is None or lat is None or lon is None:
            print(f" -> Melewati baris {index}: Data Nama/Latitude/Longitude tidak lengkap")
            continue
        try:
            if 'Wisata' in tipe or tipe == 'Landmark':
                objek = TempatWisata(nama, lat, lon, tipe, deskripsi)
            elif tipe == 'Kuliner':
                objek = Kuliner(nama, lat, lon, deskripsi)
            elif 'Ibadah' in tipe:
                agama_info = "Umum"
                if "Islam" in tipe: agama_info = "Islam"
                elif "Kristen" in tipe: agama_info = "Kristen"
                elif "Hindu" in tipe: agama_info = "Hindu"
                elif "Buddha" in tipe: agama_info = "Buddha"
            else:
                print(f" -> Peringatan: Tipe '{tipe}' untuk '{nama}' tidak dikenali. Tidak membuat objek spesifik")

            if objek:
                list_objek.append(objek)
                print(f" -> Objek {type(objek).__name__} untuk '{nama}' berhasil dibuat")

        except Exception as e:
            print(f" -> GAGAL membuat objek untuk '{nama}' di baris {index}: {e}")

    print(f"Total {len(list_objek)} objek berhasil dibuat dari {len(dataframe)} baris data")
    return list_objek

if __name__ == "__main__":
    file_name = 'lokasi_semarang.csv'
    print("--- Memulai membuat objek ---")

    df_lokasi = baca_data_lokasi(file_name)
    
    list_lokasi = objek_lokasi(df_lokasi)
    
    if list_lokasi:
        for idx, lok in enumerate(list_lokasi):
            print(f"{idx+1}. {repr(lok)}")
    else:
        print("Tidak ada objek lokasi yan dibuat")

    print("\n--- Selesai ---")