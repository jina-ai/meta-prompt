```python
import requests
import os
import umap
import matplotlib.pyplot as plt
import numpy as np

# Set up authentication
JINA_API_KEY = os.getenv("JINA_API_KEY")
headers = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "application/json"
}

# Select a dataset
# For demonstration, let's assume we're working with a synthetic dataset provided below:
data_points = [
    {"text": "positive example 1", "label": "positive"},
    {"text": "positive example 2", "label": "positive"},
    {"text": "negative example 1", "label": "negative"},
    {"text": "negative example 2", "label": "negative"},
    # Assume we have about 1k of such examples evenly split between the two classes
]

# Prepare inputs for embedding
texts = [dp["text"] for dp in data_points]
labels = np.array([0 if dp["label"] == "negative" else 1 for dp in data_points])

# Request embeddings with output_dim=2
embedding_data_2d = {
    "model": "jina-clip-v1",
    "input": [{"text": text} for text in texts],
    "output_dim": 2
}

resp_2d = requests.post("https://api.jina.ai/v1/embeddings", json=embedding_data_2d, headers=headers)
embeddings_2d = np.array([point["embedding"] for point in resp_2d.json()["data"]])

# Request embeddings with output_dim=1024
embedding_data_1024d = {
    "model": "jina-clip-v1",
    "input": [{"text": text} for text in texts],
    "output_dim": 1024
}

resp_1024d = requests.post("https://api.jina.ai/v1/embeddings", json=embedding_data_1024d, headers=headers)
embeddings_1024d = np.array([point["embedding"] for point in resp_1024d.json()["data"]])

# Reduce 1024d embeddings to 2D using UMAP
reducer = umap.UMAP(n_neighbors=15, n_components=2, metric='cosine')
embeddings_2d_umap = reducer.fit_transform(embeddings_1024d)

# Visualization: Scatter plot
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Plot for 2D embeddings
axes[0].scatter(embeddings_2d[labels==0, 0], embeddings_2d[labels==0, 1], color='red', label='Negative')
axes[0].scatter(embeddings_2d[labels==1, 0], embeddings_2d[labels==1, 1], color='blue', label='Positive')
axes[0].set_title('Original 2D Embeddings')
axes[0].legend()
axes[0].set_aspect('equal', 'box')

# Plot for 2D reduced UMAP embeddings
axes[1].scatter(embeddings_2d_umap[labels==0, 0], embeddings_2d_umap[labels==0, 1], color='red', label='Negative')
axes[1].scatter(embeddings_2d_umap[labels==1, 0], embeddings_2d_umap[labels==1, 1], color='blue', label='Positive')
axes[1].set_title('UMAP 2D Embeddings from 1024D')
axes[1].legend()
axes[1].set_aspect('equal', 'box')

plt.show()
```