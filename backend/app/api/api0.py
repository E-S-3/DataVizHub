from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.data_queries import get_departments_and_ledger_dates
from app.core.database import get_db

router = APIRouter()

@router.get("/initialise")
def fetch_departments_ledger_dates(db: Session = Depends(get_db)):
    return get_departments_and_ledger_dates(db)
