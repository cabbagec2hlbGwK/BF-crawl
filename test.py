import requests
import json


def getCapta():
    endpoint = "http://localhost:5000/capta"
    with open("captas\\capta.png","rb") as img:
        files = {'file': img}
        response = requests.post(endpoint, files=files)
        print(json.loads(response.content))


getCapta()

