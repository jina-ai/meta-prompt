import os
import requests
import umap
import matplotlib.pyplot as plt
import numpy as np

# Load the Jina API key from environment variables
token = os.environ["JINA_API_KEY"]

# Function to fetch sentences from the Hacker News front page
def fetch_hn_sentences():
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    hn_front_page = "https://news.ycombinator.com"
    r_response = requests.get(f"https://r.jina.ai/{hn_front_page}", headers=headers)
    if r_response.status_code == 200:
        r_data = r_response.json()
        content = r_data['data']['content']
        sentences = content.split('. ')
        return [sentence.replace('\n', ' ').strip() for sentence in sentences]
    else:
        print(f"Error fetching Hacker News sentences: {r_response.json()['message']}")
        return []

# Function to generate embeddings from sentences
def get_embeddings(sentences):
    endpoint = "https://api.jina.ai/v1/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    data = {
        "model": "jina-clip-v1",
        "input": [{"text": sentence} for sentence in sentences],
    }

    embeddings_response = requests.post(endpoint, json=data, headers=headers)
    if embeddings_response.status_code == 200:
        embeddings_data = embeddings_response.json()
        embeddings = [data_point["embedding"] for data_point in embeddings_data["data"]]
        return embeddings
    else:
        print(f"Error generating embeddings: {embeddings_response.json()['message']}")
        return []

# Fetch Hacker News sentences
hn_sentences = fetch_hn_sentences()

# Get embeddings for the fetched sentences
embeddings = get_embeddings(hn_sentences)

# Convert the list of embeddings to a 2D array
embeddings_array = np.array(embeddings)

# Use UMAP to reduce the embeddings to 2 dimensions
reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, metric='correlation')
embedding_2d = reducer.fit_transform(embeddings_array)

# Visualize the 2D embeddings using Matplotlib
plt.figure(figsize=(12, 12))
plt.scatter(embedding_2d[:, 0], embedding_2d[:, 1])
for i, sentence in enumerate(hn_sentences[:len(embedding_2d)]):
    plt.text(embedding_2d[i, 0], embedding_2d[i, 1], sentence[:50] + '...', fontsize=9)

plt.show()