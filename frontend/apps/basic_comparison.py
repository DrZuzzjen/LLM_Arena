import streamlit as st
import asyncio
import aiohttp
from config.settings import OPENAI_MODELS, NVIDIA_MODELS, GROQ_MODELS

BACKEND_URL = st.secrets.get("BACKEND_URL", "http://backend:8000")

def app():
    st.title("Basic LLM Comparison")

    query = st.text_input("Enter your query:")

    model_types = {
        "OpenAI": st.selectbox("OpenAI Model", OPENAI_MODELS),
        "NVIDIA": st.selectbox("NVIDIA Model", NVIDIA_MODELS),
        "Groq": st.selectbox("Groq Model", GROQ_MODELS)
    }

    async def stream_response(provider, url, response_placeholder, timer_placeholder):
        start_time = asyncio.get_event_loop().time()
        full_response = ""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                async for line in response.content:
                    if line:
                        decoded_line = line.decode('utf-8').strip()
                        if decoded_line.startswith("data: "):
                            data = decoded_line[6:]
                            if data == "[DONE]":
                                break
                            full_response += data
                            response_placeholder.markdown(f"**{provider}**:\n{full_response}")
                    elapsed = asyncio.get_event_loop().time() - start_time
                    timer_placeholder.text(f"{provider} Time: {elapsed:.2f}s")
        
        elapsed = asyncio.get_event_loop().time() - start_time
        timer_placeholder.text(f"{provider} Time: {elapsed:.2f}s (Completed)")

    async def run_comparison():
        if query:
            tasks = []
            for provider in model_types:
                col1, col2 = st.columns([3, 1])
                response_placeholder = col1.empty()
                timer_placeholder = col2.empty()
                url = f"{BACKEND_URL}/stream/{provider.lower()}?query={query}&model={model_types[provider]}"
                tasks.append(stream_response(provider, url, response_placeholder, timer_placeholder))
            await asyncio.gather(*tasks)
        else:
            st.warning("Please enter a query.")

    if st.button("Compare LLMs"):
        asyncio.run(run_comparison())