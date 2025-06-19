
from fastapi import Depends
from httpx import AsyncClient
from src.services.llm_service import LLMService
from src.utils.http_client import get_http_client

def get_llm_service(client: AsyncClient = Depends(get_http_client)) -> LLMService:
    return LLMService(client)
