import requests
import os

endpoint = "https://api.jina.ai/v1/classify"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('JINA_API_KEY')}"
}

data = {
    "model": "jina-clip-v1",
    "input": [
        {"text": "A sleek smartphone with a high-resolution display and multiple camera lenses"},
        {"text": "Fresh sushi rolls served on a wooden board with wasabi and ginger"},
        {"image": "https://picsum.photos/id/11/367/267"},
        {"image": "https://picsum.photos/id/22/367/267"},
        {"text": "Vibrant autumn leaves in a dense forest with sunlight filtering through"},
        {"image": "https://picsum.photos/id/8/367/267"}
    ],
    "labels": [
        "Technology and Gadgets",
        "Food and Dining",
        "Nature and Outdoors",
        "Urban and Architecture"
    ]
}

response = requests.post(endpoint, headers=headers, json=data)
print(response.json())