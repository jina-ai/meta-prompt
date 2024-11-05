import os
import requests

# Read the API key from environment variable
api_key = os.getenv("JINA_API_KEY")

# Define the API endpoint
url = "http://api.jina.ai/v1/embeddings"

# Set the headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "accept": "application/json",
}

# Define the data payload
data = {
    "model": "jina-embeddings-v3",
    "input": ["Jina"],
    "embedding_type": "float",
    "task": "retrieval.query",
    "dimensions": 768,
    "normalized": False,
    "late_chunking": True
}

# Make the POST request
response = requests.post(url, json=data, headers=headers)

# Print the response
print(response.json())