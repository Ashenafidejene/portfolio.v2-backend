from httpx import AsyncClient
from src.core.llm import deepseek, gemini, chatgpt
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class LLMService:
    """Orchestrates LLM API calls with failover logic"""

    def __init__(self, http_client: AsyncClient):
        self.client = http_client

    async def call_llm(self, query: str, preferred_model: str = "deepseek") -> str:
        models = {
            "deepseek": deepseek.call,
            "gemini": gemini.call,
            "chatgpt": chatgpt.call
        }

        if preferred_model not in models:
            raise HTTPException(status_code=400, detail=f"Unsupported model: {preferred_model}")

        try:
            return await models[preferred_model](self.client, query)
        except Exception as primary_error:
            logger.warning(f"{preferred_model} failed: {primary_error}")

            errors = {}
            for model_name, model_func in models.items():
                if model_name != preferred_model:
                    try:
                        return await model_func(self.client, query)
                    except Exception as e:
                        logger.warning(f"{model_name} also failed: {e}")
                        errors[model_name] = str(e)

            raise HTTPException(
                status_code=503,
                detail=f"All LLM providers failed. Primary error: {str(primary_error)}. "
                       f"Secondary errors: {errors}"
            )
