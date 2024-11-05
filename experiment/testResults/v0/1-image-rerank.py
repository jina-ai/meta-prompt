import os
import requests

JINA_API_KEY = os.getenv("JINA_API_KEY")

headers = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Content-Type": "application/json",
}

data = {
    "model": "jina-clip-v1",
    "input": ["image1_url", "image2_url", "image3_url"],
    "embedding_type": "float",
    "task": "classification",
    "dimensions": 768,
}

response = requests.post('http://api.jina.ai/v1/embeddings', headers=headers, json=data)
print(response.json())