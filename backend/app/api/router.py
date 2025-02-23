from fastapi import APIRouter
from app.api import api1, api2, api3, api4, api5


router = APIRouter()
router.include_router(api1.router, prefix="/api", tags=["ROI"])
router.include_router(api2.router, prefix="/api", tags=["Top Budget"])
router.include_router(api3.router, prefix="/api", tags=["Rev & Exp"])
router.include_router(api4.router, prefix="/api", tags=["Funds"])
router.include_router(api5.router, prefix="/api", tags=["Net Profit"])
