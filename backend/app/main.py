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

    Args:
        comune (str): Name of the Comune
        year (int): Year of interest

    Returns:
        dict: Total waste in Kg or a message if not found
    """
    # Assuming the CSV file path is fixed, you can hardcode or configure it here
    csv_file_path = 'app/filedati.csv'
    waste = total_waste(comune, year, csv_file_path)
    return {"comune": comune, "year": year, "total_waste": waste}
