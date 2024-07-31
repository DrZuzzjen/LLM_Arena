import streamlit as st
import asyncio
import aiohttp
from config.settings import OPENAI_MODELS, NVIDIA_MODELS, GROQ_MODELS
from components.llm_card import llm_card
from components.comparison_charts import token_usage_chart, time_comparison_chart, overall_performance_chart

BACKEND_URL = st.secrets.get("BACKEND_URL", "http://backend:8000")

def app():
    st.title("Enhanced LLM Comparison with Metrics & Charts")

    col1, col2 = st.columns([2, 1])
    
    with col1:
        query = st.text_area("Enter your query:", height=100)
    
    with col2:
        st.subheader("Model Selection")
        openai_model = st.selectbox("OpenAI Model", OPENAI_MODELS)
        nvidia_model = st.selectbox("NVIDIA Model", NVIDIA_MODELS)
        groq_model = st.selectbox("Groq Model", GROQ_MODELS)

    # Create placeholders for each LLM
    placeholders = {}
    for provider in ["OpenAI", "NVIDIA", "Groq"]:
        placeholders[provider] = st.empty()

    # Create placeholders for charts
    charts_placeholder = st.empty()

    async def stream_response(provider, model, query, placeholder):
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
                        placeholder.empty()
                        with placeholder.container():
                            llm_card(provider, model, full_response, metrics)
        
        return metrics

    async def run_comparison(query, models):
        tasks = []
        for provider, model in models.items():
            tasks.append(stream_response(provider, model, query, placeholders[provider]))
        
        results = await asyncio.gather(*tasks)
        return dict(zip(models.keys(), results))

    if st.button("Compare LLMs"):
        if query:
            st.info("Comparison in progress...")
            
            models = {
                "OpenAI": openai_model,
                "NVIDIA": nvidia_model,
                "Groq": groq_model
            }
            
            results = asyncio.run(run_comparison(query, models))
            
            # Display comparison charts
            with charts_placeholder.container():
                st.subheader("Comparison Charts")
                token_usage_chart(results)
                time_comparison_chart(results)
                overall_performance_chart(results)
            
        else:
            st.warning("Please enter a query.")