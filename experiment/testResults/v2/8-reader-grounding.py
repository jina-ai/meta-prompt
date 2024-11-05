import os
import requests
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from umap import UMAP

# Set API key
JINA_API_KEY = os.environ.get("JINA_API_KEY")
headers = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Content-Type": "application/json",
}

# Generate synthetic dataset
X, y = make_classification(n_samples=1000, n_features=20, n_informative=2, n_redundant=10, n_clusters_per_class=1, n_classes=2)

# Convert data to DataFrame for easier manipulation
df = pd.DataFrame(X)
df['label'] = y

# Prepare data for embedding
data_points = df.iloc[:, :-1].values.tolist()
data_labels = df['label'].values

# Embedding Function
def embed_data(data_points, dimensions=2, task='separation'):
    embeddings_url = "https://api.jina.ai/v1/embeddings"
    payload = {
        "model": "jina-embeddings-v3",
        "input": data_points,
        "task": task,
        "dimensions": dimensions,
    }
    response = requests.post(embeddings_url, headers=headers, json=payload)
    if response.status_code == 200:
        embeddings = response.json()['data']
        return [embedding['embedding'] for embedding in embeddings]
    else:
        print(f"Error occurred: {response.text}")
        return None

# Embed with 2 dimensions
embeddings_2d = embed_data(data_points, dimensions=2)
if embeddings_2d:
    df_2d = pd.DataFrame(embeddings_2d, columns=['x', 'y'])

# Embed with 1024 dimensions
embeddings_1024d = embed_data(data_points, dimensions=1024)
if embeddings_1024d:
    # Perform UMAP reduction to 2 dimensions
    reducer = UMAP(n_components=2)
    embeddings_umap = reducer.fit_transform(np.array(embeddings_1024d))
    df_1024d_umap = pd.DataFrame(embeddings_umap, columns=['x', 'y'])

# Create scatter plot
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Plot for 2D embeddings
axs[0].scatter(df_2d['x'], df_2d['y'], c=data_labels, cmap='coolwarm', alpha=0.6)
axs[0].set_title('2D Embeddings')
axs[0].set_aspect('equal', 'box')

# Plot for UMAP reduced embeddings
axs[1].scatter(df_1024d_umap['x'], df_1024d_umap['y'], c=data_labels, cmap='coolwarm', alpha=0.6)
axs[1].set_title('UMAP reduced 1024D Embeddings')
axs[1].set_aspect('equal', 'box')

plt.show()