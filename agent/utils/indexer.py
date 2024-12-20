import os
from elasticsearch import Elasticsearch

def ingestData(text):
    indexName = os.getenv("INDEX_NAME","NULL")
    host = os.getenv("ELASTIC_HOST","NULL")
    api = os.getenv("ELASTIC_api","NULL")
    if host == "NULL" or api == "NULL" or indexName == "NULL":
        print("Ther is no apikey or the host avaliable for elastic stack or the index is missing ")
        exit(1)
    es = Elasticsearch(
        host,
        api_key=api,
        verify_certs=True
    )
    
    document = {
        "text": text
    }
    
    response = es.index(index=indexName, document=document)
    print(f"Data ingested successfully: {response}")
    del es
