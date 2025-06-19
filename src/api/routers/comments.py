from fastapi import APIRouter, Depends, HTTPException
from src.services.comment_service import CommentService
from src.models.schemas import (
    CommentCreate,
    CommentResponse,
    VoteRequest,
    ErrorResponse
)
from fastapi import status

router = APIRouter(
    prefix="/comments",
    tags=["Guestbook"],
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        400: {"model": ErrorResponse, "description": "Invalid request"}
    }
)

@router.post("", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment: CommentCreate,
    comment_service: CommentService = Depends(CommentService)
):
    """Add a new comment to the guestbook"""
    try:
        comment_id = await comment_service.add_comment(comment.token, comment.text)
        return await comment_service.get_comment(comment_id["id"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to add comment: {str(e)}"
        )

@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
async def vote_comment(
    vote: VoteRequest,
    comment_service: CommentService = Depends(CommentService)
):
    """Like/dislike a comment"""
    success = await comment_service.vote_comment(vote.comment_id, vote.vote_type)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vote failed"
        )