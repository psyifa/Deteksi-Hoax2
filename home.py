import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def show_home():
    # Load the dataset
    df = pd.read_csv("data.csv")
    df_evaluasi = pd.read_csv("Evaluasi Model.csv")

    # Convert 'Tanggal' to datetime
    df['Tanggal'] = pd.to_datetime(df['Tanggal'], format='%d/%m/%Y')
    df['Year'] = df['Tanggal'].dt.year

    # Convert text columns to string to avoid type errors
    df['Content'] = df['Content'].astype(str)

    # Row with 4 visualizations
    col1, col2, col3, col4 = st.columns([1.5, 2.5, 2, 2])

    # Visualization 1: Bar chart for Hoax vs Non-Hoax using Plotly
    with col1:
        st.markdown("<h6 style='font-size: 12px; margin-bottom: 0;'>Hoax vs Non-Hoax</h6>", unsafe_allow_html=True)
        df_label_counts = df['Label'].value_counts().reset_index()
        df_label_counts.columns = ['Label', 'Jumlah']
        bar_chart_label = px.bar(df_label_counts, x='Label', y='Jumlah', color='Label',
                                color_discrete_map={'HOAX': 'red', 'NON-HOAX': 'green'})
        bar_chart_label.update_layout(
            width=200, height=150, xaxis_title='Label', yaxis_title='Jumlah',
            xaxis_title_font_size=10, yaxis_title_font_size=10,
            xaxis_tickfont_size=8, yaxis_tickfont_size=8, margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False
        )
        st.plotly_chart(bar_chart_label, use_container_width=False)

    # Visualization 2: Bar chart for Hoax vs Non-Hoax per Data Source using Plotly
    with col2:
        st.markdown("<h6 style='font-size: 12px; margin-bottom: 0;'>Hoax vs Non-Hoax per Data Source</h6>", unsafe_allow_html=True)
        datasource_label_counts = df.groupby(['Datasource', 'Label']).size().reset_index(name='counts')
        fig_datasource = px.bar(datasource_label_counts, x='Datasource', y='counts', color='Label', barmode='group',
                               color_discrete_map={'HOAX': 'red', 'NON-HOAX': 'green'})
        fig_datasource.update_layout(
            width=500, height=150, xaxis_title='Datasource', yaxis_title='Jumlah',
            xaxis_title_font_size=10, yaxis_title_font_size=10,
            xaxis_tickfont_size=8, yaxis_tickfont_size=8, xaxis_tickangle=0,
            margin=dict(t=10, b=10, l=10, r=10), showlegend=True
        )
        st.plotly_chart(fig_datasource, use_container_width=False)
    
    # Visualization 3: Line chart for Hoax per Year using Plotly
    with col3:
        st.markdown("<h6 style='font-size: 12px; margin-bottom: 0;'>Hoax per Tahun</h6>", unsafe_allow_html=True)
        hoax_per_year = df[df['Label'] == 'HOAX'].groupby('Year').size().reset_index(name='count')
        line_chart_hoax = px.line(hoax_per_year, x='Year', y='count', line_shape='linear',
                                 color_discrete_sequence=['red'])
        line_chart_hoax.update_layout(
            width=200, height=150, xaxis_title='Tahun', yaxis_title='Jumlah Hoax',
            xaxis_title_font_size=10, yaxis_title_font_size=10,
            xaxis_tickfont_size=8, yaxis_tickfont_size=8, margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False
        )
        st.plotly_chart(line_chart_hoax, use_container_width=False)
    
    # Visualization 4: Line chart for Non-Hoax per Year using Plotly
    with col4:
        st.markdown("<h6 style='font-size: 12px; margin-bottom: 0;'>Non-Hoax per Tahun</h6>", unsafe_allow_html=True)
        non_hoax_per_year = df[df['Label'] == 'NON-HOAX'].groupby('Year').size().reset_index(name='count')
        line_chart_non_hoax = px.line(non_hoax_per_year, x='Year', y='count', line_shape='linear',
                                      color_discrete_sequence=['green'])
        line_chart_non_hoax.update_layout(
            width=200, height=150, xaxis_title='Tahun', yaxis_title='Jumlah Non-Hoax',
            xaxis_title_font_size=10, yaxis_title_font_size=10,
            xaxis_tickfont_size=8, yaxis_tickfont_size=8, margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False
        )
        st.plotly_chart(line_chart_non_hoax, use_container_width=False)

    # Create a new row for WordCloud visualizations
    col5, col6 = st.columns([2.5, 2.5])

    # Wordcloud for Hoax
    with col5:
        st.markdown("<h6 style='font-size: 12px; margin-bottom: 0;'>Wordcloud for Hoax</h6>", unsafe_allow_html=True)
        hoax_text = ' '.join(df[df['Label'] == 'HOAX']['Content'])
        wordcloud_hoax = WordCloud(width=500, height=150, background_color='white', colormap='Reds').generate(hoax_text)
        fig_hoax = plt.figure(figsize=(5, 2.5))
        plt.imshow(wordcloud_hoax, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(fig_hoax)
    
    # Wordcloud for Non-Hoax
    with col6:
        st.markdown("<h6 style='font-size: 12px; margin-bottom: 0;'>Wordcloud for Non-Hoax</h6>", unsafe_allow_html=True)
        non_hoax_text = ' '.join(df[df['Label'] == 'NON-HOAX']['Content'])
        wordcloud_non_hoax = WordCloud(width=500, height=150, background_color='white', colormap='Greens').generate(non_hoax_text)
        fig_non_hoax = plt.figure(figsize=(5, 2.5))
        plt.imshow(wordcloud_non_hoax, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(fig_non_hoax)
        
    col7 = st.columns([5])
    # Evaluation Metrics Table
    with col7[0]:
        st.markdown("<h6 style='font-size: 12px; margin-bottom: 0;'>Evaluation Metrics</h6>", unsafe_allow_html=True)
        header = pd.MultiIndex.from_tuples([
            ('Pre-trained Model', ''),
            ('Label 0', 'Precision'),
            ('Label 0', 'Recall'),
            ('Label 0', 'F1-Score'),
            ('Label 1', 'Precision'),
            ('Label 1', 'Recall'),
            ('Label 1', 'F1-Score'),
            ('', 'Accuracy')
        ])

        data = [
            ["indobenchmark/indobert-base-p2", 0.6898, 0.9793, 0.8094, 0.84, 0.1981, 0.3206, 0.7023],
            ["cahya/bert-base-indonesian-522M", 0.7545, 0.8756, 0.8106, 0.68, 0.4811, 0.5635, 0.7358],
            ["indolem/indobert-base-uncased", 0.7536, 0.8238, 0.7871, 0.6136, 0.5094, 0.5567, 0.7124],
            ["mdhugol/indonesia-bert-sentiment-classification", 0.7444, 0.8601, 0.7981, 0.6447, 0.4623, 0.5385, 0.7191]
        ]

        df = pd.DataFrame(data, columns=header)
        st.write(df)
