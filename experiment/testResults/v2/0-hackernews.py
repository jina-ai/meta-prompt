import os
import requests
import numpy as np
import umap
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

# Load API Key from environment
JINA_API_KEY = os.getenv("JINA_API_KEY")
if JINA_API_KEY is None:
    raise EnvironmentError("Please set the environment variable 'JINA_API_KEY' with your API key.")

headers = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Content-Type": "application/json",
}

def get_hackernews_headlines():
    """Fetch headlines from HackerNews frontpage."""
    response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    if response.status_code != 200:
        raise ConnectionError("Failed to fetch top stories from HackerNews.")
    top_stories_ids = response.json()[:10]  # Get top 10 stories for simplicity
    headlines = []
    for story_id in top_stories_ids:
        story_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
        if story_response.status_code == 200:
            story_data = story_response.json()
            headlines.append(story_data.get("title", "No Title Found"))
    return headlines

def get_embeddings(texts):
    """Retrieve embeddings for a list of texts using Jina AI Search Foundation API."""
    data = {
        "model": "jina-embeddings-v3",
        "input": texts,
    }
    response = requests.post("https://api.jina.ai/v1/embeddings", headers=headers, json=data)
    if response.status_code == 200:
        return [embedding["embedding"] for embedding in response.json()["data"]]
    else:
        raise ConnectionError("Failed to fetch embeddings.")

def visualize_embeddings(embeddings, labels):
    """Visualize 2D projections of embeddings using UMAP."""
    reducer = umap.UMAP()
    embeddings_np = np.array(embeddings)
    embedding_2d = reducer.fit_transform(embeddings_np)
    
    plt.figure(figsize=(12, 8))
    for i, label in enumerate(labels):
        plt.scatter(embedding_2d[i, 0], embedding_2d[i, 1])
        plt.text(embedding_2d[i, 0], embedding_2d[i, 1], label, fontsize=9)
    plt.title("2D UMAP Projection of HackerNews Headlines")
    plt.show()

def main():
    try:
        headlines = get_hackernews_headlines()
        embeddings = get_embeddings(headlines)
        visualize_embeddings(embeddings, headlines)
    except Exception as e:
        print(f"An error occurred: {e}")

main()