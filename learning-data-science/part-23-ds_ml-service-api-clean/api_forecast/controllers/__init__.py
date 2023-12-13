""""
    author
"""

from fastapi import APIRouter #type: ignore
from api_forecast.controllers import ping

api_router = APIRouter() 

api_router.include_router(ping.router, tags=["api-analytics"])

