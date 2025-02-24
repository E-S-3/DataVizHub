import pytest
from unittest.mock import MagicMock
from app.services.data_queries import (
    get_top_roi_departments,
    get_revenue_expenses_by_year,
    get_net_profit_by_time
)
from datetime import datetime


# Mocking Database Session Fixture for Top ROI
@pytest.fixture
def mock_top_roi_db():
    mock_db = MagicMock()
    
    # Mocking the result for get_top_roi_departments
    mock_db.query().join().filter().group_by().order_by().limit().all.return_value = [
        ("HR", 5000),
        ("Finance", 4500)
    ]
    
    return mock_db


# Test for get_top_roi_departments
def test_get_top_roi_departments(mock_top_roi_db):
    start_date = "2019-01-01"
    end_date = "2019-12-31"
    
    result = get_top_roi_departments(mock_top_roi_db, start_date=start_date, end_date=end_date)
    
    assert len(result) == 2  # Two departments mocked
    assert result[0] == ("HR", 5000)
    assert result[1] == ("Finance", 4500)


# Mocking Database Session Fixture for Revenue/Expenses by Year
@pytest.fixture
def mock_revenue_expenses_db():
    mock_db = MagicMock()

    # Mocking the result for get_revenue_expenses_by_year
    mock_db.query().filter().group_by().order_by().all.return_value = [
        (2020, 150000, 120000),
        (2021, 160000, 130000)
    ]
    
    return mock_db


# Test for get_revenue_expenses_by_year
def test_get_revenue_expenses_by_year(mock_revenue_expenses_db):
    start_date = "2020-01-01"
    end_date = "2021-12-31"
    
    result = get_revenue_expenses_by_year(mock_revenue_expenses_db, start_date=start_date, end_date=end_date)
    
    assert len(result) == 2  # Two years mocked
    assert result[0] == (2020, 150000, 120000)
    assert result[1] == (2021, 160000, 130000)


# Mocking Database Session Fixture for Net Profit by Time
@pytest.fixture
def mock_net_profit_db():
    mock_db = MagicMock()

    # Mocking the result for get_net_profit_by_time
    mock_db.query().filter().group_by().order_by().all.return_value = [
        (2020, 20000),
        (2021, 30000)
    ]
    
    return mock_db


# Test for get_net_profit_by_time
def test_get_net_profit_by_time(mock_net_profit_db):
    start_date = "2020-01-01"
    end_date = "2021-12-31"
    
    result = get_net_profit_by_time(mock_net_profit_db, start_date=start_date, end_date=end_date)
    
    assert len(result) == 2  # Two years mocked
    assert result[0] == (2020, 20000)
    assert result[1] == (2021, 30000)
