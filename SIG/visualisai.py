import pandas as pd
import folium
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
    

def baca_data_lokasi(nama_file: str) -> pd.DataFrame:
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

        if pd.isna(nama) or pd.isna(lat) or pd.isna(lon):
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
                
                objek = TempatIbadah(nama, lat, lon, agama_info, deskripsi)
                
            else:
                print(f" -> Peringatan: Tipe '{tipe}' untuk '{nama}' tidak dikenali. Tidak membuat objek spesifik")

            if objek:
                list_objek.append(objek)
                print(f" -> Objek {type(objek).__name__} untuk '{nama}' berhasil dibuat")

        except Exception as e:
            print(f" -> GAGAL membuat objek untuk '{nama}' di baris {index}: {e}")

    print(f"Total {len(list_objek)} objek berhasil dibuat dari {len(dataframe)} baris data")
    return list_objek

def peta_lokasi(list_objek: list, file_output: str = "peta_lokasi.html"):
    if not list_objek:
        print("Tidak ada objek lokasi untuk dipetakan")
        return

    print(f"\nMemulai pembuatan peta Folium dari {len(list_objek)} lokasi...")
    
    try:
        lat_tengah = list_objek[0].latitude
        lon_tengah = list_objek[0].longitude
    except IndexError: 
        lat_tengah, lon_tengah = -6.9929, 110.4200

    # PERBAIKAN 3: Menggunakan list [] untuk location, bukan set {}
    peta = folium.Map(location=[lat_tengah, lon_tengah], zoom_start=13, tiles="OpenStreetMap")
    print(f" -> Objek peta dibuat, berpusat di ({lat_tengah:.4f}, {lon_tengah:.4f})")

    jumlah_marker = 0
    for lok in list_objek:
        koordinat = lok.get_koordinat()

        if koordinat != (0.0, 0.0):
            info_popup_html = lok.get_info_popup()

            # PERBAIKAN 2: Menambahkan koma (,) di setiap akhir baris atribut marker
            folium.Marker(
                location=koordinat,
                popup=folium.Popup(info_popup_html, max_width=300),
                tooltip=lok.nama,
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(peta)
            jumlah_marker += 1
        else:
            print(f" -> Melewati marker untuk '{lok.nama}' karena koordinat tidak valid")

    try:
        peta.save(file_output)
        print(f"Total marker ditambahkan: {jumlah_marker}")
        print(f"Peta berhasil disimpan ke '{file_output}'")
    except Exception as e:
        print(f"\nERROR saat menyimpan peta Folium: {type(e).__name__} - {e}")


# --- PROGRAM UTAMA ---
if __name__ == "__main__":
    nama_file = "lokasi_semarang.csv"
    nama_peta = "peta_interaktif_semarang.html"

    print("--- Visualisasi Peta ---")

    df_lokasi = baca_data_lokasi(nama_file)
    list_objek = objek_lokasi(df_lokasi)
    peta_lokasi(list_objek, nama_peta)

    print(f"\nSilakan buka file '{nama_peta}' di browser")
    print("\n--- Selesai ---")