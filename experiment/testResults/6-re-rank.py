import os
import requests

token = os.environ["JINA_API_KEY"]
endpoint = "https://api.jina.ai/v1/rerank"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
data = {
    "model": "jina-colbert-v2",
    "query": "Future of AI",
    "top_n": 5,
    "documents": [
        "Jina AI is a Neural Search Company building an open-source search framework for businesses and developers",
        "Weaviate is an open-source search engine powered by machine learning, specifically designed for vector search",
        "OpenAI is an AI research and deployment company creating and promoting friendly AI for the benefit of all",
        "Hugging Face is a community and data science platform for developers to build, train and deploy machine learning models",
        "Qdrant is an open-source vector search engine that helps power efficient similarity search and storage of vector embeddings"
    ]
}

response = requests.post(endpoint, headers=headers, json=data)
print(response.json())