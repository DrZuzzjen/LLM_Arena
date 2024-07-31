from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os

class GroqService:
    def __init__(self):
        self.client = ChatGroq(
            api_key=os.environ.get("GROQ_API_KEY"),
            streaming=True
        )

    async def generate(self, query: str, model: str):
        try:
            async for chunk in self.client.astream([HumanMessage(content=query)], model=model):
                yield chunk.content
        except Exception as e:
            yield f"Error: {str(e)}"