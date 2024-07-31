import streamlit as st
from state.app_state import LLMResponse

def render_llm_card(llm_response: LLMResponse):
    # Render LLM card based on llm_response data
    st.write(f"{llm_response.provider} - {llm_response.model}")
    st.write(f"Response: {llm_response.response}")
    st.write(f"Metrics: {llm_response.metrics}")
    st.write(f"Finish Order: {llm_response.finish_order}")

def render_llm_cards(llm_responses):
    for provider, llm_response in llm_responses.items():
        render_llm_card(llm_response)