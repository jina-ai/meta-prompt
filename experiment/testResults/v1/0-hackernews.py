import os
import requests
import matplotlib.pyplot as plt
import umap
import numpy as np
from dotenv import load_dotenv

load_dotenv()
JINA_API_KEY = os.getenv('JINA_API_KEY')

def get_hackernews_headlines():
    response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
    top_stories_ids = response.json()
    headlines = []
    for story_id in top_stories_ids[:30]:  # Limit to top 30 stories for brevity
        story_response = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty')
        story_data = story_response.json()
        headlines.append(story_data['title'])
    return headlines

def embed_texts(texts):
    headers = {
        'Authorization': f'Bearer {JINA_API_KEY}',
    }
    data = {
        'model': 'jina-embeddings-v3',
        'input': texts,
    }
    response = requests.post('https://api.jina.ai/v1/embeddings', headers=headers, json=data)
    embeddings = response.json()
    return [item['embedding_vector'] for item in embeddings['data']]

def visualize_embeddings(embeddings):
    reducer = umap.UMAP()
    embedding_coords = reducer.fit_transform(embeddings)
    
    plt.figure(figsize=(10, 10))
    plt.scatter(embedding_coords[:, 0], embedding_coords[:, 1])
    plt.title('UMAP visualization of HackerNews Headlines')
    plt.show()

def main():
    headlines = get_hackernews_headlines()
    embeddings = embed_texts(headlines)
    # Convert embeddings from strings to np.arrays
    embeddings_np = np.array([np.fromstring(embedding, sep=',') for embedding in embeddings])
    visualize_embeddings(embeddings_np)

if __name__ == '__main__':
    main()