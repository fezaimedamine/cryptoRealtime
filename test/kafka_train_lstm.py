# train_lstm.py
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from kafka_preprocess_data import preprocess_data
from kafka_fetch_historical_data import fetch_historical_data

def build_lstm_model(X):
    # Définir le modèle LSTM
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(1)  # Sortie unique : prix prédit
    ])
    # Compiler le modèle
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    return model

def train_lstm_model(crypto_symbol):
    # Récupérer les données historiques
    df = fetch_historical_data(crypto_symbol)
    
    # Prétraiter les données
    X, y, scaler = preprocess_data(df)

    # Construire le modèle LSTM
    model = build_lstm_model(X)

    # Entraîner le modèle
    model.fit(X, y, epochs=20, batch_size=32)

    # Sauvegarder le modèle entraîné
    model.save(f"{crypto_symbol}_lstm_model.h5")

    return model, scaler
