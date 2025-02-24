import pytest
from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI app from your main.py

@pytest.fixture
def client():
    # Create a TestClient instance to test the FastAPI app
    with TestClient(app) as client:
        yield client


# Test for /top-roi/
def test_get_top_roi(client):
    department_ids = [101, 102, 103, 105, 106, 107]
    for department in department_ids:
        # Update URL to include the /api prefix
        response = client.get(f"/api/top-roi/?department={department}&start_date=2017-01-01&end_date=2019-12-31")
        assert response.status_code == 200
        data = response.json()
        assert "labels" in data
        assert "values" in data
        assert isinstance(data["labels"], list)
        assert isinstance(data["values"], list)

# Test for /top-budget/
def test_get_top_budget(client):
    department_ids = [101, 102, 103, 105, 106, 107]
    for department in department_ids:
        # Update URL to include the /api prefix
        response = client.get(f"/api/top-budget/?department={department}&start_date=2017-01-01&end_date=2019-12-31")
        assert response.status_code == 200
        data = response.json()
        assert "labels" in data
        assert "values" in data
        assert isinstance(data["labels"], list)
        assert isinstance(data["values"], list)

# Test for /revenue-expenses/
def test_get_revenue_expenses(client):
    department_ids = [101, 102, 103, 105, 106, 107]
    for department in department_ids:
        # Update URL to include the /api prefix
        response = client.get(f"/api/revenue-expenses/?department={department}&start_date=2015-02-11&end_date=2018-12-31")
        assert response.status_code == 200
        data = response.json()
        assert "years" in data
        assert "revenues" in data
        assert "expenses" in data
        assert isinstance(data["years"], list)
        assert isinstance(data["revenues"], list)
        assert isinstance(data["expenses"], list)

# Test for /fund-table/
def test_get_fund_table(client):
    department_ids = [101, 102, 103, 105, 106, 107]
    for department in department_ids:
        # Update URL to include the /api prefix
        response = client.get(f"/api/fund-table/?department={department}&start_date=2017-10-01&end_date=2019-12-31")
        assert response.status_code == 200
        data = response.json()
        assert "funds" in data
        assert isinstance(data["funds"], list)

# Test for /net-profit/
def test_get_net_profit(client):
    department_ids = [101, 102, 103, 105, 106, 107]
    for department in department_ids:
        # Update URL to include the /api prefix
        response = client.get(f"/api/net-profit/?department={department}&start_date=2016-01-01&end_date=2017-12-31")
        assert response.status_code == 200
        data = response.json()
        assert "times" in data
        assert "net_profits" in data
        assert isinstance(data["times"], list)
        assert isinstance(data["net_profits"], list)

def test_get_top_roi_invalid_department(client):
    department_ids = [999]  # 999 doesn't exist
    for department in department_ids:
        response = client.get(f"/api/top-roi/?department={department}&start_date=2017-01-01&end_date=2019-12-31")
        assert response.status_code == 404 
        data = response.json()
        assert "detail" in data  

def test_get_top_budget_invalid_date_range(client):
    department_ids = [101]
    response = client.get(f"/api/top-budget/?department={department_ids[0]}&start_date=2020-01-01&end_date=2019-12-31")
    assert response.status_code == 400  # Assuming the API returns 400 for invalid date range
    data = response.json()
    assert "detail" in data


