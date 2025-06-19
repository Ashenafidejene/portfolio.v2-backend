from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from src.dependencies.llm_service import get_llm_service
from src.services.llm_service import LLMService
from src.utils.http_client import get_http_client
from src.models.schemas import ProjectQuery, LLMResponse, ErrorResponse
from fastapi import status

router = APIRouter(
    prefix="/projects",
    tags=["Project Q&A"],
    responses={
        404: {"model": ErrorResponse, "description": "Project not found"}
    }
)

PROJECTS_DB = {
    "llm-gateway": "A FastAPI backend that routes queries to multiple LLMs...",
    "ai-portfolio": "Next.js portfolio with AI-powered features..."
}

@router.post("/ask", response_model=LLMResponse)
async def ask_about_project(
    query: ProjectQuery,
    llm_service: LLMService = Depends(get_llm_service)  # ✅ fix here too
):
    """
    Get AI-powered answers about specific projects
    
    - **project_id**: ID of project (e.g. 'llm-gateway')
    - **question**: Your question about the project
    """
    if query.project_id not in PROJECTS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    context = f"Project: {PROJECTS_DB[query.project_id]}\nQuestion: {query.question}"
    response = await llm_service.call_llm(context)
    
    return LLMResponse(
        response=response,
        model_used="chatgpt",  # Default for project Q&A
        timestamp=datetime.now()
    )