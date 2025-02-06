import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

# Fungsi 
hour_df = pd.read_csv('data/hour.csv')
day_df = pd.read_csv('data/day.csv')

# Merge berdasarkan dteday
merged_df = hour_df.merge(day_df[['dteday', 'cnt']], on='dteday', suffixes=('_hour', '_day'))

# Mengubah tipedata dteday object menjadi datetime
merged_df['dteday'] = pd.to_datetime(merged_df['dteday'])

# Fungsi untuk mengecek outliers
def remove_outliers(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    initial_count = len(df)
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    
    return df  # Mengembalikan DataFrame yang sudah bersih

merged_df = remove_outliers(merged_df)  


# Sidebar
st.sidebar.title("Menu Navigasi")
menu = st.sidebar.selectbox("Pilih Menu:", ["Home", "Lihat Dataset", "Pertanyaan Satu", "Pertanyaan Dua", "Pertanyaan Tiga", "Binning", "Kesimpulan"])

# Halaman Home
if menu == "Home":
    st.title('Proyek Analisis Data: Bike Sharing Dataset')
    st.markdown("""
    **Pertanyaan Bisnis:** \n
    1. Bagaimana prediksi jumlah total penyewaan sepeda (casual dan registered) pada hari tertentu berdasarkan musim, cuaca, dan suhu?
    2. Apakah hari kerja (workingday) memiliki dampak signifikan terhadap jumlah penyewaan sepeda?
    3. Apakah suhu (temp) atau kelembapan (hum) memiliki hubungan signifikan dengan jumlah penyewaan sepeda?
    """)
    st.subheader("Deskripsi Data")
    st.write(merged_df.describe())
    st.subheader("Dataframe")
    st.dataframe(merged_df.head())
    
# Halaman Lihat Dataset
elif menu == "Lihat Dataset":
    st.title("Lihat Dataset")
    st.dataframe(merged_df.head())
    
# Pertanyaan Satu: Bagaimana prediksi jumlah total penyewaan sepeda (casual dan registered) pada hari tertentu berdasarkan musim, cuaca, dan suhu?
elif menu == "Pertanyaan Satu":
    st.title("Bagaimana prediksi jumlah total penyewaan sepeda (casual dan registered) pada hari tertentu berdasarkan musim, cuaca, dan suhu?")
    
    # Mapping season ke bentuk teks
    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    merged_df["season"] = merged_df["season"].map(season_mapping)

    # Mapping weathersit ke bentuk teks
    weather_mapping = {
        1: "Clear/Partly Cloudy",
        2: "Mist/Cloudy",
        3: "Light Snow/Rain"
    }
    merged_df["weathersit"] = merged_df["weathersit"].map(weather_mapping)
    
    # Rata-rata penyewaan berdasarkan musim
    season_avg = merged_df.groupby("season")["cnt_hour"].mean().reset_index()
    season_avg.columns = ["Season", "Avg Rentals"]
    
    # Rata-rata penyewaan berdasarkan cuaca
    weather_avg = merged_df.groupby("weathersit")["cnt_hour"].mean().reset_index()
    weather_avg.columns = ["Weather", "Avg Rentals"]

    # Rata-rata penyewaan berdasarkan kategori suhu
    merged_df["temp_category"] = pd.cut(merged_df["temp"], bins=[0, 0.25, 0.5, 0.75, 1], labels=["Very Cold", "Cold", "Warm", "Hot"])
    temp_avg = merged_df.groupby("temp_category")["cnt_hour"].mean().reset_index()
    temp_avg.columns = ["Temperature Category", "Avg Rentals"]

    # Tampilkan tabel hasil rata-rata
    st.subheader("Rata-rata Penyewaan Berdasarkan Musim")
    st.table(season_avg)

    st.subheader("Rata-rata Penyewaan Berdasarkan Cuaca")
    st.table(weather_avg)

    st.subheader("Rata-rata Penyewaan Berdasarkan Kategori Suhu")
    st.table(temp_avg)

    # Visualisasi rata-rata penyewaan berdasarkan musim
    st.subheader("Grafik Rata-rata Penyewaan Berdasarkan Musim")
    plt.figure(figsize=(8, 5))
    sns.barplot(x="Season", y="Avg Rentals", data=season_avg, palette="coolwarm")
    plt.xlabel("Musim")
    plt.ylabel("Jumlah Penyewaan Rata-rata")
    st.pyplot(plt)

    # Visualisasi rata-rata penyewaan berdasarkan cuaca
    st.subheader("Grafik Rata-rata Penyewaan Berdasarkan Cuaca")
    plt.figure(figsize=(8, 5))
    sns.barplot(x="Weather", y="Avg Rentals", data=weather_avg, palette="viridis")
    plt.xlabel("Cuaca")
    plt.ylabel("Jumlah Penyewaan Rata-rata")
    st.pyplot(plt)

    # Visualisasi rata-rata penyewaan berdasarkan kategori suhu
    st.subheader("Grafik Rata-rata Penyewaan Berdasarkan Kategori Suhu")
    plt.figure(figsize=(8, 5))
    sns.barplot(x="Temperature Category", y="Avg Rentals", data=temp_avg, palette="plasma")
    plt.xlabel("Kategori Suhu")
    plt.ylabel("Jumlah Penyewaan Rata-rata")
    st.pyplot(plt)

    # Penjelasan
    st.markdown("""
    ### Rata-rata Penyewaan Berdasarkan Musim
    - **Fall (Musim Gugur)**: Penyewaan tertinggi dengan rata-rata 170.32 penyewaan per hari.
    - **Winter (Musim Dingin)**: Rata-rata 152.75 penyewaan per hari, sedikit lebih rendah dari musim gugur.
    - **Summer (Musim Panas)**: Rata-rata 147.89 penyewaan per hari, sedikit lebih rendah dibandingkan musim gugur dan musim dingin.
    - **Spring (Musim Semi)**: Penyewaan terendah dengan rata-rata 98.54 penyewaan per hari.

    ### Rata-rata Penyewaan Berdasarkan Cuaca
    - **Clear/Partly Cloudy (Jernih/Separa Berawan)**: Penyewaan tertinggi dengan rata-rata 149.04 penyewaan per hari.
    - **Light Snow/Rain (Salju/Hujan Ringan)**: Penyewaan terendah dengan rata-rata 94.33 penyewaan per hari.
    - **Mist/Cloudy (Kabut/Berawan)**: Rata-rata 140.57 penyewaan per hari.

    ### Rata-rata Penyewaan Berdasarkan Kategori Suhu
    - **Very Cold (Suhu Sangat Dingin)**: Penyewaan terendah dengan rata-rata 65.49 penyewaan per hari.
    - **Cold (Suhu Dingin)**: Rata-rata 126.53 penyewaan per hari.
    - **Warm (Suhu Hangat)**: Rata-rata 164.85 penyewaan per hari.
    - **Hot (Suhu Panas)**: Penyewaan tertinggi dengan rata-rata 242.09 penyewaan per hari.

    ### Kesimpulan
    Penyewaan sepeda lebih tinggi pada musim gugur, cuaca cerah, dan suhu panas, sementara lebih rendah pada musim semi, cuaca berawan, dan suhu sangat dingin.
    """)
    
# Pertanyaan Dua: Apakah hari kerja (workingday) memiliki dampak signifikan terhadap jumlah penyewaan sepeda?
elif menu == "Pertanyaan Dua":
    st.title("Apakah hari kerja (workingday) memiliki dampak signifikan terhadap jumlah penyewaan sepeda?")

    # Analisis rata-rata jumlah penyewaan berdasarkan hari kerja dan hari libur
    avg_rentals_workingday = merged_df[merged_df['workingday'] == 1]['cnt_hour'].mean()
    avg_rentals_holiday = merged_df[merged_df['workingday'] == 0]['cnt_hour'].mean()

    # Hitung selisih
    difference = avg_rentals_workingday - avg_rentals_holiday

    # Tampilkan hasil analisis dalam bentuk tabel
    analysis_result = [
        ["Hari Kerja", avg_rentals_workingday],
        ["Hari Libur", avg_rentals_holiday],
        ["Selisih", difference]
    ]

    # Ubah menjadi DataFrame untuk streamlit
    analysis_df = pd.DataFrame(analysis_result, columns=["Kategori", "Rata-rata Penyewaan"])

    # Tampilkan tabel hasil analisis
    st.subheader("Hasil Analisis Rata-rata Penyewaan")
    st.table(analysis_df)

    # Visualisasi jumlah penyewaan sepeda berdasarkan hari kerja dan hari libur
    st.subheader("Grafik Perbandingan Penyewaan Sepeda pada Hari Kerja vs Hari Libur")
    plt.figure(figsize=(8, 5))
    sns.barplot(x=['Hari Kerja', 'Hari Libur'], y=[avg_rentals_workingday, avg_rentals_holiday], palette=['blue', 'red'])
    plt.xlabel('Kategori')
    plt.ylabel('Rata-rata Penyewaan Sepeda')
    plt.title('Perbandingan Penyewaan Sepeda pada Hari Kerja vs Hari Libur')
    st.pyplot(plt)

    # Penjelasan
    st.markdown("""
    ### Penjelasan Hasil Analisis Rata-rata Penyewaan

    Berdasarkan hasil analisis rata-rata jumlah penyewaan sepeda, didapatkan perbandingan antara hari kerja dan hari libur sebagai berikut:

    - **Hari Kerja**: Rata-rata penyewaan sepeda pada hari kerja adalah **152.22**.
    - **Hari Libur**: Rata-rata penyewaan sepeda pada hari libur adalah **114.18**.
    - **Selisih**: Terdapat selisih **38.03** antara jumlah penyewaan pada hari kerja dan hari libur.

    **Interpretasi**:
    - Hasil ini menunjukkan bahwa pada **hari kerja**, jumlah penyewaan sepeda cenderung lebih tinggi dibandingkan pada **hari libur**. Hal ini dapat disebabkan oleh lebih banyak orang yang menggunakan sepeda untuk aktivitas sehari-hari, seperti bekerja atau berpergian.
    - Selisih yang signifikan ini menunjukkan bahwa hari kerja mempengaruhi perilaku penyewaan sepeda secara positif, mungkin karena adanya kebutuhan yang lebih tinggi akan transportasi.

    Dengan demikian, kita bisa menyimpulkan bahwa **hari kerja** memberikan dampak yang lebih besar terhadap **jumlah penyewaan sepeda** dibandingkan dengan **hari libur**.
    """)
    
# Pertanyaan Tiga: Apakah suhu (temp) atau kelembapan (hum) memiliki hubungan signifikan dengan jumlah penyewaan sepeda?
elif menu == "Pertanyaan Tiga":
    st.title("Apakah suhu (temp) atau kelembapan (hum) memiliki hubungan signifikan dengan jumlah penyewaan sepeda?")

    # Menghitung korelasi Pearson
    corr_temp, _ = pearsonr(merged_df['temp'], merged_df['cnt_hour'])
    corr_hum, _ = pearsonr(merged_df['hum'], merged_df['cnt_hour'])

    # Menampilkan hasil analisis dalam bentuk tabel
    analysis_result = [
        ["Suhu (temp)", corr_temp],
        ["Kelembapan (hum)", corr_hum]
    ]
    
    # Ubah menjadi DataFrame untuk streamlit
    analysis_df = pd.DataFrame(analysis_result, columns=["Variabel", "Korelasi dengan Penyewaan"])
    
    st.subheader("Hasil Analisis Korelasi")
    st.table(analysis_df)
    
    # Penjelasan
    st.markdown(f"""
    ### Penjelasan Hasil Korelasi

    Berdasarkan perhitungan korelasi antara suhu (temp) dan kelembapan (hum) dengan jumlah penyewaan sepeda (cnt_hour), hasil yang didapat adalah sebagai berikut:

    - **Korelasi Suhu (temp) dengan Penyewaan**: Nilai korelasi adalah **{corr_temp:.2f}**.
    - **Korelasi Kelembapan (hum) dengan Penyewaan**: Nilai korelasi adalah **{corr_hum:.2f}**.

    **Interpretasi**:
    - Nilai korelasi **{corr_temp:.2f}** menunjukkan bahwa suhu memiliki **hubungan yang {('positif' if corr_temp > 0 else 'negatif')}** dengan jumlah penyewaan sepeda. Artinya, jika suhu meningkat, jumlah penyewaan sepeda cenderung meningkat (atau menurun jika negatif).
    - Nilai korelasi **{corr_hum:.2f}** menunjukkan bahwa kelembapan juga memiliki **hubungan yang {('positif' if corr_hum > 0 else 'negatif')}** dengan jumlah penyewaan sepeda. Jika nilai korelasi positif, artinya semakin tinggi kelembapan, semakin tinggi pula jumlah penyewaan sepeda.

    #### Visualisasi Hubungan Suhu dan Kelembapan dengan Penyewaan
    Untuk visualisasi, berikut adalah scatter plot yang menunjukkan hubungan suhu dan kelembapan dengan jumlah penyewaan sepeda:

    """)
    
    # Visualisasi hubungan suhu vs penyewaan
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Scatter plot suhu vs penyewaan
    sns.scatterplot(x=merged_df['temp'], y=merged_df['cnt_hour'], alpha=0.5, color='blue', ax=axes[0])
    axes[0].set_xlabel('Suhu (temp)')
    axes[0].set_ylabel('Jumlah Penyewaan Sepeda')
    axes[0].set_title(f'Korelasi Suhu vs Penyewaan (r = {corr_temp:.2f})')

    # Scatter plot kelembapan vs penyewaan
    sns.scatterplot(x=merged_df['hum'], y=merged_df['cnt_hour'], alpha=0.5, color='red', ax=axes[1])
    axes[1].set_xlabel('Kelembapan (hum)')
    axes[1].set_ylabel('Jumlah Penyewaan Sepeda')
    axes[1].set_title(f'Korelasi Kelembapan vs Penyewaan (r = {corr_hum:.2f})')

    plt.tight_layout()
    st.pyplot(fig)
    
# Halaman Binning
elif menu == "Binning":
    st.title("Analisis Clustering Lanjutan - Binning")

    # Fungsi untuk mengategorikan waktu
    def categorize_time(hour):
        if 0 <= hour < 6:
            return 'Morning'
        elif 6 <= hour < 12:
            return 'Afternoon'
        elif 12 <= hour < 18:
            return 'Evening'
        else:
            return 'Night'

    # Pastikan merged_df sudah ada sebelumnya, dan buat kolom baru untuk kategori waktu
    merged_df['daypart'] = merged_df['hr'].apply(categorize_time)

    # Hitung total penyewaan berdasarkan kategori waktu
    daypart_counts = merged_df.groupby('daypart')['cnt_hour'].sum().reset_index()

    # Urutkan kategori waktu agar sesuai dengan urutan logis
    daypart_counts['daypart'] = pd.Categorical(daypart_counts['daypart'], 
                                                categories=['Morning', 'Afternoon', 'Evening', 'Night'],
                                                ordered=True)
    daypart_counts = daypart_counts.sort_values('daypart')

    # Menampilkan penjelasan menggunakan st.markdown
    st.markdown("""
    ### Analisis Penyewaan Sepeda Berdasarkan Waktu dalam Sehari

    Pada analisis ini, kita akan membahas total penyewaan sepeda berdasarkan waktu dalam sehari, yang dikelompokkan menjadi empat kategori waktu utama: **Pagi (Morning)**, **Siang (Afternoon)**, **Sore (Evening)**, dan **Malam (Night)**. 

    #### Kategori Waktu:
    - **Morning (00:00 - 06:00)**: Periode waktu dini hari hingga pagi hari.
    - **Afternoon (06:00 - 12:00)**: Periode waktu dari pagi hingga siang hari.
    - **Evening (12:00 - 18:00)**: Periode waktu sore hingga menjelang malam.
    - **Night (18:00 - 00:00)**: Periode waktu malam hingga tengah malam.

    #### Langkah Analisis:
    1. **Pengelompokan Waktu**: Data penyewaan sepeda dikelompokkan berdasarkan jam dalam sehari, kemudian dikelompokkan lagi menjadi kategori waktu yang lebih besar.
    2. **Perhitungan Total Penyewaan**: Setelah pengelompokan, total penyewaan sepeda dihitung untuk masing-masing kategori waktu.
    3. **Hasil**: Hasil analisis menunjukkan bagaimana penyewaan sepeda berbeda pada berbagai waktu dalam sehari, yang dapat memberikan wawasan mengenai pola permintaan berdasarkan waktu.

    #### Tabel Hasil Analisis
    """)
    # Menampilkan hasil tabel di Streamlit
    st.subheader("Total Penyewaan Berdasarkan Kategori Waktu")
    st.table(daypart_counts)

    st.markdown("""
    #### Visualisasi Penyewaan Sepeda Berdasarkan Waktu
    Berikut adalah grafik yang menggambarkan jumlah penyewaan sepeda berdasarkan waktu dalam sehari. Grafik ini membantu kita memahami pola penyewaan pada berbagai waktu sepanjang hari.

    Grafik ini menunjukkan:
    - **Waktu Pagi (Morning)** memiliki penyewaan yang relatif lebih sedikit dibandingkan dengan waktu lainnya.
    - **Waktu Sore (Evening)** dan **Malam (Night)** memiliki jumlah penyewaan yang lebih tinggi, menunjukkan bahwa permintaan sepeda meningkat pada waktu tersebut.

    """)

    # Visualisasi data
    st.subheader("Grafik Penyewaan Sepeda Berdasarkan Waktu")
    plt.figure(figsize=(8,5))
    plt.bar(daypart_counts['daypart'], daypart_counts['cnt_hour'], color=['blue', 'orange', 'green', 'red'])
    plt.xlabel('Time of Day')
    plt.ylabel('Total Bike Rentals')
    plt.title('Bike Rentals by Time of Day')

    # Tampilkan grafik di Streamlit
    st.pyplot(plt)

    
# Kesimpulan
elif menu == "Kesimpulan":
    st.title("Kesimpulan")
    
    # Kesimpulan analisis
    st.markdown("""
    ### Kesimpulan Analisis Penyewaan Sepeda

    Berdasarkan analisis terhadap data penyewaan sepeda, ditemukan beberapa pola yang dapat memberikan wawasan bagi pengelola layanan penyewaan sepeda untuk mengoptimalkan layanan mereka. Berikut adalah beberapa kesimpulan utama:

    #### 1. **Pengaruh Musim terhadap Penyewaan**
    Penyewaan sepeda mengalami fluktuasi yang signifikan berdasarkan musim. Jumlah penyewaan cenderung lebih tinggi pada musim tertentu, seperti musim **gugur**, dibandingkan dengan musim **semi**. Hal ini menunjukkan bahwa faktor **cuaca** memiliki peran penting dalam keputusan pengguna untuk menyewa sepeda. Oleh karena itu, pengelola layanan penyewaan sepeda perlu mempertimbangkan faktor musim dalam strategi pemasaran dan perencanaan armada sepeda.

    #### 2. **Dampak Kondisi Cuaca**
    Kondisi cuaca memiliki dampak yang signifikan terhadap jumlah penyewaan sepeda. **Cuaca cerah** dan **berawan** mendukung peningkatan jumlah penyewaan sepeda. Sebaliknya, **cuaca ekstrem** seperti **hujan lebat** atau **badai** menyebabkan penurunan signifikan dalam penyewaan. Oleh karena itu, **prediksi cuaca** dapat digunakan sebagai alat untuk **mengantisipasi permintaan sepeda** pada hari tertentu dan menyesuaikan ketersediaan sepeda sesuai dengan kondisi cuaca.

    #### 3. **Hari Kerja vs. Akhir Pekan**
    Pada hari kerja, penyewaan sepeda cenderung lebih tinggi di **pagi** dan **sore hari**, yang mencerminkan pola perjalanan komuter yang tinggi. Di sisi lain, pada akhir pekan, jumlah penyewaan meningkat secara merata sepanjang hari, mengindikasikan bahwa penggunaan sepeda lebih banyak dilakukan untuk tujuan **rekreasi**. Pengelola layanan penyewaan sepeda dapat memanfaatkan data ini untuk **menyusun jadwal pengelolaan armada sepeda** dan mempromosikan sepeda pada waktu-waktu yang tepat sesuai dengan pola penggunaan.

    Dengan mempertimbangkan hasil analisis ini, pengelola dapat **mengoptimalkan penggunaan sepeda**, **memprediksi permintaan**, dan **menyediakan layanan yang lebih efisien** untuk pelanggan.
    """)
