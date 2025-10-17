
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

AGENT_CARD = {
    "name": "Ollama Gemma3 FastA2A Agent",
    "description": "A minimal FastA2A-compatible agent that forwards prompts to Ollama Gemma3.",
    "version": "1.0",
    "a2a_endpoint": "/a2a",
    "protocols": ["FastA2A v0.2"],
    "author": "Agent Zero"
}

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://host.docker.internal:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma3")

@app.get("/.well-known/agent.json")
def agent_card():
    return JSONResponse(content=AGENT_CARD)

@app.post("/a2a")
async def a2a_endpoint(request: Request):
    data = await request.json()
    prompt = data.get("prompt") or data.get("message")
    if not prompt:
        return JSONResponse(status_code=400, content={"error": "Missing 'prompt' or 'message' in request."})
    ollama_payload = {"model": OLLAMA_MODEL, "prompt": prompt}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(OLLAMA_URL, json=ollama_payload, timeout=60)
            resp.raise_for_status()
            ollama_data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
            # Ollama returns streaming by default; force non-stream in payload if needed
            if "response" in ollama_data:
                answer = ollama_data["response"]
            elif "message" in ollama_data:
                answer = ollama_data["message"]
            else:
                answer = resp.text
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
    # FastA2A response format: {"text": ...}
    return JSONResponse(content={"text": answer})
