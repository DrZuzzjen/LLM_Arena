import streamlit as st
from apps.basic_comparison import app as basic_comparison
from apps.metrics_charts import app as metrics_charts

# Deshabilitar completamente la detección automática de páginas
st.set_page_config(page_title="LLM Comparison Tool", layout="wide")

# Ocultar todos los elementos extra
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Crear un diccionario de páginas
PAGES = {
    "Metrics & Charts": metrics_charts,
    "Basic Comparison": basic_comparison
}

# Barra lateral para navegación
selection = st.sidebar.radio("Choose a comparison mode:", list(PAGES.keys()))

# Mostrar la página seleccionada
PAGES[selection]()