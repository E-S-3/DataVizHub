from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.services.data_queries import get_top_budget_departments
from app.services.schemas import BudgetResponse
from app.core.database import get_db

router = APIRouter()

@router.get("/top-budget/", response_model=BudgetResponse)
def get_top_budget(
    department: Optional[int] = None, 
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None, 
    db: Session = Depends(get_db)):
    results = get_top_budget_departments(db, department, start_date, end_date)
    
    labels = [r[0] for r in results]
    values = [float(r[1]) for r in results]
    
    return {"labels": labels, "values": values}