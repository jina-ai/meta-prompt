import os
import requests

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
JINA_API_KEY = os.environ.get("JINA_API_KEY")

def generate_embedding(input_text, model="jina-embeddings-v3", embedding_type="binary"):
    url = "https://api.jina.ai/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "input": [input_text],
        "embedding_type": embedding_type
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise error if request failed
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")

embedding_result = generate_embedding("Jina")
print(embedding_result)