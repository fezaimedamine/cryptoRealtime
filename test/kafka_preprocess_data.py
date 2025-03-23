# preprocess_data.py
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def preprocess_data(historical_df):
    # Sélectionner les features (open, high, low, close, volume)
    features = ['open', 'high', 'low', 'close', 'volume']
    data = historical_df[features].values

    # Normalisation des données avec MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data)

    # Préparer les données pour le modèle LSTM (séquences X et y)
    X, y = [], []
    for i in range(60, len(data_scaled)):  # Utilisation des 60 valeurs précédentes pour prédiction
        X.append(data_scaled[i-60:i])  # Derniers 60 pas de temps
        y.append(data_scaled[i, 3])    # Prix de clôture prédit (colonne 'close')

    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], len(features)))

    return X, y, scaler
