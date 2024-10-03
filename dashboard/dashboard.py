import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set style untuk seaborn
sns.set(style='dark')

def create_daily_users_df(df):
    # Mengonversi kolom 'dteday' menjadi datetime 
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Mengelompokkan data per hari dan menghitung jumlah pengguna casual dan registered
    daily_users_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered": "sum"
    })
    
    # Mengatur index menjadi kolom biasa dan mengganti nama kolom
    daily_users_df = daily_users_df.reset_index()
    daily_users_df.rename(columns={
        "casual": "casual_users",
        "registered": "registered_users"
    }, inplace=True)
    
    return daily_users_df

# Load data
hour_df = pd.read_csv("all_data.csv")


# Membuat header
st.header('Bike Sharing :sparkles:')

# Mengubah kolom 'dteday' menjadi datetime
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Komponen filter
min_date = hour_df["dteday"].min().date()
max_date = hour_df["dteday"].max().date()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("bike.png")
    
    # Mengambil rentang tanggal dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)  # Pastikan ini adalah tuple dengan dua tanggal
    )

    # Menambahkan filter untuk jam
    min_hour = 0
    max_hour = 23
    start_hour = st.slider(
        label='Jam Mulai',
        min_value=min_hour,
        max_value=max_hour,
        value=(min_hour, max_hour)  # Pastikan ini adalah tuple dengan dua jam
    )

# Filter DataFrame berdasarkan tanggal dan jam yang dipilih
filtered_df = hour_df[
    (hour_df['dteday'].dt.date >= start_date) & 
    (hour_df['dteday'].dt.date <= end_date) &
    (hour_df['dteday'].dt.hour >= start_hour[0]) & 
    (hour_df['dteday'].dt.hour <= start_hour[1])
]

# Menampilkan DataFrame yang sudah difilter
st.write("Data Sepeda yang difilter:")
st.dataframe(filtered_df)

# Jumlah pengguna terdaftar
st.subheader('Users')

# Menghitung pengguna per hari
daily_users_df = create_daily_users_df(filtered_df)

# Streamlit layout
col1, col2 = st.columns(2)

with col1:
    total_casual_users = daily_users_df["casual_users"].sum()  # Mengakses kolom yang benar
    st.metric("Total Casual Users", value=total_casual_users)

with col2:
    total_registered_users = daily_users_df["registered_users"].sum()  # Mengakses kolom yang benar
    st.metric("Total Registered Users", value=total_registered_users)


# Membuat DataFrame
hour_df = pd.DataFrame(hour_df)  # Ganti ini dengan data Anda

# Menghitung total penyewa per jam
bike_per_hour = hour_df.groupby('hr')['cnt'].sum().reset_index()

# Mengurutkan DataFrame berdasarkan jumlah pengguna (cnt) dari yang paling banyak ke paling sedikit
sorted_bike_per_hour = bike_per_hour.sort_values(by='cnt', ascending=False).reset_index(drop=True)


# Membuat bar chart
fig, ax = plt.subplots(figsize=(12, 6))

# Bar chart
sns.barplot(x=sorted_bike_per_hour['hr'], y=sorted_bike_per_hour['cnt'], ax=ax, color='b')

# Menambahkan judul dan label
ax.set_title('Total Penyewa di tiap Jam', fontsize=16)
ax.set_xlabel('Jam', fontsize=14)
ax.set_ylabel('Jumlah Penyewa', fontsize=14)
ax.tick_params(axis='x', rotation=45)
ax.grid(axis='y')

# Menambahkan anotasi untuk titik maksimum dan minimum
max_cnt = sorted_bike_per_hour['cnt'].max()
min_cnt = sorted_bike_per_hour['cnt'].min()
max_hour = sorted_bike_per_hour.loc[sorted_bike_per_hour['cnt'].idxmax(), 'hr']
min_hour = sorted_bike_per_hour.loc[sorted_bike_per_hour['cnt'].idxmin(), 'hr']

ax.annotate(f'Maks: {max_cnt}', xy=(max_hour, max_cnt), xytext=(max_hour, max_cnt + 1),
            arrowprops=dict(facecolor='black', arrowstyle='->'), fontsize=12)
ax.annotate(f'Min: {min_cnt}', xy=(min_hour, min_cnt), xytext=(min_hour, min_cnt + 1),
            arrowprops=dict(facecolor='red', arrowstyle='->'), fontsize=12)

# Menampilkan chart di Streamlit
st.pyplot(fig)


import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Membuat DataFrame
hour_df = pd.DataFrame(hour_df)

# Menghitung jumlah pengguna casual berdasarkan weathersit
casual_by_weathersit = hour_df.groupby('weathersit')['casual'].sum()

# Mengurutkan hasil berdasarkan jumlah pengguna casual
sorted_casual_by_weathersit = casual_by_weathersit.sort_values(ascending=False)

# Menampilkan hasil dalam Streamlit dengan layout yang rapi
st.write("### Jumlah Pengguna Casual Berdasarkan Weathersit")
st.dataframe(sorted_casual_by_weathersit.reset_index(name='Jumlah Pengguna Casual'), width=400)

# Membuat line chart yang lebih rapi
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(sorted_casual_by_weathersit.index, sorted_casual_by_weathersit.values, marker='o', linestyle='-', color='b')

# Menambahkan judul dan label dengan format yang lebih jelas
ax.set_title('Jumlah Pengguna Casual Berdasarkan Weathersit', fontsize=16, fontweight='bold')
ax.set_xlabel('Weathersit', fontsize=14)
ax.set_ylabel('Jumlah Pengguna Casual', fontsize=14)
ax.set_xticks(sorted_casual_by_weathersit.index)  # Set ticks sesuai jumlah weathersit
ax.set_xticklabels(sorted_casual_by_weathersit.index, fontsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.grid(True, linestyle='--', alpha=0.6)

# Menampilkan chart di Streamlit
st.pyplot(fig)

st.caption('Copyright (c) Bangkit | Vina 2024')


