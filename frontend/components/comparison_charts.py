import streamlit as st
import plotly.graph_objects as go

def token_usage_chart(results):
    fig = go.Figure(data=[
        go.Bar(name='Prompt Tokens', x=list(results.keys()), y=[r['metrics']['prompt_tokens'] for r in results.values()]),
        go.Bar(name='Completion Tokens', x=list(results.keys()), y=[r['metrics']['completion_tokens'] for r in results.values()])
    ])
    fig.update_layout(barmode='stack', title='Token Usage Comparison', height=300)
    st.plotly_chart(fig, use_container_width=True)

def time_comparison_chart(results):
    fig = go.Figure(data=[go.Bar(x=list(results.keys()), y=[r['metrics']['time'] for r in results.values()])])
    fig.update_layout(title='Response Time Comparison', height=300)
    st.plotly_chart(fig, use_container_width=True)

def overall_performance_chart(results):
    categories = ['Response Time', 'Token Efficiency', 'Cost Efficiency']
    fig = go.Figure()

    for provider, data in results.items():
        fig.add_trace(go.Scatterpolar(
            r=[data['metrics']['time'], data['metrics']['total_tokens'], data['metrics']['cost']],
            theta=categories,
            fill='toself',
            name=provider
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title='Overall Performance Comparison',
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)