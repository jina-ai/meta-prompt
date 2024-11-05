import requests
import os

# Reading the Jina API Key from environment variable
api_key = os.getenv("JINA_API_KEY")

# Setting the API endpoint for embedding generation
endpoint = "https://api.jina.ai/v1/embeddings"

# Preparing the headers with the Jina API Key and specifying JSON content type and accept headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

# Preparing the request data with model details and input text
data = {
    "model": "jina-clip-v1",  # Model for generating embeddings
    "input": [{"text": "Jina"}],  # Text input for which embedding needs to be generated
}

# Sending the POST request to Jina AI API to generate embedding
response = requests.post(endpoint, json=data, headers=headers)

# Checking if the request was successful
if response.status_code == 200:
    # Extracting embedding from response
    embedding = response.json().get("data")[0].get("embedding")
    print("Embedding for 'Jina':", embedding)
else:
    print("Failed to generate embedding. Status code:", response.status_code)