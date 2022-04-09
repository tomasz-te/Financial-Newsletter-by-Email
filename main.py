# Deploy on https://www.pythonanywhere.com/

import requests
import datetime as dt
import smtplib

STOCK = "TSLA" # Stock ticker
COMPANY_NAME = "Tesla Inc" # Stock name
CHANGE = # Daily percentage change triggering sending the newsletter.
EMAIL = "" # Your email
PASSWORD = "" # Your password
SMTP = "" # Your email smtp server
TO_EMAIL = "" # Where to send email
API_NEWSAPI = "", # Your API key for NewsAPI
API_ALPHA = "" # Your API key for Alphavantage

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_ALPHA
}
request = requests.get("https://www.alphavantage.co/query", params=parameters)
data = request.json()
yesterday = dt.datetime.now().date() - dt.timedelta(days=1)

if yesterday.weekday() == 0:
    day_before_yesterday = dt.datetime.now().date() - dt.timedelta(days=4)
else:
    day_before_yesterday = dt.datetime.now().date() - dt.timedelta(days=2)

yesterday = str(yesterday)
day_before_yesterday = str(day_before_yesterday)
stock_yesterday_price = float(data["Time Series (Daily)"][yesterday]["4. close"])
stock_day_before_yesterday_price = float(data["Time Series (Daily)"][day_before_yesterday]["4. close"])
price_change_percent = round(
    ((stock_yesterday_price - stock_day_before_yesterday_price) / stock_day_before_yesterday_price) * 100)

if price_change_percent >= 2 or price_change_percent <= -2:
    news_parameters = {
        "apiKey": API_NEWSAPI,
        "qInTitle": COMPANY_NAME,
        "pageSize": 3
    }
    request = requests.get(url="https://newsapi.org/v2/everything", params=news_parameters)
    data = request.json()

    if price_change_percent > 0:
        up_down_symbol = "🔺"
    else:
        up_down_symbol = "🔻"

    message_to_send = f"Subject:{COMPANY_NAME} alert!\n\n{STOCK} {up_down_symbol}{price_change_percent}%\n"

    for _ in range(3):
        message_to_send += f"Headline: {data['articles'][_]['title']}\n"
        message_to_send += f"Brief: {data['articles'][_]['description']}\n"

    print(message_to_send)

    with smtplib.SMTP(SMTP) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=TO_EMAIL,
            msg=message_to_send
        )
