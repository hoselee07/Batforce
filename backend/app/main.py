"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import pandas as pd

from .mymodules.birthdays import total_waste
from .mymodules.birthdays import total_waste_all_years
from .mymodules.birthdays import find_municipalities_by_waste
from .mymodules.birthdays import raccolta_differenziata_change

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


# function 1 - total_waste (comune, year)
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
    csv_file_path = 'app/filedati.csv'
    waste = total_waste(comune, year, csv_file_path)
    return {"comune": comune, "year": year, "total_waste": waste}


# function 2
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


# function 3
@app.get('/find_municipalities_by_waste/{year}')
def get_find_municipalities_by_waste(year: int):
    """
    Endpoint to retrieve the municipalities with the highest and lowest waste per capita for a given year.

    Args:
        year (int): Year of interest

    Returns:
        JSONResponse: Contains the municipalities with the highest and lowest waste per capita.
    """
    csv_file_path = 'app/filedati.csv'
    highest_municipality, highest_waste, lowest_municipality, lowest_waste = find_municipalities_by_waste(
        csv_file_path, year)
    return JSONResponse(content={
        "Year": year,
        "Highest Waste Per Capita": {"Municipality": highest_municipality, "Waste (in kg)": highest_waste},
        "Lowest Waste Per Capita": {"Municipality": lowest_municipality, "Waste (in kg)": lowest_waste}
    })


# function 4
@app.get('/raccolta_differenziata/{comune}')
def get_raccolta_differenziata_change(comune: str):
    """
    Endpoint to get the change in 'raccolta differenziata' over the years for a given comune.

    Args:
        comune (str): Name of the Comune

    Returns:
        JSONResponse: The % change in 'raccolta differenziata' over the years for a given comune.
    """
    file_path = 'app/filedati.csv'
    data = raccolta_differenziata_change(comune, file_path)
    return JSONResponse(content=data)


@app.get('/get-date')
def get_date():
    """
    Endpoint to get the current date.

    Returns:
        dict: Current date in ISO format.
    """
    current_date = datetime.now().isoformat()
    return JSONResponse(content={"date": current_date})

