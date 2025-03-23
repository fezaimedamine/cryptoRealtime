from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "cryptoData",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

for message in consumer:
    print(f"Received: {message.value}")


# ////////////////////////////////////////////////////////////// 
def on_message(ws, message):
    """
    Fonction de rappel pour traiter les messages reçus via WebSocket.
    """
    try:
        data = json.loads(message)
        print(f"Reçu des données : {data}")

        # Envoyer les données à Kafka
        producer.send(kafka_topic, value=data)
        producer.flush()
        print(f"Données envoyées à Kafka : {data}")
    except Exception as e:
        print(f"Erreur lors du traitement du message : {e}")

def on_error(ws, error):
    """
    Fonction de rappel pour gérer les erreurs WebSocket.
    """
    print(f"Erreur WebSocket : {error}")

def on_close(ws, close_status_code, close_msg):
    """
    Fonction de rappel lorsque la connexion WebSocket est fermée.
    """
    print(f"Connexion WebSocket fermée : {close_msg}")

def on_open(ws):
    """
    Fonction de rappel lorsque la connexion WebSocket est ouverte.
    """
    print("Connexion WebSocket établie")
    # S'abonner à des symboles boursiers (exemple : Apple, Microsoft)
    subscribe_message = {
        "type": "subscribe",
        "symbol": "AAPL"  # Symbole boursier
    }
    ws.send(json.dumps(subscribe_message))
    print("Abonnement envoyé :", subscribe_message)

# Configuration WebSocket
ws = websocket.WebSocketApp(
    websocket_url,
    on_message=on_message,
    
)


# Démarrer la connexion WebSocket
print("Démarrage de la connexion WebSocket...")

ws.on_open = on_open
ws.run_forever()