from httpx import AsyncClient
from fastapi import HTTPException
from src.config.setting import settings  # Optional if used
import logging

logger = logging.getLogger(__name__)

class GeoService:
    """Handles location detection and greetings"""
    
    def __init__(self, http_client: AsyncClient):
        self.client = http_client
        self.cache = {}
    
    async def get_location(self, ip: str) -> dict:
        if not ip or ip == "127.0.0.1":
            ip = ""
        
        if ip in self.cache:
            return self.cache[ip]
        
        try:
            response = await self.client.get(
                f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,city",
                timeout=5.0
            )
            data = await response.json()  # <-- Fix here
            
            if data.get("status") != "success":
                raise ValueError("Location lookup failed")
            
            self.cache[ip] = data
            return data
        
        except Exception as e:
            logger.exception("Location service error")
            raise HTTPException(
                status_code=400,
                detail=f"Location service error: {str(e)}"
            )
    
    async def get_greeting(self, ip: str) -> str:
        location = await self.get_location(ip)
        country = location.get("country", "unknown location")
        country_code = location.get("countryCode", "").lower()
        
        greetings = {
            "us": "Hello",
            "gb": "Hello",
            "fr": "Bonjour",
            "es": "Hola",
            "de": "Hallo",
        }
        
        return f"{greetings.get(country_code, 'Hello')}! 👋 You're visiting from {country}"
