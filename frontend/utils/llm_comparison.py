import asyncio
import streamlit as st
from state.app_state import get_app_state
from typing import Dict

async def stream_response(provider: str, model: str, query: str):
    app_state = get_app_state()
    # Simulated streaming logic
    for i in range(10):
        await asyncio.sleep(0.5)
        app_state.update_llm_response(provider, 
                                      model=model, 
                                      response=f"Partial response {i}",
                                      metrics={"time": i * 0.5, "tokens": i * 10})
        st.experimental_rerun()
    
    app_state.update_llm_response(provider, finish_order=len(app_state.llm_responses))
    app_state.update_charts_data()

def run_comparison(query: str, models: Dict[str, str]):
    app_state = get_app_state()
    app_state.query = query
    
    async def run_async():
        tasks = [stream_response(provider, model, query) for provider, model in models.items()]
        await asyncio.gather(*tasks)
    
    asyncio.run(run_async())