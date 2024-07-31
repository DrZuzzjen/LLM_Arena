import streamlit as st

def llm_card(provider: str, model: str, response: str, metrics: dict):
    with st.expander(f"{provider} - {model}", expanded=True):
        st.markdown(f"**Response:**\n{response}")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Time", f"{metrics['time']:.2f}s")
            st.metric("Tokens Used", metrics['total_tokens'])
        with col2:
            st.metric("Cost", f"${metrics['cost']:.6f}")
            st.metric("Words", metrics['word_count'])