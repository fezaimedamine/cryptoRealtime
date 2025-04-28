# train_model.py
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import pandas as pd
import numpy as np
from kafka_preprocess_data import prepare_data
import os
from datetime import datetime
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Liste des cryptos à entraîner
CRYPTO_LIST = ['BTC', 'ETH', 'XRP', 'SOL', 'ADA']

def evaluate_model(model, X_test, y_test):
    """Évalue les performances du modèle"""
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    return {
        'mae': round(mae, 4),
        'rmse': round(rmse, 4),
        'accuracy': round(model.score(X_test, y_test), 4)
    }

def train_model(crypto_symbol):
    """Entraîne et sauvegarde un modèle pour une crypto donnée"""
    try:
        logger.info(f" Début de l'entraînement pour {crypto_symbol}")
        
        # 1. Préparation des données
        historical_df, _ = prepare_data(crypto_symbol)
        if historical_df.empty:
            raise ValueError(f"Aucune donnée disponible pour {crypto_symbol}")
        
        # 2. Feature engineering
        X = historical_df[['open', 'high', 'low', 'close', 'volume']]
        y = historical_df['close'].shift(-1).dropna()
        X = X[:-1]
        
        # 3. Séparation train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, shuffle=False
        )
        
        # 4. Entraînement du modèle
        model = RandomForestRegressor(
            n_estimators=200,
            max_depth=10,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        
        # 5. Évaluation
        metrics = evaluate_model(model, X_test, y_test)
        
        # 6. Sauvegarde
        os.makedirs('models', exist_ok=True)
        model_path = f'{crypto_symbol}_model.pkl'
        joblib.dump(model, model_path)
        
        logger.info(f"""
 Entraînement terminé pour {crypto_symbol}
 Performances:
- MAE: {metrics['mae']}
- RMSE: {metrics['rmse']}
- R²: {metrics['accuracy']}
 Modèle sauvegardé: {model_path}
        """)
        
        return model, metrics
        
    except Exception as e:
        logger.error(f" Erreur lors de l'entraînement pour {crypto_symbol}: {str(e)}")
        raise

if __name__ == "__main__":
    # Entraînement pour toutes les cryptos
    for crypto in CRYPTO_LIST:
        try:
            train_model(crypto)
        except Exception as e:
            logger.error(f"Échec de l'entraînement pour {crypto}: {e}")
            continue