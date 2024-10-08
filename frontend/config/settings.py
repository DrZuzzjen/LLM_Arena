import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = "http://backend:8000"

# API Keys (these will be populated from environment variables in production)
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
NVIDIA_API_KEY=os.getenv("NVIDIA_API_KEY")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
HUMAN_REVIEW = os.getenv('HUMAN_REVIEW', 'True').lower() == 'true'
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
LANGCHAIN_TRACING_V2 = True
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")


OPENAI_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-3.5-turbo-instruct",
    "gpt-4",
    "gpt-4-turbo",
]

NVIDIA_MODELS = [
    "meta/llama-3.1-8b-instruct",
    "mistralai/mixtral-8x22b-instruct-v0.1",
    "meta/llama-3.1-405b-instruct",
    "nv-mistralai/mistral-nemo-12b-instruct",
    "google/gemma-2-9b-it",
    "microsoft/phi-3-medium-128k-instruct"
]

GROQ_MODELS = [
      "llama3-70b-8192",
      "llama-3.1-70b-versatile",
      "llama3-groq-70b-8192-tool-use-preview",
      "llama-3.1-405b-reasoning",
      "gemma2-9b-it",
      "gemma-7b-it",
      "mixtral-8x7b-32768"
    ]
