import os
import requests

def generate_embedding(text, return_type='binary'):
    api_key = os.getenv('JINA_API_KEY')
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "jina-embeddings-v3",
        "input": [text],
        "embedding_type": return_type
    }
    
    response = requests.post("https://api.jina.ai/v1/embeddings", json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['data'][0]['embedding_vector']
    else:
        return "Error: " + response.json()['error']['message']

# Example usage:
embedding_vector = generate_embedding("Jina", "binary")
print(embedding_vector)