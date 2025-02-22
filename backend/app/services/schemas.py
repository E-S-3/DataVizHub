from pydantic import BaseModel
from typing import List, Optional

class ROIResponse(BaseModel):
    labels: List[str]
    values: List[float]

class BudgetResponse(BaseModel):
    labels: List[str]
    values: List[float]

class RevenueExpenseResponse(BaseModel):
    years: List[int]
    revenues: List[float]
    expenses: List[float]