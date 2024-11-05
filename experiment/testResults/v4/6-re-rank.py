import os
import requests

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
JINA_API_KEY = os.getenv("JINA_API_KEY")
headers = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "application/json"
}

def rerank_documents(query, documents):
    url = "https://api.jina.ai/v1/rerank"
    data = {
        "model": "jina-reranker-v2-base-multilingual",
        "query": query,
        "documents": documents
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["results"]
    else:
        raise Exception(f"Error in rerank_documents: {response.json()}")

def main():
    query = "Future of AI"
    documents = ["Jina", "Weaviate", "OpenAI", "Hugging Face", "Qdrant"]
    try:
        reranked_documents = rerank_documents(query, documents)
        print("Re-ranked documents based on the query 'Future of AI':")
        for doc in reranked_documents:
            print(f"Index: {doc['index']}, Text: {doc['document']['text']}, Score: {doc['relevance_score']}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()