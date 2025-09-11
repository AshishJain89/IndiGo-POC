from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from infrastructure.ai.groq_client import chat_groq

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    provider: Optional[str] = "groq"
    model: Optional[str] = "gpt-oss:20b"

class ChatResponse(BaseModel):
    response: str

@router.post("/chat/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Add more providers here as needed
    if request.provider == "groq":
        try:
            model = request.model if request.model is not None else "gpt-oss:20b"
            answer = await chat_groq(request.message, model=model)
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Groq API error: {str(e)}")
        return ChatResponse(response=answer)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown provider: {request.provider}")
