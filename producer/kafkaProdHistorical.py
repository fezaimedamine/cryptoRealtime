import requests
import json
import time
from kafka import KafkaProducer

# Kafka configuration
KAFKA_TOPIC = "crypto_historical"
KAFKA_BROKER = "localhost:9092"
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# CryptoCompare API Key
API_KEY = "a2ea63a50f47d88207df27081157aa9b9e87c46888050bfbbfce883070f14dbd"

# Function to fetch only the latest hour of historical data
def get_latest_hour_data(crypto_symbol, currency="USD"):
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={crypto_symbol}&tsym={currency}&limit=1"
    headers = {"Authorization": f"Apikey {API_KEY}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["Data"]["Data"][-1]  # Only the latest hour
    else:
        print(f"Error fetching data for {crypto_symbol}: {response.status_code}")
        return None

# Cryptos to track
cryptos = ["BTC", "ETH", "XRP", "ADA", "SOL"]

while True:
    for crypto in cryptos:
        latest_data = get_latest_hour_data(crypto)  # Fetch only the last hour
        
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
            producer.send(KAFKA_TOPIC, message)
    
    print("Waiting 1 hour before fetching again...")
    time.sleep(3600)  # Wait 1 hour before fetching the next hour's data
