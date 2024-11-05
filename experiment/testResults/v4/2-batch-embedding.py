import requests
import os
import json

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
api_key = os.getenv('JINA_API_KEY')
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def generate_embeddings(text_data):
    url = "https://api.jina.ai/v1/embeddings"
    payload = {
        "model": "jina-embeddings-v3",
        "input": text_data,
        "embedding_type": "float"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        print("Error while generating embeddings:", response.json())

def main():
    numbers_in_text = [str(n) for n in range(1, 101)]
    embeddings = generate_embeddings(numbers_in_text)
    if embeddings:
        # Process or save your embeddings here
        print(embeddings)

if __name__ == "__main__":
    main()