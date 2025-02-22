from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Dataset(Base):
    __tablename__ = "dataset_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # add here