# plots a graph of the day's yield curve from the US treasury
# Future wants: 
  # posts the yield curve to instagram
  # Looks good
  # tells you how many days the 3mo to 30yrs has been inverted

import requests
from bs4 import BeautifulSoup
import datetime
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

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

    # Function for converting headers corresponding values in years
    def get_period_value(period):
        # Check if the period contains 'Mo' for months or 'Yr' for years
        if 'Mo' in period:
            return float(period.split()[0]) / 12
        elif 'Yr' in period:
            return float(period.split()[0])
        else:
            return None  # Return None for unexpected formats

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


def plot_yield_curve(headers, date, data):
    with plt.style.context('/Users/collin/Documents/GitHub/yield_curve_poster/rose-pine.mplstyle'):
        plt.figure(figsize=(6, 3.5))
        plt.plot(headers, data, marker = '.')
        plt.xlabel("Maturity (Years)")
        plt.ylabel("Yield")
        plt.title(f"US Treasury Yield Curve Rates on {date}")
        plt.savefig('yield_curve.png', dpi=1200, bbox_inches='tight')  # Adjust the dpi as needed

def post_to_insta():
    load_dotenv()
    # Initialize the login data
    access_token = os.getenv('ACCESS_TOKEN')
    business_account_id = os.getenv('BUSINESS_ACCOUNT_ID')
    yield_curve_file_path = 'yield_curve.png'

    def upload_media_to_instagram(access_token, business_account_id, media_file_path):
        url = f"https://graph.facebook.com/{business_account_id}/media"

        files = {
            'media_file': open(media_file_path, 'rb'),
        }

        params = {
            'access_token': access_token,
            'image_url': 'IMAGE_URL_PLACEHOLDER',  # You can also use 'video_url' for video files
        }

        response = requests.post(url, files=files, params=params)
        return response.json()
    
    def publish_media_to_instagram(access_token, business_account_id, media_id):
        url = f"https://graph.facebook.com/{business_account_id}/media_publish"

        params = {
            'access_token': access_token,
            'creation_id': media_id,
        }

        response = requests.post(url, params=params)
        return response.json()

    try:
        # Step 1: Upload the media file
        upload_response = upload_media_to_instagram(access_token, business_account_id, yield_curve_file_path)
        media_id = upload_response.get('id')

        if media_id:
            # Step 2: Publish the media to your business account
            publish_response = publish_media_to_instagram(access_token, business_account_id, media_id)
            print("Media posted successfully!")
        else:
            print("Media upload failed.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    date, headers, data = data_grabber()
    plot_yield_curve(headers, date, data)
    post_to_insta()

if __name__ == "__main__":
    main()
