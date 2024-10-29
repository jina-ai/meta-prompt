import os
import requests

# Retrieve the Jina API key from the environment variable
JINA_API_KEY = os.getenv("JINA_API_KEY")

# Jina embeddings API endpoint
endpoint = "https://api.jina.ai/v1/embeddings"

# Headers including the authorization token
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {JINA_API_KEY}"
}

# Data payload for the request
data = {
    "model": "jina-embeddings-v3",
    "task": "text-matching",
    "dimensions": 1024,
    "input": [str(i) for i in range(1, 101)]
}

# Sending the POST request to Jina AI to generate embeddings
response = requests.post(endpoint, json=data, headers=headers)

# Printing the response from Jina AI
print(response.json())