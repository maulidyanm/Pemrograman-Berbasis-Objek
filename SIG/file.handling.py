import pandas as pd
import folium
import datetime
import time
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

def tulis_log(pesan: str, file_log: str = "proses_peta.log"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(file_log, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {pesan}\n")
    except IOError as e:
        print(f"ERROR: Gagal menulis ke file log '{file_log}': {e}")

def buat_peta(list_objek: list, file_output: str = "peta_lokasi.html"):
    nama_fungsi = "buat_peta"

    if not list_objek:
        pesan_log = f"[{nama_fungsi}] Gagal: Tidak ada data lokasi untuk dipetakan"
        print(pesan_log)
        tulis_log(pesan_log)
        return
    
    # PERBAIKAN 3: Perbaiki indentasi agar kode ini dieksekusi
    print(f"\n[{nama_fungsi}] memulai pembuatan peta dari {len(list_objek)} lokasi...")
    tulis_log(f"[{nama_fungsi}] memulai pembuatan peta '{file_output}' dengan {len(list_objek)} lokasi")

    try:
        lat_tengah = list_objek[0].latitude
        lon_tengah = list_objek[0].longitude # PERBAIKAN 4: Typo 'longtitude'
    except IndexError:
        lat_tengah, lon_tengah = -6.9929, 110.4200
        
    # PERBAIKAN 3: Keluarkan dari blok 'except' agar peta tetap dibuat meskipun tidak terjadi error!
    peta = folium.Map(location=[lat_tengah, lon_tengah], zoom_start=12)

    jumlah_marker = 0
    lokasi_dilewati = []
    
    for lok in list_objek:
        koordinat = lok.get_koordinat()
        if koordinat != (0.0, 0.0):
            info_popup_html = lok.get_info_popup()
            # PERBAIKAN 5: Tooltip dimasukkan ke marker, bukan popup
            folium.Marker(
                location=koordinat, 
                popup=folium.Popup(info_popup_html, max_width=300),
                tooltip=lok.nama
            ).add_to(peta)
            jumlah_marker += 1
        else:
            lokasi_dilewati.append(lok.nama)

    if lokasi_dilewati:
        pesan_lewat = f"[{nama_fungsi}] melewati marker untuk: {','.join(lokasi_dilewati)} (koordinat tidak valid)"
        print(f" -> Peringatan: {pesan_lewat}")
        tulis_log(pesan_lewat)

    try:
        peta.save(file_output)
        pesan_sukses = f"[{nama_fungsi}] Peta '{file_output}' berhasil dibuat dengan {jumlah_marker} marker"
        print(f" -> {pesan_sukses}")
        tulis_log(pesan_sukses)
    except Exception as e:
        pesan_error = f"[{nama_fungsi}] ERROR saat menyimpan peta '{file_output}': {type(e).__name__} - {e}"
        print(f" -> {pesan_error}")
        tulis_log(pesan_error)

# --- PROGRAM UTAMA ---
if __name__ == "__main__":
    nama_file = "lokasi_semarang.csv"
    nama_peta = "peta_interaktif_semarang.html"  
    file_log = "proses_peta.log"

    print("--- File Handling & OOP ---")

    df_lokasi = baca_data_lokasi(nama_file)
    list_semua = objek_lokasi(df_lokasi) 
    buat_peta(list_semua, nama_peta)

    print(f"\nSilakan periksa isi file log '{file_log}' untuk melihat catatan")
    print("\n--- Selesai ---")