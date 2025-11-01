import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
from datetime import datetime

app = FastAPI()

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://host.docker.internal:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma3")

@app.post("/a2a", response_class=JSONResponse)
async def a2a_endpoint(request: Request):
    data = await request.json()
    prompt = data.get("prompt") or data.get("message")
    if not prompt:
        return JSONResponse(status_code=400, content={"error": "Missing 'prompt' or 'message' in request."})
    ollama_payload = {"model": OLLAMA_MODEL, "prompt": prompt}
    try:
        async with httpx.AsyncClient() as client:
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

@app.get("/.well-known/agent.json", response_class=JSONResponse)
def agent_metadata():
    return {
        "@context": "https://a2a.org/agent.schema.jsonld",
        "id": "http://localhost:8000/.well-known/agent.json",
        "type": "Agent",
        "name": "Ollama Gemma3 FastA2A Agent",
        "description": "A minimal FastA2A-compatible agent that forwards prompts to Ollama Gemma3.",
        "version": "1.0.0",
        "protocol": { "name": "FastA2A", "version": "0.2" },
        "endpoints": {
            "a2a": "http://localhost:8000/a2a",
            "metadata": "http://localhost:8000/.well-known/agent.json",
            "health": "http://localhost:8000/healthz"
        },
        "capabilities": ["text-generation", "question-answering"],
        "maintainer": { "name": "Agent Zero", "email": "contact@example.com" },
        "license": "Apache-2.0",
        "created": datetime.utcnow().isoformat() + 'Z',
        "build": {
            "commit": os.environ.get("GIT_COMMIT", "<git-commit-sha>"),
            "time": datetime.utcnow().isoformat() + 'Z'
        }
    }
