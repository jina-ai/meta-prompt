import os
import requests

# Fetching the Jina API Key from the environment variable
JINA_API_KEY = os.getenv("JINA_API_KEY")

# Setting up the endpoint and headers for the request
endpoint = "https://api.jina.ai/v1/embeddings"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "application/json"
}

# Preparing the data payload with the input texts
data = {
    "model": "jina-clip-v1",
    "input": [
        {"text": "one"},
        {"text": "two"},
        {"text": "three"},
        {"text": "four"},
        {"text": "five"},
        {"text": "six"},
        {"text": "seven"},
        {"text": "eight"},
        {"text": "nine"},
        {"text": "ten"}
    ]
}

# Sending the POST request to the Jina Embeddings API
response = requests.post(endpoint, json=data, headers=headers)

# Checking if the request was successful
if response.status_code == 200:
    print("Embeddings generated successfully")
    embeddings = response.json().get("data")
    for index, item in enumerate(embeddings):
        print(f"Embedding for '{data['input'][index]['text']}':", item["embedding"])
else:
    print("Failed to generate embeddings. Error:", response.text)