import os
import requests
import json

# Reading the API key from environment variable
JINA_API_KEY = os.getenv('JINA_API_KEY')

headers = {
    'Authorization': f'Bearer {JINA_API_KEY}',
    'Content-Type': 'application/json',
}

data = {
    "model": "jina-embeddings-v3",
    "input": ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
}

response = requests.post('https://api.jina.ai/v1/embeddings', headers=headers, data=json.dumps(data))

if response.status_code == 200:
    embeddings = response.json()['data']
    print("Embeddings generated successfully:")
    for i, embedding in enumerate(embeddings):
        print(f"Text: {data['input'][i]}, Embedding: {embedding['embedding'][:10]}...") # Showing just part of the embedding for brevity
else:
    print(f"Error: {response.json()['message']}")
