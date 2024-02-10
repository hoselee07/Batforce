"""
Frontend module for the Flask application.

This module defines a simple Flask application that serves as the frontend for the project.
"""
from flask import Flask, render_template
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField

# Flask application configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace 'your_secret_key' with a real secret key

# Backend service configuration
FASTAPI_BACKEND_HOST = 'http://backend'  # URL of the FastAPI backend
BACKEND_URL = f'{FASTAPI_BACKEND_HOST}/query/'


class WasteQueryForm(FlaskForm):
    """Form for querying total waste data by municipality and year."""
    comune = StringField('Comune:')
    year = IntegerField('Year:')
    submit = SubmitField('Get Total Waste')


class MunicipalitiesQueryForm(FlaskForm):
    """Form for finding municipalities based on waste data for a specified year."""
    year = IntegerField('Year:')
    submit = SubmitField('Find Municipalities')


class ComuneForm(FlaskForm):
    """Form for retrieving specific data for a given municipality."""
    comune = StringField('Municipality Name')
    submit = SubmitField('Get Data')


@app.route('/')
def index():
    """
    Serve the homepage of the application.

    Fetches the current date from the backend and renders the 'index.html' template
    with the fetched date.
    """
    date_from_backend = fetch_date_from_backend()
    return render_template('index.html', date_from_backend=date_from_backend)


def fetch_date_from_backend():
    """
    Fetch the current date from the backend service.

    Returns:
        str: The current date in ISO format if available, otherwise a default
        message indicating the date is not available.
    """
    backend_url = 'http://backend/get-date'
    try:
        response = requests.get(backend_url)
        response.raise_for_status()
        return response.json().get('date', 'Date not available')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching date from backend: {e}")
        return 'Date not available'


@app.route('/internal', methods=['GET', 'POST'])
def internal():
    """
    Handle requests to query total waste for a specific municipality and year.

    Renders a form for input and, on submission, queries the backend for total
    waste data, displaying the results on the same page.
    """
    form = WasteQueryForm()
    total_waste_result = None
    error_message = None

    if form.validate_on_submit():
        comune = form.comune.data
        year = form.year.data
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/total_waste/{comune}/{year}'
        response = requests.get(fastapi_url)

        if response.status_code == 200:
            data = response.json()
            total_waste_result = data.get('total_waste', 'No data available')
        else:
            error_message = f'Error: Unable to fetch total waste data for {comune} in {year}'

    return render_template('internal.html', form=form, total_waste_result=total_waste_result, error_message=error_message)


@app.route('/total_waste_all_years', methods=['GET', 'POST'])
def total_waste_all_years_query():
    """
    Query and display total waste data for a municipality across all years.

    Displays a form for municipality input and, upon submission, fetches and
    shows waste data for all years for the specified municipality.
    """
    form = WasteQueryForm()
    total_waste_data = None
    error_message = None

    if form.validate_on_submit():
        comune = form.comune.data
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/total_waste_all_years/{comune}'
        response = requests.get(fastapi_url)

        if response.status_code == 200:
            data = response.json()
            total_waste_data = data.get('total_waste_data', {})
        else:
            error_message = "Error fetching data from backend."

    return render_template('internal.html', form=form, total_waste_data=total_waste_data, error_message=error_message)


@app.route('/find_municipalities_by_waste', methods=['GET', 'POST'])
def find_municipalities_by_waste():
    """
    Find municipalities based on waste data for a given year.

    Handles form display and submission, querying the backend for municipalities
    with specific waste characteristics and displaying the results.
    """
    form = MunicipalitiesQueryForm()
    result = None
    error_message = None

    if form.validate_on_submit():
        year = form.year.data
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/find_municipalities_by_waste/{year}'
        response = requests.get(fastapi_url)

        if response.status_code == 200:
            data = response.json()
            result = {
                "Year": year,
                "Highest Waste Per Capita": data.get("Highest Waste Per Capita"),
                "Lowest Waste Per Capita": data.get("Lowest Waste Per Capita")
            }
        else:
            error_message = f"Error: Unable to fetch data for the year {year}"

    return render_template('find_municipalities.html', form=form, result=result, error_message=error_message)


@app.route('/raccolta_differenziata', methods=['GET', 'POST'])
def raccolta_differenziata():
    """
    Retrieve and display data related to differentiated waste collection for a given municipality.

    Renders a form for the municipality input and, upon submission, queries the backend
    for data related to differentiated waste collection for the specified municipality,
    displaying the data on the same page.
    """
    form = ComuneForm()
    data = None

    if form.validate_on_submit():
        comune = form.comune.data
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/raccolta_differenziata/{comune}'
        response = requests.get(fastapi_url)

        if response.status_code == 200:
            data = response.json()
        else:
            data = {'error': 'Failed to fetch data'}

    return render_template('raccolta_differenziata.html', form=form, data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)







