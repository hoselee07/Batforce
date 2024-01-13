import pandas as pd

data = pd.read_csv('/app/app/filedati.csv', delimiter=';')

# Function1 - total_waste
# This function takes three parameters:
# the name of a "Comune", a year, and the path to the CSV file.
# It searches the CSV file for the given "Comune" and year and
# returns the corresponding “Rifiuto totale (in Kg)” value.

def total_waste(comune, year, data):
    """
    Function to retrieve the total waste for a given comune and year.

    :param comune: Name of the Comune
    :param year: Year of interest
    :param file_path: Path to the CSV file
    :return: Total waste in Kg or a message if not found
    """
    
    # Load the CSV file with the correct delimiter
    data = pd.read_csv('/app/app/filedati.csv', delimiter=';')

    # Filter data for the given comune and year
    filtered_data = data[(data['Comune'] == comune) & (data['Anno'] == year)]

    # Check if there is an entry for the given comune and year
    if not filtered_data.empty:
        # Extract the total waste value
        total_waste = filtered_data['Rifiuto totale (in Kg)'].iloc[0]
        return total_waste
    else:
        return "No data found for the specified Comune and Year."
