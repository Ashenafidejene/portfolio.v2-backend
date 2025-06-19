# src/api/routers/greet.py
from fastapi import APIRouter, Request, Depends, status
from httpx import AsyncClient
from src.services.geo_service import GeoService
from src.utils.http_client import get_http_client
from src.dependencies.geo_service import get_geo_service  # ✅ Import here
from src.models.schemas import LocationResponse, ErrorResponse

router = APIRouter(
    prefix="/greet",
    tags=["Location Services"],
    responses={400: {"model": ErrorResponse, "description": "Invalid IP address"}}
)

@router.get("", response_model=LocationResponse)
async def greet_user(
    request: Request,
    geo_service: GeoService = Depends(get_geo_service)  # ✅ FIXED
):
    """
    Get location-based greeting
    """
    ip = request.client.host
    location = await geo_service.get_location(ip)
    greeting = await geo_service.get_greeting(ip)

    return LocationResponse(
        ip=ip,
        country=location["country"],
        country_code=location["countryCode"],
        city=location.get("city"),
        greeting=greeting
    )
