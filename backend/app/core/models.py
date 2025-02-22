from app.core.database import Base
from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

# Define Department Model
class Department(Base):
    __tablename__ = "department"
    department_id = Column(Integer, primary_key=True)
    department_name = Column(String(255))
    department_name_key = Column(String(255))

# Define Fund Model
class Fund(Base):
    __tablename__ = "fund"
    fund_id = Column(Integer, primary_key=True)
    fund_description = Column(String(255))
    fund_description_key = Column(String(255))

# Define Cost Center Model
class CostCenter(Base):
    __tablename__ = "cost_center"
    cost_center_id = Column(Integer, primary_key=True)
    cost_center_description = Column(String(255))
    cost_center_description_key = Column(String(255))

# Define Ledger Model
class Ledger(Base):
    __tablename__ = "ledger"
    id = Column(Integer, primary_key=True)
    general_ledger_date = Column(Date)
    amount = Column(DECIMAL(15, 2))
    ledger_description = Column(String(255))
    
    fund_id = Column(Integer, ForeignKey("fund.fund_id"))
    department_id = Column(Integer, ForeignKey("department.department_id"))
    cost_center_id = Column(Integer, ForeignKey("cost_center.cost_center_id"))

    # Relationships
    fund = relationship("Fund")
    department = relationship("Department")
    cost_center = relationship("CostCenter")
