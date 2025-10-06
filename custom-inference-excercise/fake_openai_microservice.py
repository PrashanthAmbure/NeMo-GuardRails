# fake_openai_microservice.py
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from langchain_ollama import ChatOllama
import uvicorn
import time

app = FastAPI()
TOKENS = {}

@app.post("/v1/auth/token")
def get_token(data: dict):
    # api_key = data.get("api_key")
    # if not api_key or not api_key.startswith("sk-"):
    #     raise HTTPException(status_code=401, detail="Invalid API key")

    token = f"token-{int(time.time())}"
    TOKENS[token] = time.time()
    return {"access_token": token}

@app.post("/v1/chat/completions")
def chat_completions(authorization: str = Header(None), payload: dict = {}):
    print(f"PAYLOAD: {payload}")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = authorization.replace("Bearer ", "")
    if token not in TOKENS:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    messages = payload.get("messages", [])
    last_user_message = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "Hi")
    reply = f"🤖 Echo from fake LLM: {last_user_message[::-1]}"

    return JSONResponse({
        "id": "chatcmpl-fake",
        "object": "chat.completion",
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": reply},
            "finish_reason": "stop"
        }],
        "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20}
    })

@app.get("/v1/ping")
def ping():
    return "pong"

from pydantic import BaseModel
from typing import Union, List
class ChatRequest(BaseModel):
    # prompt: str
    prompt: Union[str, List[str]]

@app.post("/v1/chat")
async def chat(request: ChatRequest):
    if isinstance(request.prompt, list):
        prompt_text = "\n".join(request.prompt)
    else:
        prompt_text = request.prompt
    model = ChatOllama(model='llama3', temperature=2.5)
    response = model.invoke(prompt_text)
    print(f"Response={response.content}")
    return JSONResponse({
        "response": response.content
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
