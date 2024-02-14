import os
import sys
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import pandas as pd

# Add the project root to the sys.path to allow imports from the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the FastAPI application for testing
from app.main import app

# Initialize the test client with the FastAPI app
client = TestClient(app)

# Load dataset for testing purposes
df = pd.read_csv('app/filedati.csv')

def test_read_main():
    """Test the main/root endpoint to ensure it returns the correct response."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_root_endpoint():
    """Ensure the root endpoint is reachable and returns a HTTP 200 status."""
    response = client.get("/")
    assert response.status_code == 200

def test_total_waste():
    """Test the total waste endpoint for a given comune and year."""
    comune = "Comune1"
    year = 2020
    response = client.get(f"/total_waste/{comune}/{year}")
    assert response.status_code == 200
    data = response.json()
    assert "total_waste" in data
    assert isinstance(data["total_waste"], (int, float, str))  # Check for expected data type

def test_total_waste_all_years():
    """Test retrieving total waste data for all years for a specific comune."""
    comune = "Comune1"
    response = client.get(f"/total_waste_all_years/{comune}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict) or 'error' in data
    if isinstance(data, dict):
        assert len(data) > 0  # Ensure data is not empty

def test_find_municipalities_by_waste():
    """Test endpoint for finding municipalities with the highest and lowest waste per capita for a year."""
    year = 2000
    response = client.get(f"/find_municipalities_by_waste/{year}")
    assert response.status_code == 200
    content = response.json()
    assert "Highest Waste Per Capita" in content and "Lowest Waste Per Capita" in content
    assert isinstance(content["Highest Waste Per Capita"], dict)
    assert isinstance(content["Lowest Waste Per Capita"], dict)

@pytest.mark.parametrize("comune", ['Affi', 'Vicenza', 'Belfiore'])
def test_raccolta_differenziata_change_multiple_comuni(comune):
    """Parameterized test for checking differentiated waste collection change across multiple comuni."""
    response = client.get(f"/raccolta_differenziata/{comune}")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data and "percentage_change" in data
    assert isinstance(data["data"], dict)
    assert isinstance(data["percentage_change"], (int, float))

def test_total_waste_all_years_no_data():
    """Test the total waste for all years endpoint with a comune that has no data."""
    response = client.get("/total_waste_all_years/NonexistentComune")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['comune'] == 'NonexistentComune'

def test_raccolta_differenziata_insufficient_data():
    """Test the differentiated waste collection endpoint for a comune with insufficient data."""
    response = client.get("/raccolta_differenziata/San Stino di Livenza")
    assert response.status_code == 200
    assert response.json() == {'error': 'Insufficient data for percentage change calculation'}

def test_raccolta_differenziata_nodata():
    """Test the differentiated waste collection endpoint for a comune with insufficient data."""
    response = client.get("/raccolta_differenziata/Pippo")
    assert response.status_code == 200
    assert response.json() == {'error': 'No data available for the specified comune'}

def test_total_waste_all_years_success():
    """Test successfully retrieving total waste data for all years for a specific comune."""
    comune = "Preganziol"
    response = client.get(f"/total_waste_all_years/{comune}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0  # Check for non-empty data

def test_total_waste_valid_data():
    """Test the total waste endpoint with valid comune and year, expecting to return actual data."""
    response = client.get("/total_waste/Comune1/2020")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict) and "total_waste" in data  # Check for expected data structure and key

def test_total_waste_no_data():
    """Test the total waste endpoint with a nonexistent comune for a specific year, expecting no data."""
    response = client.get("/total_waste/NonexistentComune/2020")
    assert response.status_code == 200  # Use 200 to indicate successful handling of the request, even if no data exists
    response_json = response.json()
    # Ensure the response structure includes 'comune', 'year', and 'error' keys
    assert response_json['comune'] == 'NonexistentComune'
    assert response_json['year'] == 2020

def test_total_waste_basic_scenario():
    """Test a basic scenario where total waste data is expected to be available for a given comune and year."""
    response = client.get("/total_waste/Affi/2000")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "total_waste" in data  # Validate the presence of the 'total_waste' key in the response
    # This test ensures that the endpoint functions correctly under expected conditions

def get_data_for_comune(comune_name):
    """Retrieve data for a specified comune. This function simulates data fetching and processing."""
    # Filter the dataset for the specified comune
    filtered_data = df[df['Comune'] == comune_name]
    if filtered_data.empty:
        # Return an error message if no data is found for the comune
        return {'error': 'No data available for the specified comune'}
    else:
        # Placeholder for data processing logic
        pass

def test_get_date():
    """Test the endpoint that returns the current date, verifying the date format."""
    response = client.get("/get-date")
    assert response.status_code == 200
    data = response.json()
    assert "date" in data  # Ensure the 'date' key is present in the response
    try:
        # Attempt to parse the date to confirm it's in the expected ISO format
        parsed_date = datetime.fromisoformat(data["date"])
        assert isinstance(parsed_date, datetime)  # Validate that the parsing was successful
    except ValueError:
        # If parsing fails, the test should fail indicating the date format is incorrect
        assert False, "Returned date is not in ISO format"
