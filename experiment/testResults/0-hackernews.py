import os
import requests
import umap
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
JINA_API_KEY = os.getenv('JINA_API_KEY')

def fetch_frontpage_sentences():
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    response = requests.post('https://s.jina.ai/',
                             headers=headers,
                             json={"q": "site:ycombinator.com Hacker News", "options": "Text"})
    if response.status_code == 200:
        articles = response.json().get('data', [])
        sentences = []
        for article in articles:
            content = article.get('content', '')
            sentences.extend(content.split('. '))
        return sentences
    else:
        return []

def generate_embeddings(sentences):
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {
        "model": "jina-embeddings-v3",
        "input": sentences,
    }
    response = requests.post('https://api.jina.ai/v1/embeddings', headers=headers, json=data)
    if response.status_code == 200:
        embeddings = [item['embedding'] for item in response.json()['data']]
        return embeddings
    else:
        return []

def visualize_embeddings(sentences, embeddings):
    reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, metric='cosine')
    embedding_data = reducer.fit_transform(embeddings)

    plt.figure(figsize=(15,10))
    plt.scatter(embedding_data[:, 0], embedding_data[:, 1])
    for i, sentence in enumerate(sentences):
        plt.text(embedding_data[i, 0], embedding_data[i, 1], sentence, fontsize=9)
    plt.title("2D UMAP Visualization of Hacker News Frontpage Sentences")
    plt.show()

def main():
    sentences = fetch_frontpage_sentences()
    if not sentences:
        print("Failed to fetch sentences.")
        return
    embeddings = generate_embeddings(sentences)
    if not embeddings:
        print("Failed to generate embeddings.")
        return
    visualize_embeddings(sentences, embeddings)

if __name__ == "__main__":
    main()