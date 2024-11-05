import os
import requests
import json

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
JINA_API_KEY = os.getenv("JINA_API_KEY")

def generate_embedding(input_text):
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "model": "jina-embeddings-v3",
        "input": [input_text],
        "embedding_type": "binary"
    }
    response = requests.post("https://api.jina.ai/v1/embeddings", headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.json()}")

# Example usage
if __name__ == "__main__":
    input_text = "Jina"
    result = generate_embedding(input_text)
    print(result)