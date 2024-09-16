import streamlit as st
from apps.basic_comparison import app as basic_comparison
from apps.metrics_charts import app as metrics_charts

# Deshabilitar completamente la detección automática de páginas
st.set_page_config(page_title="LLM Comparison Tool", layout="wide")

# Ocultar todos los elementos extra
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Crear un diccionario de páginas
PAGES = {
    "📊 Metrics & Charts": metrics_charts,
    "📝 Text Response": basic_comparison,
    "🤌 About the Project": "project",
    "🧑‍💻 About Me": "about_me"
}

# Barra lateral para navegación
selection = st.sidebar.radio("Choose a comparison mode:", list(PAGES.keys()))

# Definir las secciones de 'About'
def about_project():
    st.title("About the Project")
    st.write("""
        Welcome to **LLM Arena**!
        This is where the heavyweights of language models go head-to-head: OpenAI, NVIDIA, and Groq. 
        the goal? To find out which model and provider is the fastest and most efficient in terms of both speed and the number of words generated..             
        By analyzing these data points, users can make informed decisions on which LLM is best suited for their needs.
    """)
    st.image("assets/demo.gif", width=750)

def about_me():
    st.title("About Me")
    
    # Add your image (replace with your own image path or link)
    st.image("assets/image.png", width=150)    
    st.write("""
        I'm Fran, an 🤖 AI Advocate, Speaker and seasoned Full Stack Developer who simplifies AI and coding into practical skills for everyone. 
        I'm all about creating AI solutions that work for you and explaining tech in ways that stick. 
        
        Feel free to connect with me on:
        - [Twitter](https://x.com/Farmacod)
        - [LinkedIn](https://www.linkedin.com/in/gutierrezfrancois/)
        - [GitHub](https://github.com/DrZuzzjen)
    """)



# Mostrar la página seleccionada
if PAGES[selection] == "project":
    about_project()
elif PAGES[selection] == "about_me":
    about_me()
else:
    PAGES[selection]()
