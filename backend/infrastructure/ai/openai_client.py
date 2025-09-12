import os
import httpx

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

async def chat_openai(message: str, model: str = "gpt-4") -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OpenAI API key not set.")
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": message}
        ]
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(OPENAI_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
