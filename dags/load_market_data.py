import os
import sqlite3
from datetime import date
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, 'data','database')
os.makedirs(DATABASE_DIR, exist_ok=True)

DATABASE_PATH = os.path.join(DATABASE_DIR, 'financial_data.db')
connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()
cursor.executescript('''

CREATE TABLE IF NOT EXISTS stock_prices (
    date TEXT NOT NULL,
    ticker TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    PRIMARY KEY (date, ticker)
)
''')
connection.commit()

SILVER_DIR = os.path.join(BASE_DIR, 'data', 'silver','market')
today = date.today().isoformat()

silver_filename = os.path.join(SILVER_DIR, f'TEST_{today}.csv')
df = pd.read_csv(silver_filename)
df['ticker'] = 'TEST'

for _,row in df.iterrows():
    cursor.execute('DELETE FROM stock_prices WHERE date=? AND ticker=?',
                   (str(row["date"]), row["ticker"]))
cursor.executemany("""
    INSERT INTO stock_prices (date, ticker, open, high, low, close, volume)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(date, ticker) DO UPDATE SET
        open = excluded.open,
        high = excluded.high,
        low = excluded.low,
        close = excluded.close,
        volume = excluded.volume
""", df[["date", "ticker", "open", "high", "low", "close", "volume"]].itertuples(index=False, name=None))

connection.commit()
print("Data loaded successfully")

cursor.execute('SELECT * FROM stock_prices')

rows = cursor.fetchall()
print('Database connects:')
for row in rows:
    print(row)

connection.close()

