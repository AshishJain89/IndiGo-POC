from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Literal, List, Dict
from backend.infrastructure.ai.groq_client import chat_groq
from backend.infrastructure.ai.perplexity_client import chat_perplexity
from backend.infrastructure.ai.openai_client import chat_openai
from backend.infrastructure.ai.cursor_client import chat_cursor
from backend.infrastructure.logging.logging_middleware import logger

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    provider: Optional[Literal["groq", "perplexity", "claude", "openai", "cursor", "copilot"]] = "groq"
    history: Optional[List[Dict[str, str]]] = None  # Each message: {"role": "user"|"assistant", "content": str}
    model: Optional[str] = None

class ChatResponse(BaseModel):
    response: str

@router.post("/chat/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        logger.info(f"Chat request: provider={request.provider}, model={request.model}, message={request.message}, history_length={len(request.history) if request.history else 0}")
        # Prepare messages for context (history + current message)
        messages = request.history or []
        messages.append({"role": "user", "content": request.message})
        if request.provider == "groq":
            model = getattr(request, "model", None) or "gemma2-9b-it"
            answer = await chat_groq(messages, model=model)
        elif request.provider == "perplexity":
            model = getattr(request, "model", None) or "pplx-7b-online"
            answer = await chat_perplexity(messages, model=model)
        elif request.provider == "openai":
            model = getattr(request, "model", None) or "gpt-4"
            answer = await chat_openai(messages, model=model)
        elif request.provider == "cursor":
            model = getattr(request, "model", None) or "cursor-pro"
            answer = await chat_cursor(messages, model=model)
        else:
            logger.error(f"Unknown provider: {request.provider}")
            raise HTTPException(status_code=400, detail=f"Unknown provider: {request.provider}")
        logger.info(f"Chat response: {answer}")
        return ChatResponse(response=answer)
    except Exception as e:
        logger.exception(f"Chat API error: {str(e)}")
        raise HTTPException(status_code=502, detail=f"API error: {str(e)}")
