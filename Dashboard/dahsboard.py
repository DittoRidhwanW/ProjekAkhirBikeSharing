import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data Bike Hour
file_Hour = "D:\\DBS\\Bike Sharing Dataset\\Dashboard\\bike_hour.csv"
df_hour = pd.read_csv(file_Hour)

# Load data Bike Day
file_Day = "D:\\DBS\\Bike Sharing Dataset\\Dashboard\\bike_day.csv"
df_day = pd.read_csv(file_Day)

# Sidebar menu
st.sidebar.title("Menu")
menu = st.sidebar.radio("Pilih Analisis", ["Pengaruh Musim", "Tren Penyewaan per Bulan"])

if menu == "Pengaruh Musim":
    st.title("Analisis Penyewaan Sepeda Terhadap Musim")
    st.header("Pengaruh Musim terhadap Jumlah Penyewaan Sepeda")

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='season', y='cnt', hue='yr', data=df_hour, palette=['red', 'green'], ax=ax)
    ax.set_title('Pengaruh Musim terhadap Jumlah Penyewaan Sepeda')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)

    # Conclusion
    st.subheader("Kesimpulan")
    st.write("Berdasarkan grafik, baik pada tahun 2011 dan 2012 musim yang paling berpengaruh pada tingginya penyewaan sepeda ada di musim fall (gugur) diikuti dengan musim spring (semi), ini dikarenakan pada musim gugur cuacanya lebih nyaman dan juga akses jalannya tidak licin dan aman.")

elif menu == "Tren Penyewaan per Bulan":
    st.title("Tren Penyewaan Sepeda per Bulan")
    st.header("Grafik Penyewaan Sepeda per Bulan (Casual & Registered)")

    # Pilihan Tahun
    available_years = df_day['yr'].unique()
    selected_years = st.multiselect("Pilih Tahun", available_years, default=available_years)

    # Pilihan Rentang Bulan
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_map = {name: idx+1 for idx, name in enumerate(month_names)}

    start_month, end_month = st.select_slider("Pilih Rentang Bulan", options=month_names, value=(month_names[0], month_names[-1]))

    # Mengelompokkan data berdasarkan tahun dan bulan, lalu menjumlahkan penyewaan
    df_monthly = df_day.groupby(['yr', 'mnth'])[['casual', 'registered']].sum().reset_index()
    df_monthly['mnth_name'] = df_monthly['mnth'].apply(lambda x: month_names[x-1])

    # Konversi rentang bulan ke angka agar bisa difilter
    start_month_num, end_month_num = month_map[start_month], month_map[end_month]

    # Filter data berdasarkan tahun dan bulan yang dipilih
    df_filtered = df_monthly[df_monthly['yr'].isin(selected_years)]
    df_filtered = df_filtered[(df_filtered['mnth'] >= start_month_num) & (df_filtered['mnth'] <= end_month_num)]

    if df_filtered.empty:
        st.warning("Data tidak tersedia untuk pilihan tahun dan rentang bulan yang dipilih.")
    else:
        df_pivot_casual = df_filtered.pivot_table(index='mnth_name', columns='yr', values='casual', aggfunc='sum')
        df_pivot_registered = df_filtered.pivot_table(index='mnth_name', columns='yr', values='registered', aggfunc='sum')

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

        st.pyplot(fig)

    st.subheader("Kesimpulan")
    st.write("Dari kedua grafik tersebut baik penyewaan secara casual ataupun registered di tahun 2011 memiliki kenaikan secara bertahap mulai dari bulan Januari sampai bulan Juni. Sedangkan di tahun 2012 mengalami kenaikan drastis mulai dari bulan Juni sampai bulan Agustus. Hal ini bertepatan juga dengan adanya kompetisi bersepeda pada Olimpiade 2012 di London, dimana hal itu menjadi salah satu penyebab banyaknya minat dalam bersepeda.")
