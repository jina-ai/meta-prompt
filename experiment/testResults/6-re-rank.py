import os
import requests

token = os.environ["JINA_API_KEY"]
endpoint = "https://api.jina.ai/v1/rerank"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}
data = {
    "model": "jina-colbert-v2",
    "query": "Future of AI",
    "top_n": 5,
    "documents": [
        "Jina",
        "Weaviate",
        "OpenAI",
        "Hugging Face",
        "Qdrant"
    ]
}

response = requests.post(endpoint, headers=headers, json=data)
print(response.json())