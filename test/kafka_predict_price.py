# predict.py
import numpy as np
import tensorflow as tf
from kafka_fetch_historical_data import fetch_historical_data
from kafka_preprocess_data import preprocess_data
from kafka_calcul_accurecy import evaluate_model

def load_model(crypto_symbol):
    return tf.keras.models.load_model(f"{crypto_symbol}_lstm_model.h5")

def predict_next_price(model, X_new, scaler):
    predicted_price = model.predict(X_new)
    # Inverser la normalisation du prix prédit
    predicted_price = scaler.inverse_transform(np.column_stack([np.zeros((X_new.shape[0], 4)), predicted_price]))[:, -1]
    return predicted_price

def prepare_input_for_prediction(latest_price, historical_data, scaler):
    num_timesteps_required = 59  # Nombre de timesteps requis

    # Transformation du dernier prix
    latest_price_df = np.array([[latest_price] * historical_data.shape[2]])  # Correspond au nombre de features
    latest_price_scaled = scaler.transform(latest_price_df)

    # Reshape et duplication pour correspondre au batch_size
    batch_size = historical_data.shape[0]
    latest_price_scaled = np.tile(latest_price_scaled, (batch_size, 1, 1))  # Dupliquer pour chaque échantillon du batch

    # Vérification et ajustement de historical_data
    if historical_data.shape[1] < num_timesteps_required:
        padding = np.zeros((batch_size, num_timesteps_required - historical_data.shape[1], historical_data.shape[2]))
        historical_data = np.concatenate((padding, historical_data), axis=1)

    # Sélection des 59 derniers timesteps
    historical_data_slice = historical_data[:, -num_timesteps_required:, :]

    # Concaténation sur l'axe temporel (axis=1)
    X_new = np.concatenate((historical_data_slice, latest_price_scaled), axis=1)

    return X_new

if __name__ == "__main__":
    crypto_symbol = "BTC"

    # Chargement du modèle et récupération des données historiques
    model = load_model(crypto_symbol)
    historical_data = fetch_historical_data(crypto_symbol)
    X, y, scaler = preprocess_data(historical_data)

    # Récupération du prix en temps réel (ou valeur de test)
    latest_price = 83528.17  # Valeur de test

    if latest_price:
        # Préparation des données pour la prédiction
        X_new = prepare_input_for_prediction(latest_price, X, scaler)
        
        # Prédiction du prix
        predicted_prices = predict_next_price(model, X_new, scaler)

        # Afficher la prédiction
        print(f"Prix prédit pour {crypto_symbol} : {predicted_prices} USD")
