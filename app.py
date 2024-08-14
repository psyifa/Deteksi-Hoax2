import streamlit as st
from home import show_home
from deteksi import show_deteksi

# Set page configuration
st.set_page_config(page_title="Hoax Detection Dashboard", layout="wide")

# Create tabs
tab1, tab2 = st.tabs(["Home", "Deteksi"])

# Content for the "Home" tab
with tab1:
    show_home()

# Content for the "Deteksi" tab
with tab2:
    show_deteksi()
