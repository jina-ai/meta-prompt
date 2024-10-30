import requests
import os
import matplotlib.pyplot as plt
import umap
import numpy as np

# Load the API token from environment variable
token = os.environ["JINA_API_KEY"]

# Define the endpoint and headers for the `r.reader API` to grab the frontpage of HackerNews
endpoint = "https://r.jina.ai/https://news.ycombinator.com"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

# Sending request to get the text/content from the HackerNews frontpage
response = requests.get(endpoint, headers=headers)
data = response.json()

# Extract sentences from the content, assuming data['data']['content'] contains the text
content = data['data']['content']
sentences = content.split(".")
print('sentences', sentences)

# Define the endpoint and headers for the `Embeddings API`
embedding_endpoint = "https://api.jina.ai/v1/embeddings"
embedding_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

# Prepare the data for the embeddings API
embedding_data = {
    "model": "jina-clip-v1",
    "input": [{"text": sentence.strip()} for sentence in sentences if sentence.strip() != ""]
}

# Sending request to get embeddings for each sentence
embedding_response = requests.post(embedding_endpoint, json=embedding_data, headers=embedding_headers)
embedding_data = embedding_response.json()

# Extract embeddings and prepare for UMAP reduction
embeddings = np.array([entry['embedding'] for entry in embedding_data['data']])

# Reduce dimensionality with UMAP
reducer = umap.UMAP(n_neighbors=5, min_dist=0.3, metric='correlation')
embedding_2d = reducer.fit_transform(embeddings)

# Plotting
plt.figure(figsize=(12, 12))
plt.scatter(embedding_2d[:, 0], embedding_2d[:, 1], alpha=0.5)
plt.title('2D UMAP Visualization of Sentences from HackerNews Frontpage')
plt.xlabel('UMAP Dimension 1')
plt.ylabel('UMAP Dimension 2')
plt.show()