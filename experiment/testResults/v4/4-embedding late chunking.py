import os
import requests

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
API_KEY = os.getenv("JINA_API_KEY")
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def generate_embedding(input_text):
    payload = {
        "model": "jina-embeddings-v3",
        "input": [input_text],
        "late_chunking": True
    }
    response = requests.post("https://api.jina.ai/v1/embeddings", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return response.text

# Example usage
embedding_response = generate_embedding("Jina")
print(embedding_response)