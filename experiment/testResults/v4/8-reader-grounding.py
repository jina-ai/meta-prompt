import os
import requests
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import umap

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
jina_api_key = os.getenv("JINA_API_KEY")
headers = {
    "Authorization": f"Bearer {jina_api_key}",
    "Accept": "application/json",
}

def fetch_embedding(data, output_dim=None):
    """Fetch embeddings for the given data."""
    body = {
        "model": "jina-embeddings-v3",
        "input": data,
        "task": "separation",
    }
    if output_dim is not None:
        body["dimensions"] = output_dim
    response = requests.post("https://api.jina.ai/v1/embeddings", headers=headers, json=body)
    if response.status_code == 200:
        return np.array([res["embedding"] for res in response.json()["data"]])
    else:
        raise Exception(f"Failed to fetch embeddings: {response.json()}")

def generate_plot(data, labels, title):
    """Generate and save a plot."""
    plt.figure()
    classes = list(set(labels))
    for _class in classes:
        idxs = [i for i, l in enumerate(labels) if l == _class]
        plt.scatter(data[idxs, 0], data[idxs, 1], label=f"Class {_class}")

    plt.title(title)
    plt.legend()
    plt.axis('square')
    plt.show()

# Dummy data and labels
data = ["text1"] * 500 + ["text2"] * 500
labels = [0] * 500 + [1] * 500

# Fetching embeddings with output_dim=2
embeddings_dim2 = fetch_embedding(data, output_dim=2)
generate_plot(embeddings_dim2, labels, "Embeddings with output_dim=2")

# Fetching embeddings without specifying output_dim (default)
embeddings_high_dim = fetch_embedding(data)

# Reducing dimensionality to 2D using UMAP
reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, metric='euclidean')
umap_embeds = reducer.fit_transform(embeddings_high_dim)

# Generating UMAP reduced plot
generate_plot(umap_embeds, labels, "UMAP reduced embeddings")

# Note: Actual implementation would require real dataset instead of dummy data/labels.