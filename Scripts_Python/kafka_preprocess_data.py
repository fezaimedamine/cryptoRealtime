# process_data.py
import pandas as pd
from kafka_fetch_historical_data import fetch_historical_data
from kafka_fetch_realtime_data import fetch_realtime_price
#from fetch_realtime_data import fetch_realtime_price

def prepare_data(crypto_symbol):
    historical_df = fetch_historical_data(crypto_symbol)
    latest_price = fetch_realtime_price(crypto_symbol)
    
    if latest_price is None:
        raise ValueError("Aucune donnée en temps réel disponible.")
    
    historical_df['returns'] = historical_df['close'].pct_change()
    historical_df.dropna(inplace=True)
    
    return latest_price, historical_df 