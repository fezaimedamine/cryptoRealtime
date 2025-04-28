# fetch_realtime_data.py
from elasticsearch import Elasticsearch

def fetch_realtime_price(crypto_symbol):
    # Elasticsearch Configuration
    host = "https://localhost:9200" 
    username = "elastic"
    password = "GsIOFCQyE*nsNllQJk38"
    index_name = "crypto_prices"
    try:
        es = Elasticsearch(
            hosts=[host],
            basic_auth=(username, password),
            verify_certs=False  # Only for local testing; remove in production
        )
        print(" Connected to Elasticsearch!")
    except Exception as e:
        print(f" Connection to Elasticsearch failed: {e}")
        exit()

    query = {
        "query": {
            "match": {"crypto": crypto_symbol}
        },
        "size": 1,
        "sort": [{"timestamp": {"order": "desc"}}]
    }

    # Query Elasticsearch for the latest price
    response = es.search(index="crypto_prices", body=query)
    data = response['hits']['hits']
    print(data[0]['_source']['usd'])

    # Return the latest USD price
    return data[0]['_source']['usd'] if data else None
