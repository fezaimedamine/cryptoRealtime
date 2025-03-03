from kafka import KafkaConsumer
from elasticsearch import Elasticsearch

def sendData(data):
    host = "https://localhost:9200"
    username = "elastic"
    password = "GsIOFCQyE*nsNllQJk38"

    try:
        es = Elasticsearch(
            hosts=[host],
            basic_auth=(username, password),
            verify_certs=False #only for local testing, remove in production.
        )
        index_name = "crypto_prices"
        # Send data to Elasticsearch
        response = es.index(index=index_name, document=data)
        print(response)
    except Exception as e:
        print(f"Connection to Elasticsearch failed: {e}")



topic="cryptoData"
consumer = KafkaConsumer(
    topic,
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',  # Commence à lire depuis le début du topic
)
cryptos = ["BTC", "ETH", "XRP", "ADA", "SOL"]
"""function to read data from topic kafka"""
def readDataFromKafka():
    data={}
    i=0
    try: 
        for message in consumer:
            if(message["USD"]):
                data[cryptos[i]]=message["USD"]
            else : data[cryptos[i]]=0
            i+=1
    except Exception as e:
        print("errer au niveau du lecture du données depuis kafka")
    return data


