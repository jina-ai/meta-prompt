import os
import requests
import json

# Read API key from environment variable
api_key = os.getenv('JINA_API_KEY')

# Define the headers
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'accept': 'application/json'
}

# Define the request payload
payload = {
    "model": "jina-embeddings-v3",
    "input": ["Jina"],
    "embedding_type": "binary"
}

# Make the HTTP POST request
response = requests.post('http://api.jina.ai/v1/embeddings', headers=headers, data=json.dumps(payload))

# Print binary embedding
print(response.json())