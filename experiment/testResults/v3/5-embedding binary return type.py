import requests
import os

JINA_API_KEY = os.getenv('JINA_API_KEY')

endpoint = "https://api.jina.ai/v1/embeddings"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "application/json"
}

data = {
    "model": "jina-clip-v1",
    "input": [{"text": "Jina"}]
}

response = requests.post(endpoint, json=data, headers=headers)
print(response.json())