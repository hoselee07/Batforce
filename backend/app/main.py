"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""

from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import pandas as pd


from .mymodules.birthdays import total_waste

app = FastAPI()

df = pd.read_csv('app/filedati.csv')

@app.get('/')
def read_root():
    """
    Root endpoint for the backend.

    Returns:
        dict: A simple greeting.
    """
    return {"Hello": "World"}

@app.get('/get-date')
def get_date():
    """
    Endpoint to get the current date.

    Returns:
        dict: Current date in ISO format.
    """
    current_date = datetime.now().isoformat()
    return JSONResponse(content={"date": current_date})

# Function1 - total_waste (comune, year)
@app.get('/total_waste/{comune}/{year}')
def get_total_waste(comune: str, year: int):
    """
    Endpoint to retrieve total waste for a given comune and year.

    This function receives the name of a Comune and a year, then returns the total
    waste generated in that Comune for the specified year. The data is retrieved
    from a CSV file.

    Args:
        comune (str): Name of the Comune.
        year (int): Year of interest.

    Returns:
        dict: Total waste in Kg or a message if not found.
    """

    # Path to the CSV file containing waste data
    csv_file_path = 'app/filedati.csv'
    
    # Retrieve waste data for the given comune and year
    waste = total_waste(comune, year, csv_file_path)
    
    # Return the waste data in a dictionary format
    return {"comune": comune, "year": year, "total_waste": waste}

# Function 2
@app.get('/total_waste_all_years/{comune}')
def get_total_waste_all_years(comune: str):
    """
    Endpoint to retrieve total waste for all years for a given comune.

    Args:
        comune (str): Name of the Comune

    Returns:
        dict: Total waste in Kg for all years or a message if not found
    """
    csv_file_path = 'app/filedati.csv'
    waste_data = total_waste_all_years(comune, csv_file_path)
    return {"comune": comune, "total_waste_data": waste_data}
