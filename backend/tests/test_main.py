import os
import sys
from fastapi.testclient import TestClient

# Add the project root to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Now you can do the relative import
from app.main import app


"""
Execute this test by running on the terminal (from the app/) the command:
pytest --cov=app --cov-report=html tests/
 """

client = TestClient(app)

# Test for the main endpoint
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

# Test for the root endpoint
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200

# Test for the total waste for a specific comune and year
def test_total_waste():
    response = client.get("/total_waste/Comune1/2020")
    assert response.status_code == 200

# Test for total waste across all years for a specific comune
def test_total_waste_all_years():
    response = client.get("/total_waste_all_years/Comune1")
    assert response.status_code == 200

# Test for finding municipalities by waste for a specific year
def test_find_municipalities_by_waste():
    year = 2000  # Use an appropriate year value that exists in your 'filedati.csv'
    response = client.get(f"/find_municipalities_by_waste/{year}")
    assert response.status_code == 200

# Test for handling invalid input
def test_invalid_input():
    response = client.get("/total_waste/InvalidComune/2020")
    assert response.status_code == 200
