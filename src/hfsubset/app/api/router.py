from fastapi import APIRouter

from src.hfsubset.app.api.routes import subset

api_router = APIRouter()
api_router.include_router(subset.router, prefix="/subset", tags=["v20.1 Hfsubset"])
