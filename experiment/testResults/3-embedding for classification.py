import requests

endpoint = "https://api.jina.ai/v1/embeddings"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('JINA_API_KEY')}"
}
data = {
    "model": "jina-embeddings-v3",
    "task": "text-matching",
    "dimensions": 1024,
    "late_chunking": False,
    "embedding_type": "float",
    "input": ["Jina"]
}
response = requests.post(endpoint, json=data, headers=headers)
print(response.json())