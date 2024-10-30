import requests
import os
import json

token = os.environ["JINA_API_KEY"]

endpoint = "https://api.jina.ai/v1/embeddings"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
data = {
    "model": "jina-clip-v1",
    "normalized": True,
    "input": [
        {"text": "Jina"}
    ]
}

response = requests.post(endpoint, headers=headers, json=data)
print(response.json())