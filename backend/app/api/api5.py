from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.services.data_queries import get_net_profit_by_time
from app.services.schemas import NetProfitResponse
from app.core.database import get_db

router = APIRouter()

@router.get("/net-profit/", response_model=NetProfitResponse)
def get_net_profit_api(
    department: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    
    results = get_net_profit_by_time(db, department, start_date, end_date)

    times = [r[0] for r in results]
    net_profits = [float(r[1]) for r in results]

    return {"times": times, "net_profits": net_profits}
