from fastapi import HTTPException, status
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError

def verify_firebase_token(token: str) -> dict:
    """Verify Firebase JWT token"""
    try:
        decoded_token = auth.verify_id_token(token)
        return {
            "uid": decoded_token["uid"],
            "email": decoded_token.get("email"),
            "name": decoded_token.get("name")
        }
    except (ValueError, FirebaseError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e