from fastapi import HTTPException
import httpx
from src.config.setting import settings

async def call(client: httpx.AsyncClient, query: str) -> str:
    try:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": query}]
            },
            headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
            timeout=30.0
        )
        response.raise_for_status()
        data = await response.json()
        return data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"OpenAI API error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
