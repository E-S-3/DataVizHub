import csv
from app.core.database import SessionLocal
from app.core.models import Dataset


def clean_and_store_data():
    session = SessionLocal()
    session.query(Dataset).delete()
    session.commit()
    session.close()