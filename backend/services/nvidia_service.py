from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.messages import HumanMessage
import os

class NVIDIAService:
    def __init__(self):
        self.client = ChatNVIDIA(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.environ.get("NVIDIA_API_KEY"),
            streaming=True
        )

    async def generate(self, query: str, model: str):
        try:
            async for chunk in self.client.astream([HumanMessage(content=query)], model=model):
                yield chunk.content
        except Exception as e:
            yield f"Error: {str(e)}"