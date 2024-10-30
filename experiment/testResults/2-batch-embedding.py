import requests
import json
import os

# Load the Jina API key from environment variables
token = os.environ["JINA_API_KEY"]

# Define the endpoint URL and header for authentication and content type
endpoint = "https://api.jina.ai/v1/embeddings"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# Create a list of numbers from 1 to 100 in text form
numbers_text = [str(number) for number in range(1, 101)]

# Define the data payload for the request
data = {
    "model": "jina-clip-v1",  # Specify the model to be used for generating embeddings
    "data": [{"text": number} for number in numbers_text]
}

# Make the POST request to the Jina embeddings endpoint
response = requests.post(endpoint, headers=headers, json=data)

# Check if the request was successful
if response.status_code == 200:
    embeddings = response.json()
    print("Embeddings generated successfully.")
    # Process or save the embeddings as needed
    # For example, print the embeddings for the first few numbers
    for i, embedding in enumerate(embeddings['data'][:5]):
        print(f"Number: {numbers_text[i]}, Embedding: {embedding['embedding'][:5]}...")  # Print the first 5 dimensions for brevity
else:
    print("Failed to generate embeddings. Status code:", response.status_code)