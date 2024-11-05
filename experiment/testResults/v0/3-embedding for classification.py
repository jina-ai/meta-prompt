import os
import requests

# Reading the JINA_API_KEY from environment variable
api_key = os.environ['JINA_API_KEY']

# Preparing the headers for the request
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

# Preparing the data for the request
data = {
    "model": "jina-embeddings-v3",
    "input": ["Jina"],
    "embedding_type": "float",
    "task": "classification",
}

# Making the POST request to the embeddings API
response = requests.post('http://api.jina.ai/v1/embeddings', headers=headers, json=data)

# Checking the response
if response.status_code == 200:
    # Extracting the embeddings
    embeddings = response.json().get('data', [])
    print(embeddings)
else:
    print("Error:", response.text)