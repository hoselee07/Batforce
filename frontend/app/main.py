"""
Frontend module for the Flask application.

This module defines a simple Flask application that serves as the frontend for the project.
"""

from flask import Flask, render_template
import requests  # Import the requests library to make HTTP requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key

# Configuration for the FastAPI backend URL
FASTAPI_BACKEND_HOST = 'http://backend'  # Replace with the actual URL of your FastAPI backend
BACKEND_URL = f'{FASTAPI_BACKEND_HOST}/query/'


class QueryForm(FlaskForm):
    person_name = StringField('Person Name:')
    submit = SubmitField('Get Birthday from FastAPI Backend')


@app.route('/')
def index():
    """
    Render the index page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    # Fetch the date from the backend
    date_from_backend = fetch_date_from_backend()
    return render_template('index.html', date_from_backend=date_from_backend)

def fetch_date_from_backend():
    """
    Function to fetch the current date from the backend.

    Returns:
        str: Current date in ISO format.
    """
    backend_url = 'http://backend/get-date'  # Adjust the URL based on your backend configuration
    try:
        response = requests.get(backend_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json().get('date', 'Date not available')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching date from backend: {e}")
        return 'Date not available'


# Function1
@app.route('/internal', methods=['GET', 'POST'])
def internal():
    """
    Handle GET and POST requests to render the internal page. 
    This function processes a form for querying total waste for a given comune and year, 
    makes a request to a FastAPI backend, and displays the result.
    """
    
    form = WasteQueryForm()
    total_waste_result = None
    error_message = None

    if form.validate_on_submit():
        comune = form.comune.data
        year = form.year.data

        # Make a GET request to the FastAPI backend
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/total_waste/{comune}/{year}'
        response = requests.get(fastapi_url)
            
        if response.status_code == 200:
            data = response.json()
            total_waste_result = data.get('total_waste', 'No data available')
        else:
            error_message = f'Error: Unable to fetch total waste data for
            {comune} in {year}'

    # This will render the same internal.html page with the form and result
    return render_template('internal.html', form=form,
    total_waste_result=total_waste_result, error_message=error_message)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)


# Function 2
@app.route('/total_waste_all_years', methods=['GET', 'POST'])
def total_waste_all_years_query():
    form = WasteQueryForm()  
    total_waste_data = None
    error_message = None

    if form.validate_on_submit():
        comune = form.comune.data

        # Construct the URL for the FastAPI backend
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/total_waste_all_years/{comune}'
        response = requests.get(fastapi_url)

        if response.status_code == 200:
            data = response.json()
            total_waste_data = data.get('total_waste_data', {})
        else:
            error_message = "Error fetching data from backend."

    return render_template('internal.html', form=form, total_waste_data=total_waste_data, error_message=error_message)
