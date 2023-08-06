# plots a graph of the day's yield curve from the US treasury
# Future wants: 
  # posts the yield curve to instagram
  # Looks good
  # tells you how many days the 3mo to 30yrs has been inverted

import requests
from bs4 import BeautifulSoup
import datetime
import matplotlib.pyplot as plt

def data_grabber():
    # time in YYYYMM form for the url
    now = datetime.datetime.now()
    page = now.strftime("%Y%m")
  
    # Create a URL object
    url = f'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month={page}'

    response = requests.get(url)
    # convert to beautiful soup 
    soup = BeautifulSoup(response.content, 'html.parser') 
    # find table
    table_element = soup.find('table')

    # initialize lists to stoe the table headers and rows
    headers = []
    rows = []

    # Extract table headers (table column names)
    header_row = table_element.find('thead').find('tr')
    for header in header_row.find_all('th'):
        headers.append(header.text.strip())

    # Extract table rows (data rows)
    data_rows = table_element.find('tbody').find_all('tr')
    for row in data_rows:
        row_data = [cell.text.strip() for cell in row.find_all('td')]
        rows.append(row_data)

    # Data date
    data_date = rows[-1][0]

    # Create a new headers list without unused headers
    headers_list = headers[:0] + headers[10:]

    # Convert time periods to number values in years
    header_values_in_years = [get_period_value(header) for header in headers_list]

    # Filter out None values for unexpected formats, if any
    header_values_in_years = [value for value in header_values_in_years if value is not None]

    # Extracting the most recent data set
    most_recent_values = [value for value in rows[-1][1:] if value != 'N/A']

    # Convert the most revent data set to numbers
    most_recent_values = [float(element) for element in most_recent_values]

    return data_date, header_values_in_years, most_recent_values

# Mapping of time periods to their corresponding values in years
def get_period_value(period):
    # Check if the period contains 'Mo' for months or 'Yr' for years
    if 'Mo' in period:
        return float(period.split()[0]) / 12
    elif 'Yr' in period:
        return float(period.split()[0])
    else:
        return None  # Return None for unexpected formats

def plot_yield_curve(headers, date, data):
    with plt.style.context('/Users/collin/Documents/GitHub/yield_curve_poster/rose-pine.mplstyle'):
        plt.figure(figsize=(6, 3.5))
        plt.plot(headers, data, marker = '.')
        plt.xlabel("Maturity (Years)")
        plt.ylabel("Yield")
        plt.title(f"US Treasury Yield Curve Rates on {date}")
        plt.savefig('/Users/collin/Documents/GitHub/yield_curve_poster/yield_curve.png', dpi=300, bbox_inches='tight')  # Adjust the dpi as needed
        plt.grid(True)
        plt.show()

def main():
    date, headers, data = data_grabber()
    plot_yield_curve(headers, date, data)

if __name__ == "__main__":
    main()
