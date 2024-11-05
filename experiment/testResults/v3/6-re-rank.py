import os
import requests

# Environment variable for API key
JINA_API_KEY = os.getenv("JINA_API_KEY")

# Headers including Authorization token read from environment
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "application/json"
}

# Data for the re-ranker API
data = {
    "model": "jina-colbert-v2",
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

# Endpoint for the re-ranker API
endpoint = "https://api.jina.ai/v1/rerank"

# Make the request to the re-ranker API
response = requests.post(endpoint, headers=headers, json=data)

# Print the re-ranked results
if response.status_code == 200:
    print("Re-ranked words for 'Future of AI':")
    for idx, result in enumerate(response.json()["data"]["results"], start=1):
        print(f"{idx}. {result['document']['text']} (Relevance score: {result['relevance_score']})")
else:
    print("Failed to re-rank the words. Please check the inputs and try again.")