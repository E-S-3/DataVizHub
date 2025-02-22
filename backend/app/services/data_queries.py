# from sqlalchemy.orm import Session
# from sqlalchemy import func
# from app.core.models import Ledger, Department, CostCenter

# def get_top_roi_departments(db: Session, start_date=None, end_date=None):
#     query = db.query(
#         Department.department_name,
#         func.sum(Ledger.amount).label("total_revenue")
#     ).join(Department, Ledger.department_id == Department.department_id)
    
#     if start_date and end_date:
#         query = query.filter(Ledger.general_ledger_date.between(start_date, end_date))
    
#     query = query.group_by(Department.department_name).order_by(func.sum(Ledger.amount).desc()).limit(5)
#     return query.all()

# def get_top_roi_cost_centers(db: Session, department_id, start_date=None, end_date=None):
#     query = db.query(
#         CostCenter.cost_center_description,
#         func.sum(Ledger.amount).label("total_revenue")
#     ).join(CostCenter, Ledger.cost_center_id == CostCenter.cost_center_id)
    
#     query = query.filter(Ledger.department_id == department_id)
    
#     if start_date and end_date:
#         query = query.filter(Ledger.general_ledger_date.between(start_date, end_date))
    
#     query = query.group_by(CostCenter.cost_center_description).order_by(func.sum(Ledger.amount).desc()).limit(5)
#     return query.all()

from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.core.models import Ledger, Department, CostCenter

def get_top_roi_departments(db: Session, start_date=None, end_date=None):
    query = db.query(
        Department.department_name,
        (func.sum(
            case(
                (Ledger.ledger_description == "Revenues", Ledger.amount),
                else_=0
            )
        ) - func.sum(
            case(
                (Ledger.ledger_description == "Expenses", Ledger.amount),
                else_=0
            )
        )).label("roi")
    ).join(Department, Ledger.department_id == Department.department_id)
    
    if start_date and end_date:
        query = query.filter(Ledger.general_ledger_date.between(start_date, end_date))
    
    query = query.group_by(Department.department_name).order_by(func.sum(Ledger.amount).desc()).limit(5)
    return query.all()

def get_top_roi_cost_centers(db: Session, department_id, start_date=None, end_date=None):
    query = db.query(
        CostCenter.cost_center_description,
        (func.sum(
            case(
                (Ledger.ledger_description == "Revenues", Ledger.amount),
                else_=0
            )
        ) - func.sum(
            case(
                (Ledger.ledger_description == "Expenses", Ledger.amount),
                else_=0
            )
        )).label("roi")
    ).join(CostCenter, Ledger.cost_center_id == CostCenter.cost_center_id)
    
    query = query.filter(Ledger.department_id == department_id)
    
    if start_date and end_date:
        query = query.filter(Ledger.general_ledger_date.between(start_date, end_date))
    
    query = query.group_by(CostCenter.cost_center_description).order_by(func.sum(Ledger.amount).desc()).limit(5)
    return query.all()
