import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("LLM Comparison Tool")

query = st.text_input("Enter your query:")
if st.button("Compare LLMs"):
    if query:
        with st.spinner("Processing..."):
            response = requests.post(f"{BACKEND_URL}/compare", json={"query": query})
            if response.status_code == 200:
                result = response.json()
                st.success("Comparison complete!")
                st.write(result)
            else:
                st.error("An error occurred while processing your request.")
    else:
        st.warning("Please enter a query.")