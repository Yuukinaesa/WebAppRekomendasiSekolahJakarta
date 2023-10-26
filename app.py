import streamlit as st
import pandas as pd
import pydeck as pdk

# Judul aplikasi
st.title('Sekolah di DKI Jakarta')

# Membaca data dari CSV
@st.cache_resource
def load_data():
    data = pd.read_csv('DataSebaranSekolah.csv')
    return data

st.cache_resource
def load_ujian_data():
    return pd.read_csv('data-rata-rata-hasil-ujian-nasional-tahun-pelajaran-20182019.csv')

df = load_data()
ujian_data = load_ujian_data()

# Pencarian sekolah
school_search = st.text_input("Cari Nama Sekolah:", "")
if school_search:
    df = df[df['nama_sekolah'].str.contains(school_search, case=False, na=False)]

# Filter berdasarkan kecamatan
kecamatans = sorted(df['kecamatan'].unique())
selected_kecamatan = st.selectbox("Pilih Kecamatan:", options=['Semua Kecamatan'] + list(kecamatans))
if selected_kecamatan != 'Semua Kecamatan':
    df = df[df['kecamatan'] == selected_kecamatan]

# Urutkan opsi "Tipe Sekolah" berdasarkan urutan khusus
school_types_order = ['SD', 'SMP', 'SMA', 'SMK']
school_types = sorted(df['tipe_sekolah'].unique(), key=lambda x: school_types_order.index(x) if x in school_types_order else len(school_types_order))
selected_type = st.selectbox("Pilih Tipe Sekolah:", options=['Semua Tipe'] + list(school_types))
if selected_type != 'Semua Tipe':
    df = df[df['tipe_sekolah'] == selected_type]

# Filter berdasarkan akreditasi
accreditations = sorted(df['akreditasi'].unique())
selected_accreditation = st.selectbox("Pilih Akreditasi:", options=['Semua Akreditasi'] + list(accreditations))
if selected_accreditation != 'Semua Akreditasi':
    df = df[df['akreditasi'] == selected_accreditation]

# Ekstrak koordinat untuk visualisasi
df[['latitude', 'longitude']] = df['koordinat'].str.split(',', expand=True).astype(float)

# Membuat peta dengan pydeck
layer = pdk.Layer(
    'ScatterplotLayer',
    data=df,
    get_position='[longitude, latitude]',
    get_color='[200, 30, 0, 160]',
    get_radius=100,
    pickable=True
)

view_state = pdk.ViewState(
    latitude=-6.2,
    longitude=106.8,
    zoom=11,
    pitch=50,
)

# Render peta
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[layer],
    tooltip={
        "text": "Nama: {nama_sekolah}\nAlamat: {alamat}\nKelurahan: {kelurahan}\nKecamatan: {kecamatan}\nNo. Telp: {telp_sekolah}\nTipe Sekolah: {tipe_sekolah}\nAkreditasi: {akreditasi}"
    }
))

st.write("──────────────────────────────────────────────────────────────")
st.markdown("<h3 style='text-align: center; color: white;'>Rekomendasi Sekolah Berdasarkan Mata Pelajaran </h2>", unsafe_allow_html=True)


# Rekomendasi berdasarkan mata pelajaran
mata_pelajaran = st.selectbox("Pilih Mata Pelajaran untuk Rekomendasi:", [''] + list(ujian_data['mata_pelajaran'].unique()))
if mata_pelajaran:
    filtered_ujian_data = ujian_data[ujian_data['mata_pelajaran'] == mata_pelajaran]
    recommended = filtered_ujian_data.sort_values(by='nilai_rataan_ujian', ascending=False).iloc[0]
    st.write(f"Sekolah {recommended['jenis sekolah/ jenjang']} {recommended['status sekolah']} direkomendasikan untuk mata pelajaran {mata_pelajaran} dengan rata-rata nilai {recommended['nilai_rataan_ujian']}")
