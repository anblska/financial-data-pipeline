import os
import json
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BRONZE_DIR = os.path.join(BASE_DIR, "data", "bronze", "market")
print("Bronze folder:", os.path.abspath(BRONZE_DIR))
os.makedirs(BRONZE_DIR, exist_ok=True)

ticker = "TEST"
today = date.today().isoformat()

filename = os.path.join(BRONZE_DIR, f"{ticker}_{today}.json")

sample_data = {
    "Meta Data": {
        "2. Symbol": "TEST"
    },
    "Time Series (Daily)": {
        today: {
            "1. open": "100.00",
            "2. high": "105.00",
            "3. low": "98.00",
            "4. close": "103.00",
            "5. volume": "150000"
        }
    }
}

with open(filename, "w") as file:
    json.dump(sample_data, file, indent=4)

print("File successfully saved:", filename)