import os
import requests
import json

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
JINA_API_KEY = os.getenv("JINA_API_KEY")

def generate_embedding(text):
    url = "https://api.jina.ai/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    data = {
        "model": "jina-embeddings-v3",
        "input": [text],
        "embedding_type": "float",
        "task": "classification"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to generate embedding:", response.text)
        return None

# Example usage
text = "Jina"
embedding = generate_embedding(text)
print(embedding)