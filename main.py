# plots a graph of the day's yield curve from the US treasury
# Future wants: 
  # posts the yield curve to instagram
  # Looks good
  # tells you how many days the 3mo to 30yrs has been inverted
# ! is totally broken, I don't think it's web scraping right

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

    # grab table from the website
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html5lib')
        table = soup.find("table", class_="t-chart")
        rows = table.find_all("tr")
        headers = [cell.get_text() for cell in rows[0].find_all("th")]
        data = {}
        for row in rows[1:]:
            cells = row.find_all("td")
            date = cells[0].get_text()
            values = [float(cell.get_text()) for cell in cells[1:]]
            data[date] = values
        return headers, data
    else:
        raise ValueError("Failed to fetch data from the website.")

def extract_most_recent_day(data):
  most_recent_day = max(data.keys())
  return most_recent_day, data[most_recent_day]

def plot_yield_curve(headers, date, values):
    plt.figure(figsize=(10, 6))
    plt.plot(headers[1:], values, marker='o')
    plt.xlabel("Maturity (Years)")
    plt.ylabel("Yield")
    plt.title(f"US Treasury Yield Curve Rates on {date}")
    plt.grid(True)
    plt.show()

def main():
    headers, data = data_grabber()
    date, values = extract_most_recent_day(data)
    plot_yield_curve(headers, date, values)

if __name__ == "__main__":
    main()
