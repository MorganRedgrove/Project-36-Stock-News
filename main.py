import requests
import datetime
import html
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

today = datetime.date.today()
yesterday = str(today - datetime.timedelta(days=1))
dbf_yesterday = str(today - datetime.timedelta(days=2))

parameters= {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK ,
    "apikey": "",
}
response = requests.get(url="https://www.alphavantage.co/query?", params=parameters)
data = response.json()
daily = data["Time Series (Daily)"]
stock_y = float(daily[yesterday]["4. close"])
print(f"{yesterday} {stock_y}")
stock_dbfy = float(daily[dbf_yesterday]["4. close"])
print(f"{dbf_yesterday} {stock_dbfy}")
# percentage_change = round(1-(stock_y/stock_dbfy),2)
percentage_change = -0.10
print(percentage_change)
if percentage_change >=0:
    symbol = "🔺"
else:
    symbol = "🔻"

if abs(percentage_change) >= 0.05:
    parameters = {
        "q": COMPANY_NAME,
        "apiKey": "",
    }
    response = requests.get(url="https://newsapi.org/v2/everything?", params=parameters)
    data = response.json()

    article1_title = data["articles"][5]["title"]
    article1_description = html.unescape(data["articles"][0]["description"])
    article1 = f"Headline: {article1_title}\nBrief: {article1_description}\n"
    # print(article1)

    article2_title = data["articles"][6]["title"]
    article2_description = html.unescape(data["articles"][1]["description"])
    article2 = f"Headline: {article2_title}\nBrief: {article2_description}\n"
    # print(article2)

    article3_title = data["articles"][12]["title"]
    article3_description = html.unescape(data["articles"][2]["description"])
    article3 = f"Headline: {article3_title}\nBrief: {article3_description}\n"
    # print(article3)

    account_sid = ""
    auth_token = ""
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=f"{COMPANY_NAME}:  {symbol}{percentage_change}%\n"
             f"{article1}\n"
             f"{article2}\n"
             f"{article3}\n",
        from_='',
        to=''
    )

    print(message.status)