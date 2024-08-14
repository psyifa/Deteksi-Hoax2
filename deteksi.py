import streamlit as st
from datetime import datetime
import pandas as pd

def show_deteksi():
    # Create a radio button to select detection method, displayed horizontally
    detection_method = st.radio("Pilih Metode Deteksi", 
                                ("Deteksi Hoax per Content", "Deteksi Hoax Unggah Data"), 
                                horizontal=True)

    if detection_method == "Deteksi Hoax per Content":
        st.title("Deteksi Berita Hoax")

        # Initialize session state for correction
        if 'correction' not in st.session_state:
            st.session_state.correction = None
        if 'detection_result' not in st.session_state:
            st.session_state.detection_result = None

        # Dropdown for selecting a model
        model = st.selectbox(
            "Pilih model",
            ["cahya/bert-base-indonesian-522M", "indobenchmark/indobert-base-p2"]
        )

        # Text input for the headline
        headline = st.text_input("Masukkan judul berita")

        # Text area for the article content
        content = st.text_area("Masukkan konten berita")

        # Detection button
        if st.button("Deteksi"):
            if headline and content:
                # Dummy detection result
                st.session_state.detection_result = "Non-Hoax"  # Replace with actual detection logic if needed

        # Display the detection result and correction options
        if st.session_state.detection_result:
            st.success(f"Prediksi: {st.session_state.detection_result}")

            st.write("Koreksi")
            st.session_state.correction = st.radio("", ("Non-Hoax", "Hoax"), index=0 if st.session_state.correction == "Non-Hoax" else 1)

            # Save button
            if st.button("Simpan"):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open('corrections.csv', 'a', encoding='utf-8') as f:
                    f.write(f"{headline},{content},{st.session_state.detection_result},{st.session_state.correction},{timestamp}\n")
                st.success("Koreksi telah disimpan.")

    elif detection_method == "Deteksi Hoax Unggah Data":
        st.title("Deteksi Berita Hoax")
        st.write("Unggah File CSV untuk mendeteksi")

        # Dropdown for model selection
        model_option = st.selectbox(
            'Pilih Model',
            ('cahya/bert-base-indonesian-522M', 'indobenchmark/indobert-base-p2')
        )

        # File uploader
        uploaded_file = st.file_uploader("Unggah file disini", type="csv")

        # Initialize session state to store the corrections
        if 'corrections' not in st.session_state:
            st.session_state.corrections = []

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("### Uploaded Data")
            st.dataframe(df)

            if st.button("Deteksi"):
                # Simulate detection results
                df['Result'] = 'Non-Hoax'
                df['Correction'] = ''

                # Save detection results in session state
                st.session_state.df = df
                st.session_state.corrections = [''] * len(df)

            if 'df' in st.session_state:
                df = st.session_state.df

                # Display detection results
                st.write("### Detection Results")
                st.dataframe(df)

                # Display correction buttons
                for i in range(len(df)):
                    st.write(f"Row {i+1}: {df.iloc[i]['Title']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Hoax {i+1}"):
                            st.session_state.corrections[i] = 'Hoax'
                    with col2:
                        if st.button(f"Non-Hoax {i+1}"):
                            st.session_state.corrections[i] = 'Non-Hoax'

                # Update DataFrame with corrections
                for i in range(len(st.session_state.corrections)):
                    df.at[i, 'Correction'] = st.session_state.corrections[i]

                st.write("### Corrected Data")
                st.dataframe(df)

                # Save corrected data
                if st.button("Simpan"):
                    df.to_csv("corrected_data.csv", index=False)
                    st.success("Data saved successfully")
