from httpx import AsyncClient, Timeout
from contextlib import asynccontextmanager
from src.config.setting import settings
from src.utils.logger import logger

async def get_http_client() -> AsyncClient:
    timeout = Timeout(30.0, connect=5.0)
    headers = {
        "User-Agent": f"AI-Portfolio-Backend/{settings.APP_VERSION}",
        "Accept": "application/json"
    }
    client = AsyncClient(
        timeout=timeout,
        headers=headers,
        follow_redirects=True
    )
    return client

# Instrumentation example (optional)
def instrument_http_client(client: AsyncClient):
    """Add logging/tracing to HTTP requests"""
    original_request = client.request
    
    async def wrapped_request(*args, **kwargs):
        logger.debug(f"Making request to {kwargs.get('url')}")
        try:
            response = await original_request(*args, **kwargs)
            logger.debug(f"Response from {kwargs.get('url')}: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"Request failed to {kwargs.get('url')}: {str(e)}")
            raise
    
    client.request = wrapped_request
    return client