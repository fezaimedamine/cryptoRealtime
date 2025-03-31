import datetime
import requests
import time
from kafka import KafkaProducer
import json

producer=KafkaProducer(
    bootstrap_servers="localhost:9002",
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
topic="cryptoData"
"""Votre clé API CryptoCompare (optionnelle pour certaines requêtes)"""
API_KEY = "a2ea63a50f47d88207df27081157aa9b9e87c46888050bfbbfce883070f14dbd"
"""Fonction pour récupérer les données en temps réel d'une cryptomonnaie"""
def get_crypto_data(crypto_symbol, currency="USD"):
    url = f"https://min-api.cryptocompare.com/data/price?fsym={crypto_symbol}&tsyms={currency}"
    headers = {
        "Authorization": f"Apikey {API_KEY}"  # Optionnel si vous n'avez pas de clé API
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erreur lors de la récupération des données :", response.status_code)
        return None
# Fonction pour afficher les données de manière lisible
def send_crypto_data(crypto_symbol, data, currency="USD"):
    if data and currency in data:
        producer.send(topic,data)
    else:
        print(f"Aucune donnée disponible pour {crypto_symbol}.")
# Cryptomonnaies à suivre (vous pouvez en ajouter d'autres)
cryptos = ["BTC", "ETH", "XRP", "ADA", "SOL"]
# Boucle pour afficher les données en temps réel et historiques
while True:
    for crypto in cryptos:
        # Récupérer les données en temps réel
        realtime_data = get_crypto_data(crypto)
        now = datetime.datetime.now()
        realtime_data["crypto"]=crypto  
        realtime_data["time"]=now
        send_crypto_data(crypto, realtime_data)
    time.sleep(1)