from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Literal
from backend.infrastructure.ai.groq_client import chat_groq
from backend.infrastructure.ai.perplexity_client import chat_perplexity
from backend.infrastructure.ai.openai_client import chat_openai
from backend.infrastructure.ai.cursor_client import chat_cursor

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    provider: Optional[Literal["groq", "perplexity", "claude", "openai", "cursor", "copilot"]] = "groq"
    model: Optional[str] = None

class ChatResponse(BaseModel):
    response: str

@router.post("/chat/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        if request.provider == "groq":
            model = request.model or "llama3-8b-8192"
            answer = await chat_groq(request.message, model=model)
        elif request.provider == "perplexity":
            model = request.model or "pplx-7b-online"
            answer = await chat_perplexity(request.message, model=model)
        elif request.provider == "openai":
            model = request.model or "gpt-4"
            answer = await chat_openai(request.message, model=model)
        elif request.provider == "cursor":
            model = request.model or "cursor-pro"
            answer = await chat_cursor(request.message, model=model)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown provider: {request.provider}")
        return ChatResponse(response=answer)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"API error: {str(e)}")
