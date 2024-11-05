import os
import requests

def rerank_documents(query, documents):
    url = "https://api.jina.ai/v1/rerank"
    headers = {
        "Authorization": f"Bearer {os.getenv('JINA_API_KEY')}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "model": "jina-reranker-v2-base-multilingual",
        "query": query,
        "documents": documents,
        "top_n": len(documents),
        "return_documents": True,
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["results"]
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

def main():
    query = "Future of AI"
    documents = ["Jina", "Weaviate", "OpenAI", "Hugging Face", "Qdrant"]
    reranked_docs = rerank_documents(query, documents)
    print("Re-ranked documents based on the query 'Future of AI':")
    for doc in reranked_docs:
        print(f"Document: {doc['document']['text']}, Relevance Score: {doc['relevance_score']}")

if __name__ == "__main__":
    main()