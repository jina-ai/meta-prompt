import requests
import os

token = os.environ["JINA_API_KEY"]

endpoint = "https://api.jina.ai/v1/embeddings"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}
data = {
    "model": "jina-clip-v1",
    "normalized": True,
    "embedding_type": "float",
    "input": [{"text": "Jina"}]
}

response = requests.post(endpoint, json=data, headers=headers)
print(response.json())