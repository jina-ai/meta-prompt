import os
import requests

def generate_embedding(input_text, task="classification"):
    api_token = os.getenv("JINA_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "jina-embeddings-v3",
        "input": [input_text],
        "task": task
    }
    response = requests.post("https://api.jina.ai/v1/embeddings", json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["data"][0]["embedding"]
    else:
        print("Error: ", response.json())
        return None

# Example usage
embedding = generate_embedding("Jina")
print(embedding)

# Reminder: Make sure your JINA_API_KEY environmental variable is set before running this code.