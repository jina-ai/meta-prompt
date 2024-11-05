import os
import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.manifold import TSNE
import umap.umap_ as umap

# Set API key
JINA_API_KEY = os.getenv("JINA_API_KEY")
headers = {"Authorization": f"Bearer {JINA_API_KEY}"}

# Generate synthetic data
X, y = make_classification(n_samples=1000, n_features=20, n_informative=2, n_redundant=10, n_clusters_per_class=1, n_classes=2)

# Convert to list for API
data = X.tolist()

# Embedding function
def get_embeddings(data, output_dim):
    response = requests.post("https://api.jina.ai/v1/embeddings",
                             json={"model": "jina-embeddings-v3", "input": data, "task": "separation",
                                   "dimensions": output_dim},
                             headers=headers)
    if response.status_code == 200:
        return [datum['embedding_vector'] for datum in response.json()['data']]
    else:
        raise ValueError("Failed to get embeddings")

# Function to plot embeddings
def plot_embeddings(embeddings, labels, title, ax):
    df = pd.DataFrame(data=embeddings)
    df['label'] = labels
    colors = {0: 'red', 1: 'blue'}
    df.plot.scatter(x=0, y=1, c=df['label'].map(colors), ax=ax, title=title, xlabel='Dimension 1', ylabel='Dimension 2', xlim=(-10,10), ylim=(-10,10))

# Get embeddings with 2 dimensions
embeddings_2d = get_embeddings(data, 2)

# UMAP reduction to 2 dimensions from 1024 dimensions embedding
embeddings_1024d = get_embeddings(data, 1024)
reducer = umap.UMAP(n_components=2)
umap_embeddings = reducer.fit_transform(np.array(embeddings_1024d))

# Plotting
fig, axs = plt.subplots(1, 2, figsize=(14, 7))
plot_embeddings(embeddings_2d, y, '2D Embeddings', axs[0])
plot_embeddings(umap_embeddings, y, 'UMAP reduced 1024D to 2D Embeddings', axs[1])

plt.show()