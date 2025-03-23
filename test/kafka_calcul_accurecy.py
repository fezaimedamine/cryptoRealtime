from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def evaluate_model(y_real, y_pred):
    mae = mean_absolute_error(y_real, y_pred)
    mse = mean_squared_error(y_real, y_pred)
    rmse = np.sqrt(mse)  # Racine carrée du MSE
    mape = np.mean(np.abs((y_real - y_pred) / y_real)) * 100  # En pourcentage

    print(f"📊 Évaluation du modèle :")
    print(f"➡️ MAE  : {mae:.4f}")
    print(f"➡️ MSE  : {mse:.4f}")
    print(f"➡️ RMSE : {rmse:.4f}")
    print(f"➡️ MAPE : {mape:.2f} %")

    return mae, mse, rmse, mape
