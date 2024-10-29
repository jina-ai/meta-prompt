import os
import requests
import matplotlib.pyplot as plt
import umap
import numpy as np

# Jina API key from environment variables
JINA_API_KEY = os.getenv('JINA_API_KEY')

# Endpoint for embeddings
embedding_endpoint = "https://api.jina.ai/v1/embeddings"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {JINA_API_KEY}"
}

# Grab sentences from HackerNews frontpage using r.reader from Jina
reader_endpoint = "https://r.jina.ai/https://news.ycombinator.com"
reader_response = requests.get(reader_endpoint, headers=headers)
sentences = reader_response.json()['content']['markdown_content'].split('\n')

# Filter out only sentences (simple approach, refine as needed)
sentences = [s for s in sentences if len(s.split()) > 3]

# Prepare data for embedding request
data = {
    "model": "jina-embeddings-v3",
    "input": sentences
}

# Request embeddings
response = requests.post(embedding_endpoint, json=data, headers=headers)
embeddings = np.array([item['embedding'] for item in response.json()['data']])

# Reduce embeddings to 2D using UMAP
reducer = umap.UMAP()
embedding_2d = reducer.fit_transform(embeddings)

# Visualize with matplotlib
plt.figure(figsize=(12,8))
plt.scatter(embedding_2d[:, 0], embedding_2d[:, 1])
plt.title('HackerNews Sentences Visualized in 2D with UMAP')
plt.xlabel('UMAP Dimension 1')
plt.ylabel('UMAP Dimension 2')
plt.show()