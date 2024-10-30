import requests
import os

token = os.environ["JINA_API_KEY"]
candidates = ["Jina", "Weaviate", "OpenAI", "Hugging Face", "Qdrant"]

endpoint = "https://api.jina.ai/v1/rerank"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}
data = {
    "model": "jina-colbert-v2",
    "query": "Future of AI",
    "top_n": 5,
    "documents": candidates
}

response = requests.post(endpoint, headers=headers, json=data)
if response.status_code == 200:
    reranked_results = response.json()["data"]["results"]
    reranked_candidates = [result["document"]["text"] for result in reranked_results]
    print("Re-ranked candidates for 'Future of AI':", reranked_candidates)
else:
    print("Error during re-ranking:", response.json())