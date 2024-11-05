import os
import requests
import matplotlib.pyplot as plt
import umap
import numpy as np

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
JINA_API_KEY = os.getenv("JINA_API_KEY")

headers = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

def get_hn_frontpage_sentences():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    top_stories = requests.get(url).json()[:10]  # Limiting to top 10 stories for brevity
    sentences = []

    for story_id in top_stories:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story_data = requests.get(story_url).json()
        sentences.append(story_data["title"])  # Assuming we're only interested in titles
    
    return sentences

def get_embeddings(texts):
    embeddings_api_url = "https://api.jina.ai/v1/embeddings"
    data = {
        "model": "jina-clip-v1",
        "input": texts,
    }
    response = requests.post(embeddings_api_url, headers=headers, json=data).json()
    embeddings = [item["embedding"] for item in response["data"]]
    return embeddings

sentences = get_hn_frontpage_sentences()
embeddings = get_embeddings(sentences)

embeddings_np = np.array(embeddings)
reducer = umap.UMAP()
umap_emb = reducer.fit_transform(embeddings_np)

plt.figure(figsize=(12, 8))
plt.scatter(umap_emb[:, 0], umap_emb[:, 1])
for i, sentence in enumerate(sentences):
    plt.text(umap_emb[i, 0], umap_emb[i, 1], sentence[:30], fontsize=9)
plt.title("UMAP visualization of HackerNews Frontpage Sentences")
plt.show()