import streamlit as st
from pages import basic_comparison, metrics_charts

PAGES = {
    "Basic Comparison": basic_comparison,
    "Metrics & Charts": metrics_charts
}

st.set_page_config(page_title="LLM Comparison Tool", layout="wide")

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]
page.app()