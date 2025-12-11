import streamlit as st
import math

# --- 1. Data Acuan Tetap ---
LUAS_ACUAN = 1440.0
KAPASITAS_ACUAN_MAKSIMAL = 3500.0
PERSENTASE_REALISASI = 0.80
KAPASITAS_PER_M2_RIIL = (KAPASITAS_ACUAN_MAKSIMAL * PERSENTASE_REALISASI) / LUAS_ACUAN

# --- Konfigurasi Halaman & Desain ---
st.set_page_config(
    page_title="Kalkulator Kapasitas Gudang",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Menambahkan gaya kustom (CSS) untuk Skema Warna Akhir
st.markdown("""
<style>
/* 1. Latar Belakang Utama */

/* Latar Belakang Body Utama (Halaman Input) = Putih */
.stApp {
    background-color: #FFFFFF; 
}

/* Latar Belakang Sidebar (Data Acuan) = Krem Coklat Pucat */
[data-testid="stSidebarContent"] {
    background-color: #EFEBE9; /* Krem Coklat Pucat */
    border-right: 1px solid #D7CCC8; /* Garis pemisah lembut */
}

/* 2. Warna Teks Umum (Agar Kontras) */

/* Warna Teks Default (H1, H2, label) = Hitam Gelap */
h1, h2, h3, h4, label {
    color: #333333 !important; 
}
/* Teks di Sidebar (terutama judul) harus gelap */
.stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar p {
    color: #333333 !important; 
}

/* 3. Style untuk Metrik Hasil */

/* Background Metrik Hasil = Biru Pucat */
[data-testid="stMetric"] {
    background-color: #F4F8FB; 
    padding: 10px;
    border-radius: 8px;
    border-left: 5px solid #007BFF; 
}

/* Warna Teks Keterangan Pembulatan (Delta Label) = Hitam/Abu-abu Gelap */
[data-testid="stMetricDelta"] {
    color: #555555 !important; /* Diubah menjadi gelap */
    font-weight: normal;
}

/* Warna Nilai Metrik (Angka Kapasitas Riil) = Biru Kuat */
[data-testid="stMetric"]:nth-child(1) [data-testid="stMetricValue"] {
    color: #007BFF !important; 
    font-size: 2em; 
}

/* Warna Nilai Metrik (Angka Kapasitas FINAL) = Hijau Kuat */
[data-testid="stMetric"]:nth-child(2) [data-testid="stMetricValue"] {
    color: #28A745 !important; 
    font-size: 2.5em; 
}

/* 4. Style untuk Estimasi Akhir (st.success) */

/* Background st.success = Hijau Tua Banget, Teks Putih */
[data-testid="stSuccess"] {
    background-color: #006400 !important; /* Hijau Tua Banget (Dark Green) */
    color: #FFFFFF !important; /* Teks harus putih agar kontras */
    border-radius: 8px;
    font-weight: bold;
    font-size: 1.1em;
}

</style>
""", unsafe_allow_html=True)


# --- Sidebar untuk Data Acuan ---
with st.sidebar:
    st.title("📚 Data Acuan Gudang")
    st.info("Acuan perhitungan menggunakan gudang Bulog ukuran standar (1440 M²).")
    
    st.subheader("Detail Acuan")
    st.metric("Luas Acuan", f"{LUAS_ACUAN:,.0f} M²")
    st.metric("Kapasitas Riil per M²", f"{KAPASITAS_PER_M2_RIIL:.4f} Ton/M²")
    st.caption(f"Diambil dari {KAPASITAS_ACUAN_MAKSIMAL:,.0f} Ton x {PERSENTASE_REALISASI * 100:.0f}%")
    
# --- Judul Utama Aplikasi ---
st.title("⚖️ Kalkulator Kapasitas Gudang")
st.caption("Hitung estimasi kapasitas berdasarkan Panjang dan Lebar yang diukur.")

# --- 2. Area Input (Panjang dan Lebar) ---
st.subheader("1. Masukkan Dimensi Gudang (Meter)")

col_input_panjang, col_input_lebar = st.columns(2)

with col_input_panjang:
    # Input Panjang
    panjang_input = st.number_input(
        "Panjang Gudang (M):",
        min_value=0.0,
        value=40.0, 
        step=1.0,
        format="%.2f"
    )

with col_input_lebar:
    # Input Lebar
    lebar_input = st.number_input(
        "Lebar Gudang (M):",
        min_value=0.0,
        value=25.0,
        step=1.0,
        format="%.2f"
    )

# --- 3. Hitungan Logika ---
luas_terhitung = panjang_input * lebar_input

if luas_terhitung > 0:
    kapasitas_teoritis = luas_terhitung * KAPASITAS_PER_M2_RIIL
    # Pembulatan ke kelipatan 1000 Ton (sesuai permintaan awal)
    kapasitas_final = math.ceil(kapasitas_teoritis / 1000) * 1000
else:
    kapasitas_teoritis = 0
    kapasitas_final = 0

# --- 4. Area Hasil ---
st.subheader("2. Hasil Estimasi Kapasitas")

if luas_terhitung > 0:
    
    # Tampilkan Luas yang Dihitung
    st.info(f"Luas Area Dihitung: **{luas_terhitung:,.2f} M²** (Panjang {panjang_input} M x Lebar {lebar_input} M)")
    
    col_hasil1, col_hasil2 = st.columns(2)

    with col_hasil1:
        # Kapasitas Riil Dihitung
        st.metric(
            label="Kapasitas Riil (Hasil Formula)",
            value=f"{kapasitas_teoritis:,.2f} Ton",
        )

    with col_hasil2:
        # Kapasitas Final Dibulatkan
        st.metric(
            label="KAPASITAS GUDANG FINAL (TON)",
            value=f"{int(kapasitas_final):,.0f} Ton",
            delta="Dibulatkan ke kelipatan 1000 Ton",
            delta_color="off" 
        )
        
    # Teks Hasil Akhir dengan background Hijau Tua Banget
    st.success(f"Estimasi yang disarankan untuk gudang ini adalah **{int(kapasitas_final):,.0f} Ton**.")

else:
    st.warning("Silakan masukkan Panjang dan Lebar Gudang (M) yang lebih besar dari nol.")