from fastapi import APIRouter
from app.api import api1

router = APIRouter()
router.include_router(api1.router, prefix="/api", tags=["ROI"])

