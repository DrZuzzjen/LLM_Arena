import streamlit as st
import asyncio
import aiohttp
from config.settings import OPENAI_MODELS, NVIDIA_MODELS, GROQ_MODELS
from components.llm_card import llm_card, load_custom_css
from components.comparison_charts import token_usage_chart, time_comparison_chart, overall_performance_chart

BACKEND_URL = st.secrets.get("BACKEND_URL", "http://backend:8000")

def app():
    load_custom_css()
    st.title("Enhanced LLM Comparison with Metrics & Charts")

    query = st.text_area("Enter your query:", height=100)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        openai_model = st.selectbox("OpenAI Model", OPENAI_MODELS)
    with col2:
        nvidia_model = st.selectbox("NVIDIA Model", NVIDIA_MODELS)
    with col3:
        groq_model = st.selectbox("Groq Model", GROQ_MODELS)

    if st.button("Compare LLMs"):
        if query:
            st.info("Comparison in progress...")
            
            models = {
                "OpenAI": openai_model,
                "NVIDIA": nvidia_model,
                "Groq": groq_model
            }
            
            results = asyncio.run(run_comparison(query, models))
            
            # Display LLM cards
            llm_cols = st.columns(3)
            for (provider, model), result, col in zip(models.items(), results.values(), llm_cols):
                with col:
                    llm_card(provider, model, result['response'], result['metrics'])
            
            # Display comparison charts
            st.subheader("Comparison Charts")
            chart_col1, chart_col2 = st.columns([2, 1])
            with chart_col1:
                token_usage_chart(results)
                overall_performance_chart(results)
            with chart_col2:
                time_comparison_chart(results)

    else:
        st.warning("Please enter a query.")

async def stream_response(provider, model, query):
    url = f"{BACKEND_URL}/stream/{provider.lower()}?query={query}&model={model}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            start_time = asyncio.get_event_loop().time()
            full_response = ""
            metrics = {"time": 0, "total_tokens": 0, "prompt_tokens": 0, "completion_tokens": 0, "cost": 0, "word_count": 0}
            async for line in response.content:
                if line:
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line.startswith("data: "):
                        data = decoded_line[6:]
                        if data == "[DONE]":
                            break
                        if data.startswith("{"):  # Metrics update
                            new_metrics = eval(data)  # Be cautious with eval in production!
                            metrics.update(new_metrics)
                        else:  # Response content
                            full_response += data
                            metrics["word_count"] = len(full_response.split())
                    
                    metrics["time"] = asyncio.get_event_loop().time() - start_time
    
    return {"response": full_response, "metrics": metrics}

async def run_comparison(query, models):
    tasks = [stream_response(provider, model, query) for provider, model in models.items()]
    results = await asyncio.gather(*tasks)
    return dict(zip(models.keys(), results))