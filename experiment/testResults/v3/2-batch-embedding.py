import os
import requests
import json

jina_api_key = os.getenv("JINA_API_KEY")
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {jina_api_key}",
    "Accept": "application/json"
}

endpoint = "https://api.jina.ai/v1/embeddings"
data = {
    "model": "jina-clip-v1",
    "input": [{"text": str(i)} for i in range(1, 101)]
}

response = requests.post(endpoint, json=data, headers=headers)
embeddings = response.json()

print(json.dumps(embeddings, indent=2))