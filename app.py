import streamlit as st
from streamlit_option_menu import option_menu

# Tambahkan CSS kustom untuk menyesuaikan ukuran dan jarak menu
st.markdown("""
    <style>
    /* Kurangi margin dan padding dari elemen-elemen utama */
    .css-18e3th9 {
        padding-top: 10px;  /* Kurangi jarak dari atas */
        padding-bottom: 10px; /* Sesuaikan padding bawah jika diperlukan */
    }
    .css-1d391kg > div > div > button {
        padding: 5px 10px;  /* Atur padding pada tombol */
        font-size: 12px;  /* Atur ukuran font pada teks menu */
    }
    .css-1d391kg > div > div > button > div {
        font-size: 12px;  /* Atur ukuran font pada teks menu */
    }
    </style>
    """, unsafe_allow_html=True)

# Menu horizontal di bagian atas halaman
selected = option_menu(
    menu_title=None,
    options=["Dashboard", "Deteksi Hoax"],
    icons=["bar-chart-line-fill", "newspaper"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Konten halaman berdasarkan pilihan menu
if selected == "Dashboard":
    st.title(f"You have selected {selected}")
elif selected == "Deteksi Hoax":
    st.title(f"You have selected {selected}")
