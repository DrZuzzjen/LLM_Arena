import streamlit as st
import plotly.graph_objects as go

def token_usage_chart(metrics: dict):
    fig = go.Figure(data=[
        go.Bar(name='Prompt Tokens', x=list(metrics.keys()), y=[m['prompt_tokens'] for m in metrics.values()]),
        go.Bar(name='Completion Tokens', x=list(metrics.keys()), y=[m['completion_tokens'] for m in metrics.values()])
    ])
    fig.update_layout(barmode='stack', title='Token Usage Comparison')
    st.plotly_chart(fig)

def time_comparison_chart(metrics: dict):
    fig = go.Figure(data=[go.Bar(x=list(metrics.keys()), y=[m['time'] for m in metrics.values()])])
    fig.update_layout(title='Response Time Comparison')
    st.plotly_chart(fig)

def overall_performance_chart(metrics: dict):
    categories = ['Response Time', 'Token Efficiency', 'Cost Efficiency']
    fig = go.Figure()

    for provider, data in metrics.items():
        fig.add_trace(go.Scatterpolar(
            r=[data['time'], data['total_tokens'], data['cost']],
            theta=categories,
            fill='toself',
            name=provider
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title='Overall Performance Comparison'
    )
    st.plotly_chart(fig)