import os
import requests

# Gather API key from environment
api_key = os.getenv('JINA_API_KEY')

# Create the input data
input_texts = [str(i) for i in range(1, 101)]  # Create a list of numbers from 1 to 100 as strings

# Define the API request parameters
url = "http://api.jina.ai/v1/embeddings"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
payload = {
    "model": "jina-embeddings-v3",
    "input": input_texts,
    "embedding_type": "float",
    "task": "retrieval.query",
    # Optional parameters can be added here based on requirements
}

# Make the request
response = requests.post(url, json=payload, headers=headers)

# Check response
if response.status_code == 200:
    data = response.json()
    print("Embeddings generated successfully.")
    print(data)
else:
    print(f"Failed to generate embeddings. Status code: {response.status_code}, Response message: {response.text}")