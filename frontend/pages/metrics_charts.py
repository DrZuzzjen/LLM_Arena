# File: app.py
import streamlit as st
from state.app_state import get_app_state
from components.input_section import render_input_section
from components.llm_cards import render_llm_cards
from components.comparison_charts import render_comparison_charts
from utils.llm_comparison import run_comparison

def main():
    st.title("Enhanced LLM Comparison with Metrics & Charts")
    
    app_state = get_app_state()
    
    query, models = render_input_section(app_state)
    
    if st.button("Compare LLMs"):
        run_comparison(query, models)
    
    render_llm_cards(app_state.llm_responses)
    render_comparison_charts(app_state.charts_data)

if __name__ == "__main__":
    main()

# File: state/app_state.py
import streamlit as st
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class LLMResponse:
    provider: str
    model: str
    response: str = ""
    metrics: Dict[str, Any] = field(default_factory=dict)
    finish_order: int = None

@dataclass
class AppState:
    query: str = ""
    llm_responses: Dict[str, LLMResponse] = field(default_factory=dict)
    charts_data: Dict[str, Any] = field(default_factory=dict)

    def update_llm_response(self, provider: str, **kwargs):
        if provider not in self.llm_responses:
            self.llm_responses[provider] = LLMResponse(provider=provider, model=kwargs.get('model', ''))
        for key, value in kwargs.items():
            setattr(self.llm_responses[provider], key, value)

    def update_charts_data(self):
        # Logic to update charts data based on llm_responses
        pass

def get_app_state():
    if 'app_state' not in st.session_state:
        st.session_state.app_state = AppState()
    return st.session_state.app_state

# File: components/input_section.py
import streamlit as st
from state.app_state import AppState

def render_input_section(app_state: AppState):
    query = st.text_area("Enter your query:", value=app_state.query)
    models = {
        "OpenAI": st.selectbox("OpenAI Model", ["gpt-3.5-turbo", "gpt-4"]),
        "NVIDIA": st.selectbox("NVIDIA Model", ["llama-2-70b-hf", "mixtral-8x7b-instruct-v0.1"]),
        "Groq": st.selectbox("Groq Model", ["llama2-70b-4096", "mixtral-8x7b-32768"])
    }
    return query, models

# File: components/llm_cards.py
import streamlit as st
from state.app_state import LLMResponse

def render_llm_card(llm_response: LLMResponse):
    # Render LLM card based on llm_response data
    st.write(f"{llm_response.provider} - {llm_response.model}")
    st.write(f"Response: {llm_response.response}")
    st.write(f"Metrics: {llm_response.metrics}")
    st.write(f"Finish Order: {llm_response.finish_order}")

def render_llm_cards(llm_responses):
    for provider, llm_response in llm_responses.items():
        render_llm_card(llm_response)

# File: components/comparison_charts.py
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

# File: utils/llm_comparison.py
import asyncio
import streamlit as st
from state.app_state import get_app_state

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