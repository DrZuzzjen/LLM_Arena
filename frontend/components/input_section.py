import streamlit as st
from state.app_state import AppState

def render_input_section(app_state: AppState):
    query = st.text_area("Enter your query:", value=app_state.query)
    models = {
        "OpenAI": st.selectbox("OpenAI Model", ["gpt-3.5-turbo", "gpt-4"]),
        "NVIDIA": st.selectbox("NVIDIA Model", ["llama-2-70b-hf", "mixtral-8x7b-instruct-v0.1"]),
        "Groq": st.selectbox("Groq Model", ["llama2-70b-4096", "mixtral-8x7b-32768"])
    }
    return query, models