import os
import requests

# Read JINA API key from environment
api_key = os.getenv("JINA_API_KEY")

# Embed text with Jina AI Embeddings API
texts = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

response = requests.post(
    "http://api.jina.ai/v1/embeddings",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "accept": "application/json"
    },
    json={
        "model": "jina-embeddings-v3",
        "input": texts,
        "embedding_type": "float",
        "task": "retrieval.query"
    }
)

if response.status_code == 200:
    embeddings = response.json()["data"]
    for embedding in embeddings:
        print(embedding["index"], embedding["embedding"])
else:
    print(f"Failed to create embeddings: {response.status_code}, {response.text}")