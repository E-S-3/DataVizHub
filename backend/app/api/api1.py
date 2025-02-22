from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.data_queries import get_top_roi_departments, get_top_roi_cost_centers
from app.services.schemas import ROIResponse
from app.core.database import get_db

router = APIRouter()

@router.get("/top-roi/", response_model=ROIResponse)
def get_top_roi(department: Optional[int] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, db: Session = Depends(get_db)):
    if department:
        results = get_top_roi_cost_centers(db, department, start_date, end_date)
    else:
        results = get_top_roi_departments(db, start_date, end_date)
    
    labels = [r[0] for r in results]
    values = [float(r[1]) for r in results]
    
    return {"labels": labels, "values": values}