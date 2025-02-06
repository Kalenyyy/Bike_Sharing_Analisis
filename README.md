# Analisis Data Bike Sharing

Repositori ini berisi proyek analisis data **Bike Sharing**, mencakup seluruh proses analisis data dari pengumpulan, pembersihan, eksplorasi data (EDA), hingga pembuatan dashboard interaktif menggunakan Streamlit.

## Ringkasan Proyek

Sistem penyewaan sepeda berbasis sharing menjadi solusi transportasi yang semakin populer di kota-kota besar. Proyek ini bertujuan untuk menganalisis pola penggunaan sepeda berdasarkan berbagai faktor seperti musim, kondisi cuaca, dan variabel lainnya.

Dataset yang digunakan mencatat jumlah penyewaan sepeda serta faktor lingkungan seperti suhu, kelembaban, kecepatan angin, dan kondisi cuaca.

### Tujuan utama proyek ini:
- **Menganalisis pola penggunaan sepeda berdasarkan musim (spring, summer, fall, winter).**
- **Mengetahui pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda.**
- **Mempelajari hubungan antara suhu, kelembaban, dan jumlah peminjaman sepeda.**
- **Menyediakan dashboard interaktif untuk visualisasi data.**

## Fitur Utama
- **Pembersihan Data:** Menghilangkan nilai yang hilang atau tidak valid agar data siap digunakan untuk analisis.
- **Eksplorasi Data (EDA):** Menggunakan visualisasi seperti heatmap, scatter plot, dan histogram untuk mengidentifikasi pola penggunaan sepeda.
- **Dashboard Interaktif:** Dibuat menggunakan Streamlit agar pengguna dapat menjelajahi data dengan mudah.

## Dataset

Dataset yang digunakan berisi data penyewaan sepeda berdasarkan beberapa faktor berikut:

- **cnt_hour**: Jumlah sepeda yang disewa per jam.
- **season**: Musim saat data dikumpulkan (1: Spring, 2: Summer, 3: Fall, 4: Winter).
- **weathersit**: Kondisi cuaca (1: Cerah, 2: Berawan, 3: Hujan, 4: Cuaca buruk).
- **temp**: Suhu dalam skala normalisasi.
- **hum**: Kelembaban relatif.
- **windspeed**: Kecepatan angin.
- **datetime**: Waktu pengambilan data.

## Struktur Folder
```plaintext
📂 Bike-Sharing-Analysis
├── 📂 dashboard               # Skrip dashboard Streamlit
├─────📄 dashboard.py          # Skrip utama untuk dashboard
├── 📂 data                    # Direktori berisi dataset CSV
├── 📄 notebook.ipynb          # Notebook Jupyter untuk analisis data
├── 📄 README.md               # Dokumentasi proyek ini
├── 📄 requirements.txt        # Daftar pustaka Python yang dibutuhkan               
```

## Cara Menjalankan Proyek

### Prasyarat
Pastikan Anda memiliki **Python 3.12** serta pustaka berikut:
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- streamlit
- scikit-learn
- tqdm

Instal semua dependensi menggunakan perintah berikut:
```bash
pip install -r requirements.txt
```

### Menjalankan Dashboard
1. Clone repositori ini:
```bash
git clone https://github.com/username/bike-sharing-analysis.git
cd bike-sharing-analysis
```

2. Jalankan Streamlit dashboard:
```bash
cd dashboard
streamlit run dashboard.py
```

## Temuan Utama dari Analisis

1. **Pengaruh Musim terhadap Penyewaan Sepeda:**
   - Musim panas dan gugur menunjukkan jumlah penyewaan sepeda tertinggi.
   - Musim dingin memiliki jumlah penyewaan paling sedikit, kemungkinan karena cuaca yang kurang mendukung.

2. **Pengaruh Cuaca terhadap Penyewaan:**
   - Cuaca cerah atau berawan mendukung jumlah penyewaan yang lebih tinggi.
   - Saat hujan atau cuaca buruk, jumlah penyewaan sepeda menurun drastis.

3. **Hubungan antara Suhu, Kelembaban, dan Penyewaan:**
   - Semakin tinggi suhu, semakin banyak sepeda yang disewa.
   - Kelembaban tinggi (> 80%) sedikit mengurangi jumlah penyewaan.
   - Kecepatan angin yang terlalu tinggi (> 20 km/jam) juga mengurangi minat pengguna.

Dengan adanya analisis ini, diharapkan penyedia layanan bike sharing dapat mengambil keputusan yang lebih baik dalam merencanakan operasional mereka berdasarkan pola penggunaan pengguna. 🚴‍♂️

