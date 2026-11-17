import json
import pandas as pd
import os
from datetime import date

from pandas.core.interchange import column

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BRONZE_DIR = os.path.join(BASE_DIR, "data", "bronze",'market')
SILVER_DIR = os.path.join(BASE_DIR, "data", "silver",'market')

os.makedirs(SILVER_DIR, exist_ok=True)

ticker = 'TEST'
today = date.today().isoformat()

filename = os.path.join(BRONZE_DIR, f'{ticker}_{today}.json')
with open(filename,'r') as file:
    data = json.load(file)

print(data)

daily_data = data["Time Series (Daily)"]

print(daily_data)

df = pd.DataFrame.from_dict(daily_data, orient="index")
df.columns = ["open", "high", "low", "close", "volume"]

df.index.name = "date"
df = df.reset_index()

numerical_columns = ["open", "high", "low", "close", "volume"]
for column  in numerical_columns:
    df[column] = df[column].apply(pd.to_numeric)

df['date'] = pd.to_datetime(df['date'])

print('Duplicate dates:', df['date'].duplicated().sum())

print('Missing values:',df['date'].isnull().sum())

price_columns = ['open', 'high', 'low', 'close', 'volume']
print('Negative prices:',(df[price_columns] <= 0).sum())

invalid_prices = df[
    (df['high'] < df[['close','open']].max(axis=1)) |
    (df['low'] > df[['close','open']].max(axis=1))
]
print('Invalid OHLC rows:', len(invalid_prices))

output_filename = os.path.join(SILVER_DIR, f'{ticker}_{today}.csv')
df.to_csv(output_filename, index=False)
print("File saved as:", output_filename)



