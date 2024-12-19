import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re, sys

def parse_url_to_formatted_values(url):
    """
    Parses the URL to generate formatted select values based on the URL structure.

    Parameters:
        url (str): The URL to parse.

    Returns:
        list: A list of formatted select values.
    """
    # Extract the base identifier from the URL
    base_identifier_match = re.search(r'\/([^\/]+)\.htm', url)
    if not base_identifier_match:
        return []
    base_identifier = base_identifier_match.group(1).upper()

    formatted_values = [f"SELECT___{base_identifier}___"]

    # Extract query parameters for full formats
    query_params = re.findall(r'\?([^#]+)', url)
    if query_params:
        for param in query_params[0].split('&'):
            key, _ = param.split('=', 1)
            formatted_values.append(f"SELECT___{base_identifier}___{key}")

    return formatted_values

def get_flavors_in_json_with_formatted_class(url):
    """
    Gets all dropdown options from the source code of the URL for each formatted value.
    If there are multiple dropdown menus corresponding to the same formatted value, all are included.

    Parameters:
        url (str): The URL to get and parse.
        formatted_values (list): A list of formatted base identifiers (e.g., SELECT___RLX-PRO80___).

    Returns:
        dict: JSON-structured data mapping each formatted value to its dropdown options.
    """
    formatted_values = parse_url_to_formatted_values(url)
    # Get the page source
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    all_dropdowns = {}

    for formatted_value in formatted_values:
        base_identifier = formatted_value.split("___")[1]

        select_elements = soup.find_all('select', {'name': re.compile(base_identifier, re.IGNORECASE)})
        dropdown_options = []
        for select in select_elements:
            options = [option.text.strip() for option in select.find_all('option') if option.text.strip()]
            if options:
                dropdown_options.append(options)

        # Add to dictionary only if there are dropdown options
        formatted_value = formatted_value.replace("SELECT___", "").rstrip("_")
        if dropdown_options:
            all_dropdowns[formatted_value] = dropdown_options
        else:
            all_dropdowns[formatted_value] = None  # Indicate that no dropdown was found

    return json.dumps(all_dropdowns)

df = pd.read_csv("myvaporstore_scrape.csv")
df['New_Flavors'] = df['product_link'].apply(get_flavors_in_json_with_formatted_class)
df.to_csv('flavors_myvaporstore_scrape.csv', index=False)
