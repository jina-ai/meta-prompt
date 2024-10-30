import os
import requests

token = os.environ["JINA_API_KEY"]
endpoint = "https://api.jina.ai/v1/classify"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
data = {
    "model": "jina-clip-v1",
    "input": [
        {"image": "https://picsum.photos/id/11/367/267"},
        {"image": "https://picsum.photos/id/22/367/267"},
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