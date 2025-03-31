# train_model.py
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
from kafka_preprocess_data import prepare_data

def train_model(crypto_symbol):
    historical_df, _ = prepare_data(crypto_symbol)
    X = historical_df[['open', 'high', 'low', 'close', 'volume']]
    y = historical_df['close'].shift(-1).dropna()
    X = X[:-1]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    joblib.dump(model, f'{crypto_symbol}_model.pkl')
    print("✅ Modèle entraîné et sauvegardé.")

train_model('BTC')