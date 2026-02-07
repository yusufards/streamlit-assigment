import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(page_title="NYC Taxi Analysis Dashboard", layout="wide")

# Fungsi Load Data dengan Cache agar cepat
@st.cache_data
def load_data():
    df = pd.read_csv('dataset_bersih_final.csv')
    # Sampling data agar aplikasi ringan saat di-deploy
    return df.sample(50000) if len(df) > 50000 else df

df = load_data()

# KOMPONEN 1: Header (st.title)
st.title("🚕 NYC Taxi Trip Analysis Dashboard")
st.markdown("Dashboard ini menganalisis hubungan antara jarak perjalanan, lokasi, dan biaya taksi.")

# SIDEBAR UNTUK FILTER
st.sidebar.header("Filter Navigasi")

# KOMPONEN 2: Slider (st.sidebar.slider)
# Filter berdasarkan Trip Distance
dist_range = st.sidebar.slider(
    "Pilih Rentang Jarak (Miles):",
    float(df['trip_distance'].min()),
    float(df['trip_distance'].max()),
    (0.0, 5.0)
)

# KOMPONEN 3: Selectbox (st.sidebar.selectbox)
# Filter berdasarkan Location ID
all_locations = sorted(df['PULocationID'].unique())
selected_loc = st.sidebar.selectbox("Pilih Pickup Location ID:", ["All"] + list(all_locations))

# Filter Data Berdasarkan Input
filtered_df = df[(df['trip_distance'] >= dist_range[0]) & (df['trip_distance'] <= dist_range[1])]
if selected_loc != "All":
    filtered_df = filtered_df[filtered_df['PULocationID'] == selected_loc]

# KOMPONEN 4: Metrics (st.metric)
col1, col2, col3 = st.columns(3)
col1.metric("Total Data Terfilter", f"{len(filtered_df):,}")
col2.metric("Rata-rata Fare", f"${filtered_df['fare_amount'].mean():.2f}")
col3.metric("Rata-rata Jarak", f"{filtered_df['trip_distance'].mean():.2f} mi")

# VISUALISASI INTERAKTIF
st.subheader("Visualisasi Hubungan Data")

tab1, tab2 = st.tabs(["Distribusi & Korelasi", "Analisis Lokasi"])

with tab1:
    # Scatter Plot: Jarak vs Biaya
    fig1 = px.scatter(
        filtered_df, x="trip_distance", y="total_amount", 
        color="fare_amount", title="Hubungan Jarak Perjalanan vs Total Biaya",
        labels={"trip_distance": "Jarak (Miles)", "total_amount": "Total Bayar"}
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    # Bar Chart: Top Location by Fare
    top_loc = filtered_df.groupby('PULocationID')['total_amount'].mean().reset_index().sort_values(by='total_amount', ascending=False).head(10)
    fig2 = px.bar(
        top_loc, x='PULocationID', y='total_amount', 
        title="Top 10 Lokasi dengan Rata-rata Biaya Tertinggi",
        labels={'PULocationID': 'ID Lokasi', 'total_amount': 'Rata-rata Total ($)'}
    )
    st.plotly_chart(fig2, use_container_width=True)

# KOMPONEN 5: Dataframe (st.dataframe)
st.subheader("Sampel Data Mentah")
st.dataframe(filtered_df.head(100), use_container_width=True)