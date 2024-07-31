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
            async def run_comparison():
                models = {
                    "OpenAI": openai_model,
                    "NVIDIA": nvidia_model,
                    "Groq": groq_model
                }
                tasks = [stream_response(provider, model, query, llm_placeholders[provider]) 
                        for provider, model in models.items()]
                results = await asyncio.gather(*tasks)
                return dict(zip(models.keys(), results))

            # Use asyncio to run the comparison
            results = asyncio.run(run_comparison())

            # Display LLM cards side-by-side
            with col1:
                llm_card("OpenAI", openai_model, results["OpenAI"]["response"], results["OpenAI"]["metrics"])
            with col2:
                llm_card("NVIDIA", nvidia_model, results["NVIDIA"]["response"], results["NVIDIA"]["metrics"])
            with col3:
                llm_card("Groq", groq_model, results["Groq"]["response"], results["Groq"]["metrics"])

            # Display comparison charts
            with charts_placeholder.container():
                st.subheader("Comparison Charts")
                col1, col2 = st.columns([2, 1])
                with col1:
                    token_usage_chart(results)
                    overall_performance_chart(results)
                with col2:
                    time_comparison_chart(results)

        else:
            st.warning("Please enter a query.")

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

    return {"response": full_response, "metrics": metrics}

async def run_comparison(query, models):
    tasks = [stream_response(provider, model, query) for provider, model in models.items()]
    results = await asyncio.gather(*tasks)
    return dict(zip(models.keys(), results))