#openai_service.py
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os

class OpenAIService:
    def __init__(self):
        self.client = ChatOpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            streaming=True
        )

    async def generate(self, query: str, model: str):
        try:
            async for chunk in self.client.astream([HumanMessage(content=query)], model=model):
                yield chunk.content
        except Exception as e:
            yield f"Error: {str(e)}"