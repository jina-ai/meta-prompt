import requests
import os

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('JINA_API_KEY')}"
}

data = {
    "model": "jina-reranker-v2-base-multilingual",
    "query": "Future of AI",
    "top_n": 5,
    "documents": [
        "Jina",
        "Weaviate",
        "OpenAI",
        "Hugging Face",
        "Qdrant"
    ]
}

response = requests.post("https://api.jina.ai/v1/rerank", headers=headers, json=data)
results = response.json()
for result in results.get('results', []):
    print(result['document']['text'], result['relevance_score'])