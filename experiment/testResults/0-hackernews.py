import requests
import numpy as np
import matplotlib.pyplot as plt
import os
from umap import UMAP

token = os.environ["JINA_API_KEY"]

# Retrieve hackernews frontpage articles using Jina's s.reader API
s_reader_endpoint = "https://s.jina.ai/https://news.ycombinator.com/"
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {token}"
}

s_reader_response = requests.get(s_reader_endpoint, headers=headers)
articles_data = s_reader_response.json()

sentences = []
for article in articles_data['data']:
    content = article['content'].split('.')
    sentences.extend(content)

# Generate embeddings for each sentence using Jina's embedding API
embedding_endpoint = "https://api.jina.ai/v1/embeddings"
embedding_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

embedding_data = {
    "model": "jina-clip-v1",
    "input": [{"text": sentence} for sentence in sentences if sentence.strip() != ""]
}

embedding_response = requests.post(embedding_endpoint, json=embedding_data, headers=embedding_headers)
embedding_results = embedding_response.json()

# Collect embeddings
embeddings = np.array([result['embedding'] for result in embedding_results['data']])

# Reduce embeddings dimensions for visualization
umap_reducer = UMAP(n_neighbors=5, min_dist=0.3, metric='correlation')
umap_embeddings = umap_reducer.fit_transform(embeddings)

# Plotting
plt.figure(figsize=(12, 8))
plt.scatter(umap_embeddings[:, 0], umap_embeddings[:, 1], alpha=0.5)
plt.title('UMAP visualization of sentences from HackerNews frontpage')
plt.show()