import datetime as dt
import os
import requests
from twilio.rest import Client


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
NEWS_KEY = os.environ.get("NEWS_API")
NEWS_ENDPOINT = "https://newsapi.org/v2/top-headlines"
NEWS_PARAMETERS = {
    "apiKey": NEWS_KEY,
    "q": "Tesla",
}
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
API_KEY = os.environ.get("API_KEY")
PARAMETERS_ALPH = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": API_KEY
}
ACC_SID = os.environ.get("ACC_SID")
TWILIO_KEY = os.environ.get("TWILIO_KEY")


def get_stock_data() -> dict:
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
difference = round(abs(today_price - last_closing_price) / (today_price / 2 + last_closing_price / 2) * 100, 2)
if today_price > last_closing_price:
    symbol = "🔺"
else:
    symbol = "🔻"


def get_news() -> list:
    response = requests.get(NEWS_ENDPOINT, params=NEWS_PARAMETERS)
    response.raise_for_status()
    data = response.json()
    list_of_news = data["articles"][:3]
    return list_of_news


client = Client(username=ACC_SID, password=TWILIO_KEY)


def send_message(client_object: Client, msg_title: str, msg_description: str):
    message = client_object.messages.create(
        body=f"{STOCK}:{symbol}{difference}%\nHeadline:{msg_title}\nBrief:{msg_description}",
        from_='whatsapp:+14155238886',
        to='whatsapp:+50230324739'
    )
    print(message)


if difference > 5:
    for news in get_news():
        title = news["title"]
        description = news["description"]
        send_message(client, title, description)
else:
    for news in get_news():
        title = news["title"]
        description = news["description"]
        send_message(client, title, description)

# Optional: Format the SMS message like this:
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
