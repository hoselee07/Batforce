import pandas as pd


def total_waste(comune, year, data):
    """
    Function to retrieve the total waste for a given comune and year.

    :param comune: Name of the Comune
    :param year: Year of interest
    :param file_path: Path to the CSV file
    :return: Total waste in Kg or a message if not found
    """
    data = pd.read_csv('app/filedati.csv', delimiter=';')

    filtered_data = data[(data['Comune'] == comune) & (data['Anno'] == year)]

    if not filtered_data.empty:
        total_waste = filtered_data['Rifiuto totale (in Kg)'].iloc[0]
        return total_waste
    else:
        return "No data found for the specified Comune and Year."


def total_waste_all_years(comune, data):
    """
    Retrieve total waste for all years for a given comune.

    :param comune: Name of the Comune
    :param file_path: Path to the CSV file
    :return: Dictionary with years as keys and total waste in Kg as values
    """
    data = pd.read_csv('app/filedati.csv', delimiter=';')
    filtered_data = data[data['Comune'] == comune]

    if filtered_data.empty:
        return "No data found for the specified Comune."

    return filtered_data.set_index('Anno')['Rifiuto totale (in Kg)'].to_dict()


def find_municipalities_by_waste(data, year):
    """
    Finds the municipalities with the highest and lowest waste per capita for a given year.

    Parameters:
    - data: DataFrame containing the waste data.
    - year: The year for which to find the data.

    Returns:
    - A tuple containing the municipalities with the highest and lowest waste per capita.
    """
    data = pd.read_csv('app/filedati.csv', delimiter=';')
    year_data = data[data['Anno'] == year]

    year_data['Rifiuto totale pro capite (in Kg)'] = (
        year_data['Rifiuto totale pro capite (in Kg)']
        .str.replace('.', '')
        .str.replace(',', '.')
        .astype(float)
    )
    highest_waste = year_data[year_data['Rifiuto totale pro capite (in Kg)'] ==
                              year_data['Rifiuto totale pro capite (in Kg)'].max()]

    lowest_waste = year_data[year_data['Rifiuto totale pro capite (in Kg)'] ==
                             year_data['Rifiuto totale pro capite (in Kg)'].min()]

    return (
        highest_waste['Comune'].iloc[0], highest_waste['Rifiuto totale pro capite (in Kg)'].iloc[0],
        lowest_waste['Comune'].iloc[0], lowest_waste['Rifiuto totale pro capite (in Kg)'].iloc[0]
    )


def raccolta_differenziata_change(comune, file_path):
    """
    Function to calculate the change in 'raccolta differenziata' over the years for a given comune.
    
    :param comune: Name of the Comune
    :param file_path: Path to the CSV file
    :return: Dictionary containing year-wise data and percentage change
    """
    df = pd.read_csv(file_path, delimiter=";")
    df['Raccolta differenziata (in Kg)'] = pd.to_numeric(df['Raccolta differenziata (in Kg)'].str.replace('.', ''), errors='coerce')
    comune_data = df[df['Comune'].str.strip() == comune.strip()]
    raccolta_data = comune_data[['Anno', 'Raccolta differenziata (in Kg)']].dropna(subset=['Raccolta differenziata (in Kg)'])

    if raccolta_data.empty:
        return {'error': 'No data available for the specified comune'}
    
    if len(raccolta_data) < 2:
        return {'error': 'Insufficient data for percentage change calculation'}

    first_year_amount = raccolta_data.iloc[0]['Raccolta differenziata (in Kg)']
    last_year_amount = raccolta_data.iloc[-1]['Raccolta differenziata (in Kg)']
    percentage_change = ((last_year_amount - first_year_amount) / first_year_amount) * 100

    return {
        'data': raccolta_data.set_index('Anno')['Raccolta differenziata (in Kg)'].to_dict(),
        'percentage_change': percentage_change
    }
