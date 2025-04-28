# predict_price.py
import joblib
import numpy as np
from kafka_preprocess_data import prepare_data

def predict_price(crypto_symbol):
    model = joblib.load(f'{crypto_symbol}_model.pkl')
    _, latest_price = prepare_data(crypto_symbol)
    
    X_new = np.array([[latest_price, latest_price, latest_price, latest_price, 1]])
    predicted_price = model.predict(X_new)[0]
    
    print(f'🔮 Prédiction du prix de {crypto_symbol} dans une heure : {predicted_price:.2f} USD')
    return predicted_price

predict_price("BTC")