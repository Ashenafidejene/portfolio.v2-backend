#from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import List

#load_dotenv(dotenv_path=".env")  # Optional when using env_file

class Settings(BaseSettings):
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    CORS_ORIGINS: List[str] = ["*"]
    
    DEEPSEEK_API_KEY: str
    GEMINI_API_KEY: str
    OPENAI_API_KEY: str

    FIREBASE_CREDENTIALS_PATH: str = "./firebase-key.json"
    FIREBASE_DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
