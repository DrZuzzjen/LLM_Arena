from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

async def fake_stream_llm(query: str, model: str):
    words = query.split()
    for word in words:
        yield f"data: Streaming: {word}\n\n"
        await asyncio.sleep(0.5)
    yield "data: [DONE]\n\n"

@app.get("/stream/{provider}")
async def stream_llm(provider: str, query: str, model: str):
    return StreamingResponse(fake_stream_llm(query, model), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)