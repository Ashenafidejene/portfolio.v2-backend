from src.config.setting import settings
from httpx import AsyncClient

async def call(client: AsyncClient, query: str) -> str:
    """Call DeepSeek API with user query"""
    response = await client.post(
        "https://api.deepseek.com/v1/chat",
        json={
            "messages": [{"role": "user", "content": query}],
            "model": "deepseek-chat"
        },
        headers={"Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"},
        timeout=30.0
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]