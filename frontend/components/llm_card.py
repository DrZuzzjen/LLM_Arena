import streamlit as st
import uuid

def llm_card(provider: str, model: str, response: str, metrics: dict):
    st.markdown(f"""
    <div class="llm-card">
        <h4>{provider} - {model}</h4>
        <p class="truncate-response">{' '.join(response.split()[:20])}...</p>
        <div class="metrics-grid">
            <div class="metric">
                <span class="metric-label">Time:</span>
                <span class="metric-value">{metrics['time']:.2f}s</span>
            </div>
            <div class="metric">
                <span class="metric-label">Cost:</span>
                <span class="metric-value">${metrics['cost']:.6f}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Tokens:</span>
                <span class="metric-value">{metrics['total_tokens']}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Words:</span>
                <span class="metric-value">{metrics['word_count']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(f"Show full response for {provider}", key=f"{provider}_show_more_{uuid.uuid4().hex}"):
        st.markdown(f"**Full Response:**\n{response}")

def load_custom_css():
    st.markdown("""
    <style>
    .llm-card {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .llm-card h4 {
        margin-top: 0;
        margin-bottom: 5px;
    }
    .truncate-response {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 5px;
    }
    .metric {
        display: flex;
        justify-content: space-between;
    }
    .metric-label {
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)