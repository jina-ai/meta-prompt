import requests
import os

# Load the Jina API key from environment variable
token = os.environ["JINA_API_KEY"]

endpoint = "https://api.jina.ai/v1/embeddings"  # The API endpoint for retrieving embeddings.

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

data = {
    "model": "jina-clip-v1",
    "normalized": True,
    "embedding_type": "float",
    "input": [{"text": str(number)} for number in range(1, 101)]
}

response = requests.post(endpoint, json=data, headers=headers)

# Assuming the response JSON structure
if response.status_code == 200:
    embeddings = response.json().get("data", [])
    # Process or handle the embeddings as needed
    # For instance, printing the embeddings
    for embedding in embeddings:
        print(f"Index: {embedding['index']}, Embedding: {embedding['embedding'][:5]}...")  # Example of handling the response
else:
    print(f"Error: {response.json().get('message', 'Unable to retrieve embeddings.')}")