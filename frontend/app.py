import streamlit as st
import asyncio
import aiohttp
import os

BACKEND_URL = st.secrets.get("BACKEND_URL", os.getenv("BACKEND_URL", "http://backend:8000"))

st.title("LLM Comparison Tool")

query = st.text_input("Enter your query:")
model_types = {
    "OpenAI": st.selectbox("OpenAI Model", ["gpt-4o", "gpt-4", "gpt-4-turbo","gpt-3.5-turbo"]),
    "NVIDIA": st.selectbox("NVIDIA Model", ["llama2-70b", "mixtral-8x7b", "meta/llama-3.1-405b-instruct"]),
    "Groq": st.selectbox("Groq Model", ["llama3-groq-70b-8192-tool-use-preview", "mixtral-8x7b", ""])
}

async def stream_response(url, placeholder):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async for line in response.content:
                if line:
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line.startswith("data: "):
                        data = decoded_line[6:]
                        if data != "[DONE]":
                            placeholder.markdown(data)
                        else:
                            break

async def update_timer(provider, start_time, timer_placeholder):
    while True:
        elapsed = asyncio.get_event_loop().time() - start_time
        timer_placeholder.text(f"{provider} Time: {elapsed:.2f}s")
        await asyncio.sleep(0.1)

async def process_llm(provider, query, model, placeholder, timer_placeholder):
    url = f"{BACKEND_URL}/stream/{provider.lower()}?query={query}&model={model}"
    start_time = asyncio.get_event_loop().time()
    await asyncio.gather(
        stream_response(url, placeholder),
        update_timer(provider, start_time, timer_placeholder)
    )

async def run_comparison():
    if query:
        placeholders = {provider: st.empty() for provider in model_types}
        timers = {provider: st.empty() for provider in model_types}

        tasks = [
            process_llm(provider, query, model_types[provider], placeholders[provider], timers[provider])
            for provider in model_types
        ]
        await asyncio.gather(*tasks)
    else:
        st.warning("Please enter a query.")

if st.button("Compare LLMs"):
    asyncio.run(run_comparison())