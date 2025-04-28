import requests
import time
import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["crypto"]  # Replace with your database name
collection = db["cryptoHistorical"]
# CryptoCompare API Key
API_KEY = "a2ea63a50f47d88207df27081157aa9b9e87c46888050bfbbfce883070f14dbd"
# Function to fetch only the latest hour of historical data
def get_latest_hour_data(crypto_symbol, i,currency="USD"):
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={crypto_symbol}&tsym={currency}&limit={i}"
    headers = {"Authorization": f"Apikey {API_KEY}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["Data"]["Data"][-1]  # Only the latest hour
    else:
        print(f"Error fetching data for {crypto_symbol}: {response.status_code}")
        return None

# Function to insert historical data into the database
def insert_data(df):
    records = df.to_dict(orient="records")  # Convert DataFrame to list of dictionaries
    collection.insert_many(records)

# Function to transform data
def transformation_data(message):
    df = pd.DataFrame([message])  # Wrap message in a list
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].fillna(0)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    return df

# Cryptos to track
cryptos = ["BTC", "ETH", "XRP", "ADA", "SOL"]
while True:
    for i in range(1,60):
        for crypto in cryptos:
            latest_data = get_latest_hour_data(crypto,i)  # Fetch only the last hour
            if latest_data:
                message = {
                    "symbol": crypto,
                    "time": latest_data["time"],
                    "open": latest_data["open"],
                    "high": latest_data["high"],
                    "low": latest_data["low"],
                    "close": latest_data["close"],
                    "volume": latest_data["volumeto"]
                }
                print("Fetched Data:", message)
                df = transformation_data(message)
                insert_data(df)

    print("Waiting 1 hour before fetching again...")
    time.sleep(3600)  # Wait 1 hour before fetching the next hour's data
