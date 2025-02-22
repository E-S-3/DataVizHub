from fastapi import APIRouter
from app.api import api1, api2, api3


router = APIRouter()
router.include_router(api1.router, prefix="/api", tags=["ROI"])
router.include_router(api2.router, prefix="/api", tags=["Top Budget"])
router.include_router(api3.router, prefix="/api", tags=["Rev & Exp"])
