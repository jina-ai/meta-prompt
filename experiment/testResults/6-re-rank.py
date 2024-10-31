import os
import requests

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
JINA_API_KEY = os.getenv("JINA_API_KEY")

# Function to call the Embeddings API
def get_embeddings(texts):
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {
        "model": "jina-embeddings-v3",
        "input": texts,
    }
    response = requests.post("https://api.jina.ai/v1/embeddings", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.json()}")
        return None

# Function to call the Reranker API
def rerank(query, documents):
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {
        "model": "jina-reranker-v2-base-multilingual",
        "query": query,
        "documents": documents,
        "top_n": len(documents),
        "return_documents": True,
    }
    response = requests.post("https://api.jina.ai/v1/rerank", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.json()}")
        return None

# Example usage
def main():
    query = "Future of AI"
    documents = ['Jina', 'Weaviate', 'OpenAI', 'Hugging Face', 'Qdrant']
    
    embeddings_results = get_embeddings(documents)
    
    if embeddings_results:
        embeddings_only = [result['embedding'] for result in embeddings_results['data']]
        reranked_results = rerank(query, embeddings_only)
        
        if reranked_results:
            print(f"Reranked documents: {reranked_results['results']}")
        else:
            print("Failed to rerank documents.")
    else:
        print("Failed to get embeddings.")

if __name__ == "__main__":
    main()