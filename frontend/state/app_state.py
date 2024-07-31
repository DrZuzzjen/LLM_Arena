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