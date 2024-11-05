import os
import requests

def generate_embedding(input_text, late_chunking=True):
    token = os.getenv("JINA_API_KEY")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "jina-embeddings-v3",
        "input": [input_text],
        "late_chunking": late_chunking
    }
    try:
        response = requests.post("https://api.jina.ai/v1/embeddings", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        return f"HTTP error: {err}"
    except Exception as err:
        return f"Error: {err}"

# Example usage:
embedding_result = generate_embedding("Jina")
print(embedding_result)