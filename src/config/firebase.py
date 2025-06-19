import firebase_admin
from firebase_admin import credentials, db
from src.config.setting import settings
from src.utils.logger import logger

def init_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(
                cred,
                {
                    "databaseURL": settings.FIREBASE_DATABASE_URL
                }
            )
            logger.info("Firebase initialized successfully")
    except Exception as e:
        logger.error(f"Firebase initialization failed: {str(e)}")
        raise