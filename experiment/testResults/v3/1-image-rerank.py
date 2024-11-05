import os
import requests
import json

JINA_API_KEY = os.getenv("JINA_API_KEY")

# Setup common headers
headers = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Function to classify images based on their domain using Jina Classification API
def classify_images(image_urls, labels=None):
    endpoint = "https://api.jina.ai/v1/classify"
    data = {
        "model": "jina-clip-v1",
        "input": [{"image": url} for url in image_urls]
    }
    if labels:
        data["labels"] = labels

    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return response.text

# Example usage
image_urls = [
    "https://picsum.photos/id/10/367/267",
    "https://picsum.photos/id/20/367/267",
    "https://picsum.photos/id/30/367/267"
]
labels = ["Technology", "Nature", "Architecture"]

result = classify_images(image_urls, labels)
print(json.dumps(result, indent=2))