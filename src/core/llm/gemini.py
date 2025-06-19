from httpx import AsyncClient
from src.config.setting import settings


async def call(client: AsyncClient, query: str) -> str:
    """Call Gemini API with user query"""
    response = await client.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={settings.GEMINI_API_KEY}",
        json={"contents": [{"parts": [{"text": query}]}]},
        timeout=30.0
    )
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]