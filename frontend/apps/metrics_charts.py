import streamlit as st
import asyncio
import aiohttp
import plotly.graph_objects as go  # Add this line

from plotly.subplots import make_subplots
from config.settings import OPENAI_MODELS, NVIDIA_MODELS, GROQ_MODELS
from components.llm_card import llm_card, load_custom_css
from components.comparison_charts import token_usage_chart, time_comparison_chart, overall_performance_chart

BACKEND_URL = st.secrets.get("BACKEND_URL", "http://backend:8000")

def assign_colors(results, metric, reverse=False):
    sorted_providers = sorted(results.keys(), key=lambda k: results[k]['metrics'][metric], reverse=reverse)
    colors = {
        sorted_providers[0]: "#90EE90",  # Green for best performer
        sorted_providers[1]: "#FFFFE0",  # Yellow for middle performer
        sorted_providers[2]: "#FFB6C1"   # Pink for worst performer
    }
    return colors


def create_comparison_chart(results, metric, title, xaxis_title, reverse_sort=False):
    colors = assign_colors(results, metric, reverse_sort)
    fig = go.Figure()
    
    for provider, data in results.items():
        fig.add_trace(go.Bar(
            y=[provider],
            x=[data['metrics'][metric]],
            name=provider,
            orientation='h',
            marker_color=colors[provider],
            text=[f"{data['metrics'][metric]:.2f}"],
            textposition='outside',
            hoverinfo='text',
            hovertext=f"{provider}: {data['metrics'][metric]:.2f}",
            textfont=dict(size=14),
            marker=dict(line=dict(width=2, color='#000000'))
        ))

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, color='#333333'),
            x=0.5,
            y=0.95
        ),
        xaxis=dict(title=xaxis_title, tickfont=dict(size=12)),
        yaxis=dict(title='', tickfont=dict(size=14)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='rgba(240, 240, 240, 0.5)',
        height=300,
        width=500,
        margin=dict(l=150, r=50, t=80, b=50),
        bargap=0.3
    )
    
    return fig

def words_per_second_chart(results):
    fig = create_comparison_chart(results, 'words_per_second', 'Words Per Second Comparison', 'Words/Second', reverse_sort=True)
    st.plotly_chart(fig, use_container_width=True)

def time_comparison_chart(results):
    fig = create_comparison_chart(results, 'time', 'Response Time Comparison', 'Time (seconds)')
    st.plotly_chart(fig, use_container_width=True)

def app():
    load_custom_css()
    st.title("Enhanced LLM Comparison with Metrics & Charts")

    query = st.text_area("Enter your query:", height=100, placeholder="Try asking a question or providing some context.", value="whats heavier, 100kg of feathers or 100kg of steel?")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        openai_model = st.selectbox("OpenAI Model", OPENAI_MODELS)
    with col2:
        nvidia_model = st.selectbox("NVIDIA Model", NVIDIA_MODELS)
    with col3:
        groq_model = st.selectbox("Groq Model", GROQ_MODELS)

    if st.button("Compare LLMs"):
        if query:
            # Create placeholders for LLM cards
            col1, col2, col3 = st.columns(3)
            llm_placeholders = {
                "OpenAI": col1.empty(),
                "NVIDIA": col2.empty(),
                "Groq": col3.empty()
            }

            # Create placeholder for charts
            charts_placeholder = st.empty()

            # Run comparison asynchronously
            results = asyncio.run(run_comparison(query, {
                "OpenAI": openai_model,
                "NVIDIA": nvidia_model,
                "Groq": groq_model
            }, llm_placeholders))

            # Display comparison charts
            with charts_placeholder.container():
                st.subheader("Performance Comparisons")
                col1, col2 = st.columns(2)
                with col1:
                    time_comparison_chart(results)
                with col2:
                    words_per_second_chart(results)
                
                # Keep the other charts as they are
                token_usage_chart(results)
                overall_performance_chart(results)

        else:
            st.warning("Please enter a query.")

async def stream_response(provider, model, query, placeholder, finish_order_queue):
    url = f"{BACKEND_URL}/stream/{provider.lower()}?query={query}&model={model}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            start_time = asyncio.get_event_loop().time()
            full_response = ""
            metrics = {
                "time": 0,
                "total_tokens": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "cost": 0,
                "word_count": 0,
                "words_per_second": 0  # New metric
            }
            finish_order = None
            
            # Initial card render
            placeholder.markdown(llm_card(provider, model, full_response, metrics), unsafe_allow_html=True)
            
            async for line in response.content:
                if line:
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line.startswith("data: "):
                        data = decoded_line[6:]
                        if data == "[DONE]":
                            if finish_order is None:
                                finish_order = await finish_order_queue.get()
                            break
                        if data.startswith("{"):  # Metrics update
                            new_metrics = eval(data)  # Be cautious with eval in production!
                            metrics.update(new_metrics)
                        else:  # Response content
                            full_response += data
                            metrics["word_count"] = len(full_response.split())

                    elapsed_time = asyncio.get_event_loop().time() - start_time
                    metrics["time"] = elapsed_time
                    
                    # Calculate words per second
                    if elapsed_time > 0:
                        metrics["words_per_second"] = metrics["word_count"] / elapsed_time
                    
                    placeholder.markdown(llm_card(provider, model, full_response, metrics, finish_order), unsafe_allow_html=True)

    # Final update with finish order
    final_time = asyncio.get_event_loop().time() - start_time
    metrics["time"] = final_time
    metrics["words_per_second"] = metrics["word_count"] / final_time if final_time > 0 else 0
    placeholder.markdown(llm_card(provider, model, full_response, metrics, finish_order), unsafe_allow_html=True)
    
    return {"response": full_response, "metrics": metrics, "finish_order": finish_order}

async def run_comparison(query, models, llm_placeholders):
    finish_order_queue = asyncio.Queue()
    for i in range(1, len(models) + 1):
        await finish_order_queue.put(i)

    tasks = [stream_response(provider, model, query, llm_placeholders[provider], finish_order_queue) 
             for provider, model in models.items()]
    results = await asyncio.gather(*tasks)
    return dict(zip(models.keys(), results))