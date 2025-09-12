import os
import httpx

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

async def chat_groq(messages, model: str = "gpt-oss:20b") -> str:
    if not GROQ_API_KEY:
        raise RuntimeError("Groq API key not set.")
    payload = {
        "model": model,
        "messages": messages,
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        groq_resp = await client.post(GROQ_API_URL, json=payload, headers=headers)
        groq_resp.raise_for_status()
        data = groq_resp.json()
        return data["choices"][0]["message"]["content"]
