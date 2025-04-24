from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from datetime import datetime
import joblib
import numpy as np
from kafka_preprocess_data import prepare_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data):
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception as e:
                print(f"Erreur d'envoi WebSocket : {e}")

manager = ConnectionManager()

crypto_symbol = "BTC"  # Tu peux changer selon ce que tu veux charger

async def price_updater():
    try:
        model = joblib.load(f"{crypto_symbol}_model.pkl")
    except Exception as e:
        print(f"Erreur de chargement du modèle : {e}")
        return

    while True:
        try:
            current_price, _ = prepare_data(crypto_symbol)
            
            X_new = np.array([[current_price] * 4 + [1]])  # 5 features
            prediction = model.predict(X_new)[0]

            data = {
                "BTC": {
                    "current_price": round(current_price, 2),
                    "predicted_price": round(prediction, 2),
                    "timestamp": datetime.now().isoformat(),
                    "status": "success"
                }
            }

            await manager.broadcast(data)

        except Exception as e:
            print(f"Erreur pendant l’update : {e}")

        await asyncio.sleep(5)  # Toutes les 5 secondes


@app.on_event("startup")
async def startup():
    asyncio.create_task(price_updater())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Permet de garder la connexion ouverte
    except:
        await manager.disconnect(websocket)
