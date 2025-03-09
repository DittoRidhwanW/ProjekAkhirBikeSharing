import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
@st.cache_data
def load_data():
    df_hour = pd.read_csv("Dashboard/bike_hour.csv")
    df_day = pd.read_csv("Dashboard/bike_day.csv")
    return df_hour, df_day

df_hour, df_day = load_data()

# Sidebar untuk navigasi
page = st.sidebar.selectbox("Pilih Halaman:", ["Analisis Data", "Get To Know!"])

if page == "Analisis Data":
    # Judul Dashboard
    st.title("Dashboard Penyewaan Sepeda")

    # --- VISUALISASI 1: Pengaruh Musim terhadap Jumlah Penyewaan ---
    st.subheader("Pengaruh Musim terhadap Jumlah Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season', y='cnt', hue='yr', data=df_hour, palette=['red', 'green'], ax=ax)
    ax.set_title('Pengaruh Musim terhadap Jumlah Penyewaan Sepeda')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)

    # --- VISUALISASI 2: Tren Penyewaan Sepeda per Bulan ---
    st.subheader("Tren Penyewaan Sepeda per Bulan")
    month_names = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    
    df_day['mnth'] = pd.Categorical(df_day['mnth'], categories=month_names, ordered=True)
    
    year_filter = st.multiselect("Pilih Tahun:", options=sorted(df_day['yr'].unique()), default=sorted(df_day['yr'].unique()))
    month_filter = st.multiselect("Pilih Bulan:", options=month_names, default=month_names)

    df_filtered = df_day[(df_day['yr'].isin(year_filter)) & (df_day['mnth'].isin(month_filter))]

    df_monthly = df_filtered.groupby(['yr', 'mnth'])[['casual', 'registered']].sum().reset_index()
    df_pivot_casual = df_monthly.pivot_table(index='mnth', columns='yr', values='casual', aggfunc='sum')
    df_pivot_registered = df_monthly.pivot_table(index='mnth', columns='yr', values='registered', aggfunc='sum')
    
    df_pivot_casual = df_pivot_casual.reindex(month_names)
    df_pivot_registered = df_pivot_registered.reindex(month_names)

    fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    for year in df_pivot_casual.columns:
        axes[0].plot(df_pivot_casual.index, df_pivot_casual[year], marker='o', linestyle='-', label=f'Tahun {year}')
    axes[0].set_title('Tren Penyewaan Casual per Bulan')
    axes[0].set_ylabel('Total Casual')
    axes[0].legend()
    axes[0].grid(True, linestyle='--', alpha=0.5)

    for year in df_pivot_registered.columns:
        axes[1].plot(df_pivot_registered.index, df_pivot_registered[year], marker='s', linestyle='-', label=f'Tahun {year}')
    axes[1].set_title('Tren Penyewaan Registered per Bulan')
    axes[1].set_xlabel('Bulan')
    axes[1].set_ylabel('Total Registered')
    axes[1].legend()
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    # --- KESIMPULAN ---
    st.subheader("Kesimpulan")
    st.markdown("""
    1. **Pengaruh Musim terhadap Penyewaan:**
       - Berdasarkan grafik, musim yang memiliki jumlah penyewaan sepeda terbanyak adalah **musim gugur (fall)**.
       - Hal ini dikarenakan cuaca pada musim gugur lebih nyaman untuk bersepeda, serta akses jalan lebih aman karena tidak licin.
    
    2. **Tren Penyewaan Sepeda per Bulan:**
       - Baik penyewaan casual maupun registered mengalami **kenaikan drastis pada bulan Agustus tahun 2012**.
       - Kenaikan ini bertepatan dengan **Olimpiade London 2012**, yang menjadi salah satu faktor meningkatnya minat masyarakat dalam bersepeda.
    """)

elif page == "Get To Know!":
    st.title("Waktu Paling Ramai Penyewaan")
    
    hourly_rental_counts = df_hour.groupby('hr')['cnt'].mean()
    hour_with_highest_rentals = hourly_rental_counts.idxmax()
      
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(hourly_rental_counts.index, hourly_rental_counts.values, marker='o', linestyle='-')
    ax.set_xlabel('Jam dalam Sehari')
    ax.set_ylabel('Rata-rata Penyewaan')
    ax.set_title('Rata-rata Penyewaan Sepeda per Jam')
    ax.set_xticks(range(0, 24))
    ax.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig)
    
    st.subheader("Tahukah Kamu!")
    st.markdown("""
        Berdasarkan grafik diatas, rata-rata banyak orang melakukan aktivitas bersepeda diantara jam 16.00 sampai jam 19.00, hal ini memberikan manfaat yaitu:
        - Dapat mengurangi stres dan meningkatkan suasana hati, aktivitas fisik ini memicu pelepasan endorfin, hormon yang dapat meningkatkan suasana hati dan mengurangi stres.
        - Meningkatkan kebugaran fisik, bersepeda secara teratur dapat membantu membakar kalori dan menjaga berat badan ideal. Aktivitas ini juga membantu memperkuat otot-otot kaki, paha, dan bokong.
        - Meningkatkan kualitas tidur, olahraga sore hari dapat membantu mengatur ritme sirkadian dan meningkatkan kualitas tidur. Aktivitas fisik dapat membuat tubuh lebih lelah secara positif, sehingga lebih mudah untuk tidur nyenyak di malam hari.
    """)
