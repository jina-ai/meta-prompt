import os
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from umap import UMAP

# Define Jina API key
jina_api_key = os.environ["JINA_API_KEY"]

# Download dataset
dataset_url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
data = pd.read_csv(dataset_url, header=None).iloc[:1000, [0, 8]]  # Selecting 1000 data points and 2 columns
texts = data[0].apply(str).tolist()  # Convert to list of texts
labels = data[8].tolist()  # Get labels for coloring

# Embedding parameters
headers = {
    "Authorization": f"Bearer {jina_api_key}",
    "Content-Type": "application/json",
}
data_2d = {
    "model": "jina-embeddings-v3",
    "input": texts,
    "task": "separation",
    "dimensions": 2,
}
data_1024d = {
    "model": "jina-embeddings-v3",
    "input": texts,
    "task": "separation",
    "dimensions": 1024,
}

# Embedding API request for 2D
response_2d = requests.post("http://api.jina.ai/v1/embeddings", headers=headers, json=data_2d).json()

# Extract embeddings and labels
embeddings_2d = [d['embedding'] for d in response_2d['data']]

# Embedding API request for 1024D
response_1024d = requests.post("http://api.jina.ai/v1/embeddings", headers=headers, json=data_1024d).json()
embeddings_1024d = [d['embedding'] for d in response_1024d['data']]

# Reduce 1024D to 2D using UMAP
umap = UMAP(n_components=2, random_state=42)
embeddings_1024d_reduced = umap.fit_transform(embeddings_1024d)

# Creating DataFrame for visualization
df_2d = pd.DataFrame(embeddings_2d, columns=['Dim1', 'Dim2'])
df_2d['Label'] = labels
df_1024d = pd.DataFrame(embeddings_1024d_reduced, columns=['Dim1', 'Dim2'])
df_1024d['Label'] = labels

# Plotting
fig, axs = plt.subplots(1, 2, figsize=(14, 7))
sns.scatterplot(data=df_2d, x='Dim1', y='Dim2', hue='Label', ax=axs[0], palette="viridis").set(title='2D Embeddings', aspect='equal')
sns.scatterplot(data=df_1024d, x='Dim1', y='Dim2', hue='Label', ax=axs[1], palette="viridis").set(title='1024D reduced to 2D Embeddings', aspect='equal')
plt.show()