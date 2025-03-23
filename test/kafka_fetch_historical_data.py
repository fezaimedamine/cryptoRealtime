# kafka_fetch_historical_data.py
from pymongo import MongoClient
import pandas as pd

def fetch_historical_data(crypto_symbol):
    client = MongoClient('mongodb://localhost:27017')
    db = client['crypto']
    collection = db['cryptoHistorical']

    historical_data = collection.find({"symbol": crypto_symbol})
    historical_df = pd.DataFrame(list(historical_data))

    # Sélectionner les colonnes nécessaires
    historical_df = historical_df[['time', 'open', 'high', 'low', 'close', 'volume']]
    historical_df['time'] = pd.to_datetime(historical_df['time'])
    historical_df = historical_df.sort_values(by='time')

    return historical_df
