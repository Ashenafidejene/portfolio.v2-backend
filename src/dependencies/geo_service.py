# src/dependencies/geo_service.py
from fastapi import Depends
from httpx import AsyncClient
from src.services.geo_service import GeoService
from src.utils.http_client import get_http_client

async def get_geo_service(client: AsyncClient = Depends(get_http_client)) -> GeoService:
    return GeoService(client)
