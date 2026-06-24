import pandas as pd

file_csv = 'lokasi_semarang.csv'

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
    
if __name__ == "__main__":
    print("--- Memulai Membaca CSV ---")
    df_lokasi = baca_data_lokasi(file_csv)

    if df_lokasi is not None:
        print("\n--- Inspeksi Awal DataFrame ---")
        print("\n1. Lima Baris Pertama (head()):")
        print(df_lokasi.head())

        print("\n2. Informasi DataFrame (info()):")
        print(df_lokasi.info())

        jumlah_baris, jumlah_kolom = df_lokasi.shape
        print("\n3. Dimensi Data:")
        print(f" Jumlah Lokasi (Baris): {jumlah_baris}")
        print(f" Jumlah Atribut (Kolom): {jumlah_kolom}")

        print("\n4. Nama Kolom: ")
        print(list(df_lokasi.columns))
    else:
        print("\nTidak dapat melanjutkan inspeksi karena gagal membaca file CSV")
    
    print("\n--- Selesai Membaca CSV ---")