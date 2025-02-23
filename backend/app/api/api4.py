from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.services.data_queries import get_fund_table
from app.services.schemas import FundTableResponse
from app.core.database import get_db

router = APIRouter()

@router.get("/fund-table/")
def get_fund_table_api(
    department: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    sort_by: Optional[str] = "roi",
    order: Optional[str] = "desc",
    db: Session = Depends(get_db)
):
    results = get_fund_table(db, department, start_date, end_date, sort_by, order)

    return {
        "funds": [
            {
                "fund_description": r[0],
                "total_revenue": float(r[1]) if r[1] is not None else 0.0,
                "total_expenses": float(r[2]) if r[2] is not None else 0.0,
                "ratio": float(r[3]) if r[3] is not None else 0.0,
                "roi": float(r[4]) if r[4] is not None else 0.0,
            }
            for r in results
        ]
    }