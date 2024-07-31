from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from services.openai_service import OpenAIService
from services.nvidia_service import NVIDIAService
from services.groq_service import GroqService

app = FastAPI()

openai_service = OpenAIService()
nvidia_service = NVIDIAService()
groq_service = GroqService()

async def stream_llm(service, query: str, model: str):
    async for chunk in service.generate(query, model):
        yield f"data: {chunk}\n\n"
    yield "data: [DONE]\n\n"

@app.get("/stream/{provider}")
async def stream_llm_endpoint(provider: str, query: str, model: str):
    if provider == "openai":
        service = openai_service
    elif provider == "nvidia":
        service = nvidia_service
    elif provider == "groq":
        service = groq_service
    else:
        raise HTTPException(status_code=400, detail="Invalid provider")

    return StreamingResponse(stream_llm(service, query, model), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)