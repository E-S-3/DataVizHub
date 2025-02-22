from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.core.models import Ledger, Department, CostCenter

############ API 1 ############ 
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

############ API 2 ############ 
def get_top_budget_departments(db: Session, department_id=None):
    """ Get top 10 departments by total expenditure. If a department is selected, return its top cost centers (CCD). """

    query = db.query(
        Department.department_name,
        func.sum(Ledger.amount).label("total_expenditure")
    ).join(Department, Ledger.department_id == Department.department_id)

    if department_id:
        # Get top CCDs by expenditure for a selected department
        query = db.query(
            CostCenter.cost_center_description,
            func.sum(Ledger.amount).label("total_expenditure")
        ).join(CostCenter, Ledger.cost_center_id == CostCenter.cost_center_id
        ).filter(Ledger.department_id == department_id)
    
    query = query.group_by(Department.department_name if not department_id else CostCenter.cost_center_description
    ).order_by(func.sum(Ledger.amount).desc()
    ).limit(10)

    return query.all()



############ API 3 ############ 
def get_revenue_expenses_by_year(db: Session, department_id=None):
    """ Get revenue and expenses per year. If department_id is given, filter data. """

    query = db.query(
        func.year(Ledger.general_ledger_date).label("year"),
        func.sum(case((Ledger.ledger_description == "Revenues", Ledger.amount), else_=0)).label("total_revenue"),
        func.sum(case((Ledger.ledger_description == "Expenses", Ledger.amount), else_=0)).label("total_expenses")
    ).select_from(Ledger)

    if department_id:
        query = query.filter(Ledger.department_id == department_id)

    query = query.group_by(func.year(Ledger.general_ledger_date)).order_by(func.year(Ledger.general_ledger_date))

    return query.all()