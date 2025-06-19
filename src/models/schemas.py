from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, Literal

class LLMQuery(BaseModel):
    """Request model for LLM queries"""
    query: str = Field(..., min_length=1, max_length=1000, 
                      example="Explain FastAPI in simple terms")
    model: Literal["deepseek", "gemini", "chatgpt"] = "deepseek"

class LLMResponse(BaseModel):
    """Response model for LLM queries"""
    response: str
    model_used: str
    timestamp: datetime

class ProjectQuery(BaseModel):
    """Request model for project questions"""
    project_id: str = Field(..., example="llm-gateway")
    question: str = Field(..., min_length=5, max_length=500,
                         example="How did you handle rate limiting?")

class LocationResponse(BaseModel):
    """Response model for location service"""
    ip: str
    country: str
    country_code: str
    city: Optional[str]
    greeting: str

class CommentCreate(BaseModel):
    """Request model for creating comments"""
    text: str = Field(..., min_length=1, max_length=500)
    token: str = Field(..., description="Firebase JWT token")

class CommentResponse(BaseModel):
    """Response model for comments"""
    id: str
    text: str
    author: EmailStr
    timestamp: datetime
    likes: int = 0
    dislikes: int = 0

class VoteRequest(BaseModel):
    """Request model for voting"""
    comment_id: str
    vote_type: Literal["like", "dislike"]
    token: str = Field(..., description="Firebase JWT token")

class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str
    code: int
    suggestion: Optional[str] = None