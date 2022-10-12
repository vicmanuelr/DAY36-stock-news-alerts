import requests
import datetime as dt
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
API_KEY = os.environ.get("API_KEY")
PARAMETERS_ALPH = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": API_KEY
}


def get_stock_data():
    response = requests.get(STOCK_ENDPOINT, params=PARAMETERS_ALPH)
    response.raise_for_status()
    data = response.json()
    daily_dictionary = data["Time Series (Daily)"]
    return daily_dictionary


series_dict = get_stock_data()

# split data items in api data (e.g. 2020-10-01 to ["2020", "10", "01"])
days_to_strings = [key.split("-") for key, value in series_dict.items()]

# convert strings from previous steps into tuples and then to date objects
date_objects = [dt.date(int(i[0]), int(i[1]), int(i[2])) for i in days_to_strings]

# using the date objects get the last 2 closing prices from data of the API
today_price = float(series_dict[str(date_objects[0])]["4. close"])
last_closing_price = float(series_dict[str(date_objects[1])]["4. close"])

# calculate percentage difference from 2 last closing prices
difference = abs(today_price - last_closing_price)/(today_price/2 + last_closing_price/2) * 100

if difference > 5:
    print("Get News")
else:
    print("Difference less than 5")
## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file 
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file 
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
coronavirus market crash.
"""

