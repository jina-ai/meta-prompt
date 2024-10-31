import os
import requests

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
JINA_API_KEY = os.getenv("JINA_API_KEY")
headers = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

def generate_embedding(text):
    url = "https://api.jina.ai/v1/embeddings"
    payload = {
        "model": "jina-embeddings-v3",
        "input": [text],
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["data"][0]["embedding"]
    else:
        return None

# Example usage
if __name__ == "__main__":
    text = "Jina"
    embedding = generate_embedding(text)
    if embedding:
        print("Embedding generated successfully.")
    else:
        print("Failed to generate embedding.")