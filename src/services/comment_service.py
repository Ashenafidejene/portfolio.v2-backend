from firebase_admin import db
from fastapi import HTTPException
from src.core.auth import verify_firebase_token
from src.config.setting import settings
from datetime import datetime

class CommentService:
    """Handles comment operations with Firebase"""
    
    def __init__(self):
        self.ref = db.reference("/comments")
    
    async def add_comment(self, token: str, text: str) -> dict:
        """Add authenticated comment to Firebase"""
        try:
            user = verify_firebase_token(token)
            comment_ref = self.ref.push()
            comment_ref.set({
                "text": text,
                "author": user["email"],
                "timestamp": datetime.utcnow().isoformat(),
                "likes": 0,
                "dislikes": 0
            })
            return {"id": comment_ref.key}
            
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Comment submission failed: {str(e)}"
            )
    
    async def vote_comment(self, comment_id: str, vote_type: str) -> bool:
        """Handle like/dislike votes"""
        if vote_type not in ("like", "dislike"):
            raise ValueError("Invalid vote type")
            
        try:
            self.ref.child(f"{comment_id}/{vote_type}s").transaction(
                lambda current: (current or 0) + 1
            )
            return True
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Vote failed: {str(e)}"
            )