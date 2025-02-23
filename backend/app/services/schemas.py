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
    
class FundEntry(BaseModel):
    fund_description: str
    total_revenue: float
    total_expenses: float
    ratio: float
    roi: float

class FundTableResponse(BaseModel):
    funds: List[FundEntry]

class NetProfitResponse(BaseModel):
    times: List[int] 
    net_profits: List[float]