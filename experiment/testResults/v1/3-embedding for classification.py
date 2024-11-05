import os
import requests

def generate_embedding(text):
    api_key = os.getenv("JINA_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "jina-embeddings-v3",
        "input": [text],
        "task": "classification"
    }
    try:
        response = requests.post("https://api.jina.ai/v1/embeddings", json=payload, headers=headers)
        response.raise_for_status()
        embeddings = response.json()
        return embeddings.get("data")[0].get("embedding_vector")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

embedding_vector = generate_embedding("Jina")
print(embedding_vector)