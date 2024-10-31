import os
import requests
import json

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
JINA_API_KEY = os.getenv('JINA_API_KEY')
headers = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def generate_embedding(input_text):
    url = "https://api.jina.ai/v1/embeddings"
    payload = json.dumps({
        "model": "jina-embeddings-v3",
        "input": [input_text],
        "late_chunking": True
    })
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.json()}")
            return None
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return None

# Example usage:
if __name__ == "__main__":
    text = "Jina"
    embedding_response = generate_embedding(text)
    if embedding_response:
        print(embedding_response)