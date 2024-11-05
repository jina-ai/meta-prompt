import os
import requests
import numpy as np
import umap
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Authentication token from environment variable
JINA_API_KEY = os.getenv("JINA_API_KEY")

# Set headers for authentication and content type
headers = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "application/json",
}

# Fetch sentences from HackerNews frontpage using s.reader API
search_endpoint = "https://s.jina.ai"
search_params = {
    "q": "site:ycombinator.com HN frontpage",
}
search_response = requests.get(search_endpoint, headers=headers, params=search_params)
search_data = search_response.json()

# Extract sentences from search results
sentences = []
for item in search_data.get("data", []):
    content = item.get("content", "")
    if content:
        sentences += [sentence for sentence in content.split('.') if sentence]

# Ensure sentences list isn't empty
if not sentences:
    raise ValueError("No sentences extracted from HN frontpage.")

# Generate embeddings using Jina Embeddings API
embeddings_endpoint = "https://api.jina.ai/v1/embeddings"
embeddings_data = {
    "model": "jina-clip-v1",
    "input": [{"text": sentence} for sentence in sentences],
}

embeddings_response = requests.post(embeddings_endpoint, json=embeddings_data, headers=headers)
embeddings_data = embeddings_response.json()

# Extract embeddings vectors
embeddings = [item["embedding"] for item in embeddings_data.get("data", []) if "embedding" in item]

# Check for empty embeddings
if not embeddings:
    raise ValueError("No embeddings generated.")

# Standardize the embeddings
scaler = StandardScaler()
scaled_embeddings = scaler.fit_transform(embeddings)

# Dimensionality Reduction with UMAP
reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, metric='euclidean')
embedding_2d = reducer.fit_transform(scaled_embeddings)

# Plot the 2D UMAP visualization
plt.scatter(embedding_2d[:, 0], embedding_2d[:, 1])
plt.gca().set_aspect('equal', 'datalim')
plt.title('UMAP projection of the HackerNews frontpage sentences', fontsize=12)
plt.show()