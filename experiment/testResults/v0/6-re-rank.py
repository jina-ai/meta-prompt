import os
import requests

# Read the API key from environment variable
jina_api_key = os.environ.get("JINA_API_KEY")

# Input data for the Embedding API
embedding_input = {
    "model": "jina-embeddings-v3",
    "input": ["Future of AI"],
    "task": "retrieval.query",
}

# Embedding API request
embedding_response = requests.post(
    "http://api.jina.ai/v1/embeddings",
    headers={"Authorization": f"Bearer {jina_api_key}", "Content-Type": "application/json"},
    json=embedding_input
)

# Check if embedding request was successful
if embedding_response.status_code == 200:
    embedding_data = embedding_response.json()
    # Assuming we get a vector for our query "Future of AI"
    query_vector = embedding_data["data"][0]["embedding"]

    # Input data for the Reranker API with documents representing each of the keywords
    reranker_input = {
        "model": "jina-reranker-v2-base-multilingual",
        "query": query_vector,
        "documents": ["Jina", "Weaviate", "OpenAI", "Hugging Face", "Qdrant"],
    }

    # Reranker API request
    reranker_response = requests.post(
        "http://api.jina.ai/v1/rerank",
        headers={"Authorization": f"Bearer {jina_api_key}", "Content-Type": "application/json"},
        json=reranker_input
    )

    # Process reranker response
    if reranker_response.status_code == 200:
        reranked_data = reranker_response.json()
        reranked_results = reranked_data["results"]
        # Print reranked documents
        for result in reranked_results:
            print(result["document"]["text"])
    else:
        print("Error in reranking API request")
else:
    print("Error in embedding API request")