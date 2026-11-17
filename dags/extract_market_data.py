
import os
import json
import time
import requests
from pprint import pprint
from datetime import date

TICKERS = ["AAPL", "JPM", "XOM", "WMT", "JNJ"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BRONZE_DIR = os.path.join(BASE_DIR, "data", "bronze", "market")
print("Bronze folder:", os.path.abspath(BRONZE_DIR))
os.makedirs(BRONZE_DIR, exist_ok=True)


def extract_stock_data(ticker, api_key):
    url = "https://www.alphavantage.co/query"

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "apikey": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

    except requests.RequestException as error:
        print(f"Request failed: {error}")
        raise

    data = response.json()

    if "Time Series (Daily)" not in data:
        raise ValueError(f"Unexpected API response: {data}")

    today = date.today().isoformat()
    filename = os.path.join(BRONZE_DIR, f"{ticker}_{today}.json")

    with open(filename, "x") as file:
        json.dump(data, file, indent=4)

    daily_data = data["Time Series (Daily)"]

    observations = []

    for observation_date, values in daily_data.items():
        observations.append({
            "date": observation_date,
            "open": values["1. open"],
            "high": values["2. high"],
            "low": values["3. low"],
            "close": values["4. close"],
            "volume": values["5. volume"]
        })

    return observations


api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

if not api_key:
    raise ValueError("Alpha Vantage API key not found!")

print("API key loaded:", api_key is not None)

for ticker in TICKERS:
    result = extract_stock_data(ticker, api_key)
    pprint(result)
    time.sleep(1)
