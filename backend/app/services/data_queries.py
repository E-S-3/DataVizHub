from sqlalchemy.orm import Session
from sqlalchemy import func, case, desc, and_
from app.core.models import Ledger, Department, CostCenter, Fund
from datetime import datetime, timedelta
from fastapi import HTTPException

########################  Helper Functions ########################  

# Function to check if department exists
def check_department_exists(db: Session, department_id: int):
    department = db.query(Department).filter(Department.department_id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

# Function to validate date range
def validate_date_range(start_date: str, end_date: str):
    if start_date and end_date:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d") if isinstance(start_date, str) else start_date
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") if isinstance(end_date, str) else end_date
        if start_dt > end_dt:
            raise HTTPException(status_code=400, detail="Start date must be before or equal to end date")

########################  API 0 ########################  
def get_departments_and_ledger_dates(db: Session):
    departments = db.query(Department.department_id, Department.department_name).all()
    earliest_date = db.query(func.min(Ledger.general_ledger_date)).scalar()
    latest_date = db.query(func.max(Ledger.general_ledger_date)).scalar()

    return {
        "departments": [{"id": dept.department_id, "name": dept.department_name} for dept in departments],
        "earliest_date": earliest_date,
        "latest_date": latest_date
    }


########################  API 1 ########################  
def get_top_roi_departments(db: Session, start_date=None, end_date=None):
    # Validate date range
    validate_date_range(start_date, end_date)

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
    # Check if department exists
    check_department_exists(db, department_id)
    
    # Validate date range
    validate_date_range(start_date, end_date)

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


########################  API 2 ########################  
def get_top_budget_departments(db: Session, department_id=None, start_date=None, end_date=None):
    # Check if department exists if provided
    if department_id:
        check_department_exists(db, department_id)

    # Validate date range
    validate_date_range(start_date, end_date)

    expense_case = case(
        (and_(Ledger.ledger_description == "Expenses", Ledger.amount > 0), Ledger.amount),
        else_=0
    )

    revenue_case = case(
        (and_(Ledger.ledger_description == "Revenues", Ledger.amount < 0), -Ledger.amount),
        else_=0
    )

    if department_id:
        # Get top 10 CCD for a specific department
        query = db.query(
            CostCenter.cost_center_description,
            func.sum(expense_case + revenue_case).label("total_expenditure")
        ).join(CostCenter, Ledger.cost_center_id == CostCenter.cost_center_id
        ).filter(Ledger.department_id == department_id)

    else:
        # Get top 10 departments by total expenditure
        query = db.query(
            Department.department_name,
            func.sum(expense_case + revenue_case).label("total_expenditure")
        ).join(Department, Ledger.department_id == Department.department_id)

    # Apply date filtering flexibly
    if start_date and end_date:
        query = query.filter(Ledger.general_ledger_date.between(start_date, end_date))
    elif start_date:
        query = query.filter(Ledger.general_ledger_date >= start_date)
    elif end_date:
        query = query.filter(Ledger.general_ledger_date <= end_date)

    # Grouping and ordering logic
    if department_id:
        query = query.group_by(CostCenter.cost_center_description
        ).order_by(func.sum(expense_case + revenue_case).desc()).limit(10)
    else:
        query = query.group_by(Department.department_name
        ).order_by(func.sum(expense_case + revenue_case).desc()).limit(10)

    return query.all()


########################  API 3 ########################  
def get_revenue_expenses_by_year(db: Session, department_id=None, start_date=None, end_date=None):
    # Check if department exists if provided
    if department_id:
        check_department_exists(db, department_id)

    # Validate date range
    validate_date_range(start_date, end_date)
    
    """ Get revenue and expenses over time, filtered by department, 
    with automatic time granularity selection:
      - < 1 month → group by day
      - < 1 year → group by month
      - ≥ 1 year → group by year
    """
    # Determine the appropriate time grouping
    if start_date and end_date:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d") if isinstance(start_date, str) else start_date
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") if isinstance(end_date, str) else end_date
        date_diff = (end_dt - start_dt).days

        if date_diff < 30:
            time_function = func.day(Ledger.general_ledger_date)  # Group by day
        elif date_diff < 365:
            time_function = func.month(Ledger.general_ledger_date)  # Group by month
        else:
            time_function = func.year(Ledger.general_ledger_date)  # Group by year
    else:
        time_function = func.year(Ledger.general_ledger_date)  # Default to year

    # Define revenue and expense calculations
    revenue_case = case(
        (and_(Ledger.ledger_description == "Revenues", Ledger.amount > 0), Ledger.amount),
        (and_(Ledger.ledger_description == "Expenses", Ledger.amount < 0), -Ledger.amount),
        else_=0
    )

    expense_case = case(
        (and_(Ledger.ledger_description == "Expenses", Ledger.amount > 0), Ledger.amount),
        (and_(Ledger.ledger_description == "Revenues", Ledger.amount < 0), -Ledger.amount),
        else_=0
    )

    query = db.query(
        time_function.label("time"),
        func.sum(revenue_case).label("total_revenue"),
        func.sum(expense_case).label("total_expenses")
    )

    if department_id:
        query = query.filter(Ledger.department_id == department_id)

    if start_date and end_date:
        query = query.filter(Ledger.general_ledger_date.between(start_date, end_date))
    elif start_date:
        query = query.filter(Ledger.general_ledger_date >= start_date)
    elif end_date:
        query = query.filter(Ledger.general_ledger_date <= end_date)

    query = query.group_by(time_function).order_by(time_function)

    return query.all()


########################  API 4 ########################  
def get_fund_table(db: Session, department_id=None, start_date=None, end_date=None):
    # Check if department exists if provided
    if department_id:
        check_department_exists(db, department_id)

    # Validate date range
    validate_date_range(start_date, end_date)
    
    """ Get fund description, expenses, revenues, ratio, and ROI filtered by department. """
    revenue_case = case(
        (and_(Ledger.ledger_description == "Revenues", Ledger.amount > 0), Ledger.amount),
        (and_(Ledger.ledger_description == "Expenses", Ledger.amount < 0), -Ledger.amount),
        else_=0
    )

    expense_case = case(
        (and_(Ledger.ledger_description == "Expenses", Ledger.amount > 0), Ledger.amount),
        (and_(Ledger.ledger_description == "Revenues", Ledger.amount < 0), -Ledger.amount),
        else_=0
    )

    total_revenue = func.sum(revenue_case).label("total_revenue")
    total_expenses = func.sum(expense_case).label("total_expenses")
    roi = (total_revenue - total_expenses).label("roi")
    ratio = (total_revenue / func.nullif(total_expenses, 0)).label("ratio")  # Prevent division by zero

    query = db.query(
        Fund.fund_description,
        total_revenue,
        total_expenses,
        ratio,
        roi
    ).join(Fund, Ledger.fund_id == Fund.fund_id)

    if department_id:
        query = query.filter(Ledger.department_id == department_id)

    if start_date and end_date:
        query = query.filter(Ledger.general_ledger_date.between(start_date, end_date))
    elif start_date:
        query = query.filter(Ledger.general_ledger_date >= start_date)
    elif end_date:
        query = query.filter(Ledger.general_ledger_date <= end_date)

    query = query.group_by(Fund.fund_description).order_by(desc(roi))  # Default sorting by ROI (descending)

    return query.all()


########################  API 5 ########################  
def get_net_profit_by_time(db: Session, department_id=None, start_date=None, end_date=None):
    # Check if department exists if provided
    if department_id:
        check_department_exists(db, department_id)

    # Validate date range
    validate_date_range(start_date, end_date)
    
    """ 
    automatic time series selection:
      - < 1 month → group by day
      - < 1 year → group by month
      - >= 1 year → group by year
    """
    # Determine the appropriate time grouping
    if start_date and end_date:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d") if isinstance(start_date, str) else start_date
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") if isinstance(end_date, str) else end_date
        date_diff = (end_dt - start_dt).days

        if date_diff < 30:
            time_function = func.day(Ledger.general_ledger_date)  # Group by day
        elif date_diff < 365:
            time_function = func.month(Ledger.general_ledger_date)  # Group by month
        else:
            time_function = func.year(Ledger.general_ledger_date)  # Group by year
    else:
        time_function = func.year(Ledger.general_ledger_date)  # Default to year

    # Define revenue and expense calculations
    revenue_case = case(
        (and_(Ledger.ledger_description == "Revenues", Ledger.amount > 0), Ledger.amount),
        (and_(Ledger.ledger_description == "Expenses", Ledger.amount < 0), -Ledger.amount),
        else_=0
    )

    expense_case = case(
        (and_(Ledger.ledger_description == "Expenses", Ledger.amount > 0), Ledger.amount),
        (and_(Ledger.ledger_description == "Revenues", Ledger.amount < 0), -Ledger.amount),
        else_=0
    )

    query = db.query(
        time_function.label("time"),
        (func.sum(revenue_case) - func.sum(expense_case)).label("net_profit")
    )

    if department_id:
        query = query.filter(Ledger.department_id == department_id)

    if start_date and end_date:
        query = query.filter(Ledger.general_ledger_date.between(start_date, end_date))
    elif start_date:
        query = query.filter(Ledger.general_ledger_date >= start_date)
    elif end_date:
        query = query.filter(Ledger.general_ledger_date <= end_date)

    query = query.group_by(time_function).order_by(time_function)

    return query.all()
