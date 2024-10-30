import requests
import numpy as np
from bs4 import BeautifulSoup
import umap
import matplotlib.pyplot as plt


# Function to fetch HackerNews headlines
def fetch_hn_headlines():
    url = "https://news.ycombinator.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = []

    # Find all titleline classes which contain the headlines
    for item in soup.find_all('span', class_='titleline'):
        headline = item.get_text().strip()
        headlines.append(headline)

    return headlines


# Function to get embeddings from Jina
def get_embeddings(texts):
    endpoint = "https://api.jina.ai/v1/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer jina_ad42b3eb889c44db9f2190ec851c68c9o5LJmW9Glf5wP-V3JOweluX9WAE2"
    }
    data = {
        "model": "jina-embeddings-v3",
        "input": texts
    }

    response = requests.post(endpoint, headers=headers, json=data)
    return np.array([item['embedding'] for item in response.json()['data']])


# Main visualization function
def visualize_headlines():
    # Fetch headlines
    headlines = fetch_hn_headlines()
    print(f"Fetched {len(headlines)} headlines")

    # Get embeddings
    embeddings = get_embeddings(headlines)

    # Reduce dimensionality with UMAP
    reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42)
    embedding_2d = reducer.fit_transform(embeddings)

    # Create the visualization
    plt.figure(figsize=(15, 10))
    plt.scatter(embedding_2d[:, 0], embedding_2d[:, 1], alpha=0.6)

    # Add labels for each point
    for i, headline in enumerate(headlines):
        plt.annotate(headline[:50] + '...' if len(headline) > 50 else headline,
                     (embedding_2d[i, 0], embedding_2d[i, 1]),
                     fontsize=8,
                     alpha=0.7,
                     bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    plt.title("HackerNews Headlines Visualization\nSimilar headlines are closer together",
              fontsize=14, pad=20)
    plt.xlabel("UMAP Dimension 1")
    plt.ylabel("UMAP Dimension 2")

    # Adjust layout to prevent text overlap
    plt.tight_layout()
    return plt


# Execute the visualization
plt.style.use('seaborn')
visualization = visualize_headlines()
visualization.show()