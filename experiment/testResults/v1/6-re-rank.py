import os
import requests
import json

# Get the JINA_API_KEY from environment variable
JINA_API_KEY = os.environ.get("JINA_API_KEY")

# Function to call the Embeddings API and get embeddings for the input texts
def get_embeddings(texts):
    headers = {
        'Authorization': f'Bearer {JINA_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "jina-embeddings-v3",
        "input": texts,
    }
    response = requests.post('https://api.jina.ai/v1/embeddings', headers=headers, data=json.dumps(data))
    try:
        embeddings = response.json()
        return embeddings['data']
    except Exception as e:
        print(f"Error getting embeddings: {str(e)}")
        return None

# Function to call the Reranker API to rerank a list of documents based on a query
def rerank_documents(query, documents):
    headers = {
        'Authorization': f'Bearer {JINA_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "jina-reranker-v2-base-multilingual",
        "query": query,
        "documents": documents,
    }
    response = requests.post('https://api.jina.ai/v1/rerank', headers=headers, data=json.dumps(data))
    try:
        reranked_docs = response.json()
        return reranked_docs['results']
    except Exception as e:
        print(f"Error reranking documents: {str(e)}")
        return None

# Main function to execute the re-ranking for the provided query and documents
def main():
    query = "Future of AI"
    documents = ["Jina", "Weaviate", "OpenAI", "Hugging Face", "Qdrant"]
    embeddings = get_embeddings([query] + documents)
    if embeddings:
        # Assuming we are re-ranking based on the similarity of their embeddings,
        # a simple workaround since direct reranking by embeddings is not shown
        query_embedding = embeddings[0]['embedding_vector']
        document_embeddings = embeddings[1:]
        document_scores = []
        for idx, doc_emb in enumerate(document_embeddings):
            # Just a placeholder for actual similarity calculation which is not detailed here
            similarity_score = sum([q * d for q, d in zip(query_embedding, doc_emb['embedding_vector'])])
            document_scores.append((documents[idx], similarity_score))
        
        sorted_docs = sorted(document_scores, key=lambda x: x[1], reverse=True)
        print(f"Documents ranked by future relevance to AI: {sorted_docs}")
    else:
        print("Could not retrieve embeddings to rerank documents.")

if __name__ == "__main__":
    main()