import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any

def render_comparison_charts(charts_data: Dict[str, Any]):
    if not charts_data:
        return

    st.subheader("Comparison Charts")
    
    # Token Usage Chart
    fig_tokens = go.Figure(data=[
        go.Bar(name='Prompt Tokens', x=list(charts_data.keys()), y=[d['prompt_tokens'] for d in charts_data.values()]),
        go.Bar(name='Completion Tokens', x=list(charts_data.keys()), y=[d['completion_tokens'] for d in charts_data.values()])
    ])
    fig_tokens.update_layout(title='Token Usage Comparison')
    st.plotly_chart(fig_tokens)

    # Response Time Chart
    fig_time = go.Figure(data=[go.Bar(x=list(charts_data.keys()), y=[d['time'] for d in charts_data.values()])])
    fig_time.update_layout(title='Response Time Comparison')
    st.plotly_chart(fig_time)