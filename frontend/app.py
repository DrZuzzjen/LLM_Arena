import streamlit as st
from pages import basic_comparison, metrics_charts

PAGES = {
    "Basic Comparison": basic_comparison,
    "Metrics & Charts": metrics_charts
}

def initialize_state():
    if 'app_state' not in st.session_state:
        st.session_state.app_state = {
            'query': '',
            'results': {},
            'current_page': 'Basic Comparison',
            'needs_update': {
                'basic_comparison': False,
                'metrics_charts': False
            }
        }

def main():
    st.set_page_config(page_title="LLM Comparison Tool", layout="wide")

    initialize_state()

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()), key='navigation')

    # Update current page in state
    if selection != st.session_state.app_state['current_page']:
        st.session_state.app_state['current_page'] = selection
        st.session_state.app_state['needs_update'][selection.lower().replace(' ', '_')] = True

    # Run the selected page
    page = PAGES[selection]
    page.app(st.session_state.app_state)

    # Reset update flags
    for key in st.session_state.app_state['needs_update']:
        st.session_state.app_state['needs_update'][key] = False

if __name__ == "__main__":
    main()