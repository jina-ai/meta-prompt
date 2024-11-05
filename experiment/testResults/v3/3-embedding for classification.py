import os
import requests

# Read the API key from an environment variable
api_key = os.getenv("JINA_API_KEY")

# Define the endpoint and the headers for the API request
endpoint = "https://api.jina.ai/v1/embeddings"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

# Define the data/payload for the request
data = {
    "model": "jina-clip-v1",
    "input": [
        {"text": "Jina"}
    ]
}

# Make the POST request to get embeddings
response = requests.post(endpoint, headers=headers, json=data)

# Parse the response JSON and access the embeddings
embeddings = response.json().get("data", [])[0]["embedding"] if response.status_code == 200 else []

print(embeddings)