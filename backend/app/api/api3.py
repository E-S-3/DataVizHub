from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.services.data_queries import get_top_budget_departments, get_revenue_expenses_by_year
from app.services.schemas import BudgetResponse, RevenueExpenseResponse
from app.core.database import get_db

router = APIRouter()

@router.get("/revenue-expenses/", response_model=RevenueExpenseResponse)
def get_revenue_expenses(department: Optional[int] = None, db: Session = Depends(get_db)):
    results = get_revenue_expenses_by_year(db, department)
    
    years = [r[0] for r in results]
    revenues = [float(r[1]) for r in results]
    expenses = [float(r[2]) for r in results]

    return {"years": years, "revenues": revenues, "expenses": expenses}
