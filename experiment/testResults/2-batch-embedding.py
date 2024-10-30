import requests
import os
import json

# Load the token from environment variables
token = os.environ["JINA_API_KEY"]

# API endpoint for generating embeddings
endpoint = "https://api.jina.ai/v1/embeddings"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

# Preparing the data - converting numbers 1 to 100 into text
numbers_in_text = [{"text": str(number)} for number in range(1, 101)]

data = {
    "model": "jina-clip-v1",
    "normalized": True,
    "embedding_type": "float",
    "input": numbers_in_text
}

response = requests.post(endpoint, json=data, headers=headers)
embeddings_response = response.json()

# Check if the request was successful
if embeddings_response["code"] == 200:
    # Output the embeddings
    for item in embeddings_response["data"]:
        index = item["index"]
        embedding = item["embedding"]
        print(f"Number: {numbers_in_text[index]['text']}, Embedding: {embedding[:5]}...") # Displaying only the first 5 dimensions for brevity
else:
    print("Error generating embeddings:", embeddings_response.get("message", "Unknown error"))