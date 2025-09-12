import os
import httpx

CURSOR_API_KEY = os.getenv("CURSOR_API_KEY")
CURSOR_API_URL = "https://api.cursor.sh/v1/chat/completions" # Placeholder URL

async def chat_cursor(message: str, model: str = "cursor-pro") -> str:
    if not CURSOR_API_KEY:
        raise RuntimeError("Cursor API key not set.")
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": message}
        ]
    }
    headers = {
        "Authorization": f"Bearer {CURSOR_API_KEY}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(CURSOR_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
