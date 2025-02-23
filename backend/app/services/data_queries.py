from sqlalchemy.orm import Session
from sqlalchemy import func, case, desc, asc, and_
from app.core.models import Ledger, Department, CostCenter, Fund

############ API 0 ############ 
def get_departments_and_ledger_dates(db: Session):
    departments = db.query(Department.department_id, Department.department_name).all()
    earliest_date = db.query(func.min(Ledger.general_ledger_date)).scalar()
    latest_date = db.query(func.max(Ledger.general_ledger_date)).scalar()

    return {
        "departments": [{"id": dept.department_id, "name": dept.department_name} for dept in departments],
        "earliest_date": earliest_date,
        "latest_date": latest_date
    }

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
    
    # Apply filters based on available start_date and end_date
    if start_date and end_date:
        query = query.filter(Ledger.general_ledger_date.between(start_date, end_date))
    elif start_date:
        query = query.filter(Ledger.general_ledger_date >= start_date)
    elif end_date:
        query = query.filter(Ledger.general_ledger_date <= end_date)
    
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
    
    # Apply filters based on available start_date and end_date
    if start_date and end_date:
        query = query.filter(Ledger.general_ledger_date.between(start_date, end_date))
    elif start_date:
        query = query.filter(Ledger.general_ledger_date >= start_date)
    elif end_date:
        query = query.filter(Ledger.general_ledger_date <= end_date)
    
    query = query.group_by(CostCenter.cost_center_description).order_by(func.sum(Ledger.amount).desc()).limit(5)
    return query.all()

############ API 2 ############ 
def get_top_budget_departments(db: Session, department_id=None, start_date=None, end_date=None):
    """ Get top 10 departments by total expenditure, ensuring only valid expenses are considered. """

    expense_case = case(
        (and_(Ledger.ledger_description == "Expenses", Ledger.amount > 0), Ledger.amount),
        else_=0
    )

    revenue_case = case(
        (and_(Ledger.ledger_description == "Revenues", Ledger.amount < 0), -Ledger.amount),
        else_=0
    )

    query = db.query(
        Department.department_name,
        func.sum(expense_case + revenue_case).label("total_expenditure")
    ).join(Department, Ledger.department_id == Department.department_id)

    if department_id:
        query = query.filter(Ledger.department_id == department_id)

    if start_date and end_date:
        query = query.filter(Ledger.general_ledger_date.between(start_date, end_date))

    query = query.group_by(Department.department_name
    ).order_by(func.sum(expense_case + revenue_case).desc()
    ).limit(10)

    return query.all()


############ API 3 ############ 
def get_revenue_expenses_by_year(db: Session, department_id=None, start_date=None, end_date=None):
    """ Get revenue and expenses per year. If department_id is given, filter data. """

    query = db.query(
        func.year(Ledger.general_ledger_date).label("year"),
        func.sum(case((Ledger.ledger_description == "Revenues", Ledger.amount), else_=0)).label("total_revenue"),
        func.sum(case((Ledger.ledger_description == "Expenses", Ledger.amount), else_=0)).label("total_expenses"),
    ).filter(Ledger.general_ledger_date.between(start_date, end_date) if start_date and end_date else True)

    if department_id:
        query = query.filter(Ledger.department_id == department_id)

    query = query.group_by(func.year(Ledger.general_ledger_date)).order_by(func.year(Ledger.general_ledger_date))
    
    return query.all()


############ API 4 ############ 
def get_fund_table(db: Session, department=None, start_date=None, end_date=None, sort_by="roi", order="desc"):
    """ Get fund description, expenses, revenues, ratio, and ROI with sorting, filtered by department. """

    total_revenue = func.sum(case((Ledger.ledger_description == "Revenues", Ledger.amount), else_=0)).label("total_revenue")
    total_expenses = func.sum(case((Ledger.ledger_description == "Expenses", Ledger.amount), else_=0)).label("total_expenses")
    roi = (total_revenue - total_expenses).label("roi")
    ratio = (total_revenue / func.nullif(total_expenses, 0)).label("ratio")  # Prevent division by zero

    query = db.query(
        Fund.fund_description,
        total_revenue,
        total_expenses,
        ratio,
        roi
    ).join(Fund, Ledger.fund_id == Fund.fund_id)

    if department:
        query = query.filter(Ledger.department_id == department)

    if start_date and end_date:
        query = query.filter(Ledger.general_ledger_date.between(start_date, end_date))

    # Sorting logic
    sort_column = {
        "revenue": total_revenue,
        "expenses": total_expenses,
        "ratio": ratio,
        "roi": roi
    }.get(sort_by, roi)

    order_by = desc(sort_column) if order == "desc" else asc(sort_column)

    query = query.group_by(Fund.fund_description).order_by(order_by)

    return query.all()


############ API 5 ############ 
def get_net_profit_by_time(db: Session, department=None, start_date=None, end_date=None, time_unit="year"):
    """ Get net profit (revenue - expenses) over time, filtered by department, with negative values for losses. """

    time_function = {
        "year": func.year(Ledger.general_ledger_date),
        "month": func.month(Ledger.general_ledger_date)
    }.get(time_unit, func.year(Ledger.general_ledger_date))  # Default to year

    query = db.query(
        time_function.label("time"),
        (func.sum(case((Ledger.ledger_description == "Revenues", Ledger.amount), else_=0)) -
         func.sum(case((Ledger.ledger_description == "Expenses", Ledger.amount), else_=0))).label("net_profit"),
    )

    if department:
        query = query.filter(Ledger.department_id == department)

    if start_date and end_date:
        query = query.filter(Ledger.general_ledger_date.between(start_date, end_date))

    query = query.group_by(time_function).order_by(time_function)

    return query.all()