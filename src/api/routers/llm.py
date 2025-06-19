# from httpx import AsyncClient
# from datetime import datetime
# from fastapi import APIRouter, Depends, HTTPException

# from src.services.llm_service import LLMService
# from src.utils.http_client import get_http_client
# from src.models.schemas import LLMQuery, LLMResponse, ErrorResponse
# from fastapi import status
# router = APIRouter(
#     prefix="/llm",
#     tags=["LLM Endpoints"],
#     responses={
#         429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
#         503: {"model": ErrorResponse, "description": "Service unavailable"}
#     }
# )

# @router.post("/ask", response_model=LLMResponse)
# async def ask_question(
#     query: LLMQuery,
#     llm_service: LLMService = Depends(LLMService),
#     client: AsyncClient = Depends(get_http_client)
# ):
#     """
#     Query any supported LLM (DeepSeek, Gemini, or ChatGPT)
    
#     - **query**: Your question/prompt (1-1000 chars)
#     - **model**: Preferred LLM (default: deepseek)
#     """
#     try:
#         response = await llm_service.call_llm(query.query, query.model)
#         return LLMResponse(
#             response=response,
#             model_used=query.model,
#             timestamp=datetime.now()
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#             detail=f"LLM service error: {str(e)}"
#         )

# llm.py
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime

from src.models.schemas import LLMQuery, LLMResponse, ErrorResponse
from src.services.llm_service import LLMService
from src.dependencies.llm_service import get_llm_service  # ✅ use the dependency function

router = APIRouter(
    prefix="/llm",
    tags=["LLM Endpoints"],
    responses={
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        503: {"model": ErrorResponse, "description": "Service unavailable"}
    }
)

@router.post("/ask", response_model=LLMResponse)
async def ask_question(
    query: LLMQuery,
    llm_service: LLMService = Depends(get_llm_service),  # ✅ inject service properly
):
    try:
        response = await llm_service.call_llm(query.query, query.model)
        return LLMResponse(
            response=response,
            model_used=query.model,
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"LLM service error: {str(e)}"
        )
