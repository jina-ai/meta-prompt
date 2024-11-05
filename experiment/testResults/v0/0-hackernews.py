import os
import requests
import numpy as np
import matplotlib.pyplot as plt
import umap

# Environment variable for API key
API_KEY = os.getenv("JINA_API_KEY")

# Fetching data from HACKERNEWS
response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty")
top_stories_ids = response.json()[:10]  # Getting top 10 stories for example
titles = []

for story_id in top_stories_ids:
    story_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty")
    story_data = story_response.json()
    titles.append(story_data["title"])

# Preparing for embedding
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}
data = {
    "model": "jina-embeddings-v3",
    "input": titles,
    "embedding_type": "float",
}

# Getting embeddings
embed_response = requests.post("http://api.jina.ai/v1/embeddings", headers=headers, json=data)
embeddings = np.array([item["embedding"] for item in embed_response.json()["data"]])

# Reduction with UMAP
reducer = umap.UMAP(n_neighbors=5, min_dist=0.3, metric='correlation')
embedding_2d = reducer.fit_transform(embeddings)

# Plotting
plt.figure(figsize=(12, 8))
plt.scatter(embedding_2d[:, 0], embedding_2d[:, 1])
for i, title in enumerate(titles):
    plt.text(embedding_2d[i, 0], embedding_2d[i, 1], title, fontsize=9)
plt.title("UMAP projection of HackerNews Titles")
plt.show()