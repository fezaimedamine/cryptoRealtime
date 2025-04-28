import pytest
from fastapi.testclient import TestClient
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
import asyncio
import json

from Scripts_Python.main import app, manager  # Remplace 'ton_fichier_app' par le nom de ton fichier sans .py

client = TestClient(app)
@pytest.mark.asyncio
async def test_websocket_connection():
    """Test de connexion et déconnexion WebSocket"""
    async with client.websocket_connect("/ws") as websocket:
        await websocket.send_text("ping")  # Envoyer un message pour maintenir la connexion
        assert websocket.application_state.name == "CONNECTED"
    # Après fermeture
    assert websocket.application_state.name == "DISCONNECTED"


@pytest.mark.asyncio
async def test_broadcast_message():
    """Test que le manager envoie bien un message à tous les clients"""
    # Simuler un websocket client
    async with client.websocket_connect("/ws") as websocket:
        data = {
            "BTC": {
                "current_price": 50000.0,
                "predicted_price": 50500.0,
                "timestamp": "2025-04-28T12:00:00",
                "status": "success"
            }
        }
        
        # Broadcast
        await manager.broadcast(data)
        
        # Réception
        received_data = await websocket.receive_json()
        assert received_data == data


@pytest.mark.asyncio
async def test_price_updater(monkeypatch):
    """Test du price_updater avec un modèle simulé"""
    from ton_fichier_app import price_updater, crypto_symbol

    class DummyModel:
        def predict(self, X):
            return [12345.67]  # Valeur prédite simulée

    # Forcer prepare_data à retourner un prix fixe
    async def dummy_prepare_data(symbol):
        return 50000.0, None

    # Forcer joblib.load à retourner un DummyModel
    monkeypatch.setattr("ton_fichier_app.joblib.load", lambda x: DummyModel())
    monkeypatch.setattr("ton_fichier_app.prepare_data", dummy_prepare_data)

    # Créer une tâche qui tourne une seule fois pour tester
    async def limited_price_updater():
        await price_updater()
        await asyncio.sleep(0.1)

    # Exécuter la tâche
    task = asyncio.create_task(limited_price_updater())
    await asyncio.sleep(0.2)
    task.cancel()  # On annule pour ne pas qu'il tourne à l'infini

