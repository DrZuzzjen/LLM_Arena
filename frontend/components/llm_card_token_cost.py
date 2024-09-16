import streamlit as st
import uuid

def llm_card(provider: str, model: str, response: str, metrics: dict, finish_order: int = None):
    order_class = f"finish-order-{finish_order}" if finish_order is not None else ""
    order_icon = ["🥇", "🥈", "🥉"][finish_order - 1] if finish_order is not None and finish_order <= 3 else ""
    
    card_html = f"""
    <div class="llm-card {order_class}" id="{provider}-card">
        <h4>{provider} - {model} {order_icon}</h4>
        <p class="truncate-response">{' '.join(response.split()[:50])}...</p>
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
    """
    return card_html

def load_custom_css():
    st.markdown("""
    <style>
    .llm-card {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
        transition: all 0.5s ease;
    }
    .llm-card h4 {
        margin-top: 0;
        margin-bottom: 5px;
    }
    .truncate-response {
        white-space: normal;
        overflow: visible;
        text-overflow: clip;
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
    .finish-order-1 {
        background-color: #90EE90;
        transform: scale(1.05);
        border: 2px solid #006400;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .finish-order-2 {
        background-color: #FFFFE0;
        transform: scale(1.03);
    }
    .finish-order-3 {
        background-color: #FFB6C1;
        transform: scale(1.01);
    }
    .view-full-response {
        margin-top: 10px;
        padding: 5px 10px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 3px;
        cursor: pointer;
    }
    .view-full-response:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)