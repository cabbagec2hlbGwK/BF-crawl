import os
from datetime import datetime, timezone
from elasticsearch import Elasticsearch

def ingestData(text, url, pageType):
    indexName = os.getenv("INDEX_NAME","NULL")
    host = os.getenv("ELASTIC_HOST","NULL")
    api = os.getenv("ELASTIC_API","NULL")
    print(host, api, indexName, "-------------------")
    if host == "NULL" or api == "NULL" or indexName == "NULL":
        print("Ther is no apikey or the host avaliable for elastic stack or the index is missing ")
        exit(1)
    es = Elasticsearch(
        host,
        api_key=api,
        verify_certs=True
    )
    
    document = {
        "text": text,
        "Url":url,
        "pageType":pageType,
        "timeStamp":datetime.now(timezone.utc).__str__()
    }
    
    response = es.index(index=indexName, document=document)
    print(f"Data ingested successfully: {response}")
    del es
