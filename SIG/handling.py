import pandas as pd
import folium
import datetime
import webbrowser 
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

class TempatWisata(Lokasi):
    def __init__(self, nama: str, lat: float, lon: float, jenis: str, desk: str):
        super().__init__(nama, lat, lon)
        self.jenis_wisata, self.deskripsi = jenis, desk
    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>{self.jenis_wisata}</i><br><br>{self.deskripsi}"

class Kuliner(Lokasi):
    def __init__(self, nama: str, lat: float, lon: float, desk: str):
        super().__init__(nama, lat, lon)
        self.deskripsi = desk
    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Kuliner</i><br><br>{self.deskripsi}"

class TempatIbadah(Lokasi):
    def __init__(self, nama: str, lat: float, lon: float, agama: str, desk: str):
        super().__init__(nama, lat, lon)
        self.agama, self.deskripsi = agama, desk
    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Tempat Ibadah ({self.agama})</i><br><br>{self.deskripsi}"

class Kantor(Lokasi):
    def __init__(self, nama: str, lat: float, lon: float, desk: str):
        super().__init__(nama, lat, lon)
        self.deskripsi = desk
    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Kantor Pemerintahan</i><br><br>{self.deskripsi}"

class Museum(Lokasi):
    def __init__(self, nama: str, lat: float, lon: float, desk: str):
        super().__init__(nama, lat, lon)
        self.deskripsi = desk
    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Museum</i><br><br>{self.deskripsi}"

class Taman(Lokasi):
    def __init__(self, nama: str, lat: float, lon: float, desk: str):
        super().__init__(nama, lat, lon)
        self.deskripsi = desk
    def get_info_popup(self) -> str:
        return f"<h4><b>{self.nama}</b></h4><i>Taman Kota</i><br><br>{self.deskripsi}"

def baca_data_lokasi(nama_file: str) -> pd.DataFrame:
    print(f"Mencoba membaca file CSV: {nama_file}")
    try:
        df = pd.read_csv(nama_file)
        print(" -> File CSV berhasil dibaca.")
        return df
    except Exception as e:
        print(f" -> ERROR membaca CSV: {e}")
        return None

def objek_lokasi(dataframe: pd.DataFrame) -> list:
    list_objek = []
    if dataframe is None or dataframe.empty: return list_objek
    
    print("\nMembuat objek dari DataFrame...")
    for index, row in dataframe.iterrows():
        nama = row.get('nama', None)
        lat = row.get('latitude', None)
        lon = row.get('longitude', None)
        tipe = row.get('tipe', 'Lainnya')
        desk = row.get('deskripsi', '')
        objek = None

        if pd.isna(nama) or pd.isna(lat) or pd.isna(lon): continue
            
        try:
            if 'Wisata' in tipe or tipe == 'Landmark':
                objek = TempatWisata(nama, lat, lon, tipe, desk)
            elif 'Kuliner' in tipe:
                objek = Kuliner(nama, lat, lon, desk)
            elif 'Ibadah' in tipe:
                objek = TempatIbadah(nama, lat, lon, "Umum", desk)
            elif 'Kantor' in tipe:
                objek = Kantor(nama, lat, lon, desk)
            elif 'Museum' in tipe:
                objek = Museum(nama, lat, lon, desk)
            elif 'Taman' in tipe:
                objek = Taman(nama, lat, lon, desk)

            if objek:
                list_objek.append(objek)
        except Exception as e:
            print(f" -> GAGAL membuat objek '{nama}': {e}")

    print(f"Total {len(list_objek)} objek berhasil dibuat")
    return list_objek

def tulis_log(pesan: str, file_log: str = "proses_peta.log"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(file_log, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {pesan}\n")
    except IOError: pass


def buat_peta(list_objek: list, file_output: str = "peta_lokasi.html"):
    if not list_objek: return

    lat_tengah, lon_tengah, zoom_awal = -6.9929, 110.4200, 13 
    try:
        with open("config_peta.txt", "r") as f:
            baris = f.readlines()
            lat_tengah = float(baris[0].strip())
            lon_tengah = float(baris[1].strip())
            zoom_awal = int(baris[2].strip())
        print(" -> File config_peta.txt berhasil dibaca!")
    except FileNotFoundError:
        print(" -> Peringatan: config_peta.txt tidak ditemukan. Menggunakan default Semarang.")
    except (ValueError, IndexError):
        print(" -> Peringatan: Format config_peta.txt salah. Menggunakan default Semarang.")

    peta = folium.Map(location=[lat_tengah, lon_tengah], zoom_start=zoom_awal)

    jumlah_marker = 0
    
    for lok in list_objek:
        koordinat = lok.get_koordinat()
        if koordinat != (0.0, 0.0):
            info_popup_html = lok.get_info_popup()

            warna = 'blue'
            ikon = 'info-sign'

            if isinstance(lok, TempatWisata):
                warna, ikon = 'blue', 'picture'
            elif isinstance(lok, Kuliner):
                warna, ikon = 'red', 'glass'
            elif isinstance(lok, TempatIbadah):
                warna, ikon = 'green', 'bell'
            elif isinstance(lok, Kantor):
                warna, ikon = 'gray', 'briefcase'
            elif isinstance(lok, Museum):
                warna, ikon = 'purple', 'book'
            elif isinstance(lok, Taman):
                warna, ikon = 'lightgreen', 'leaf'

            folium.Marker(
                location=koordinat, 
                popup=folium.Popup(info_popup_html, max_width=300),
                tooltip=lok.nama,
                icon=folium.Icon(color=warna, icon=ikon)
            ).add_to(peta)
            jumlah_marker += 1

    try:
        peta.save(file_output)
        tulis_log(f"Peta '{file_output}' dibuat dengan {jumlah_marker} marker.")
    except Exception as e:
        print(f" -> ERROR menyimpan peta: {e}")

if __name__ == "__main__":
    nama_file = "lokasi_semarang.csv"
    nama_peta = "peta_interaktif_semarang.html"  

    print("--- Memulai Pemrosesan Peta ---")

    df_lokasi = baca_data_lokasi(nama_file)
    list_semua = objek_lokasi(df_lokasi) 
    buat_peta(list_semua, nama_peta)

    print(f"\nProses Selesai. Membuka {nama_peta} di browser...")
    
    webbrowser.open(nama_peta)