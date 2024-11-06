import os
import requests
import json

JINA_API_KEY = os.getenv('JINA_API_KEY')

def embed(texts):
    try:
        headers = {
            'Authorization': f'Bearer {JINA_API_KEY}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        data = {
            'model': 'jina-embeddings-v3',
            'input': texts
        }
        response = requests.post('https://api.jina.ai/v1/embeddings', headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'An error occurred: {e}')

def rerank(query, documents):
    try:
        headers = {
            'Authorization': f'Bearer {JINA_API_KEY}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        data = {
            'model': 'jina-reranker-v2-base-multilingual',
            'query': query,
            'documents': documents
        }
        response = requests.post('https://api.jina.ai/v1/rerank', headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'An error occurred: {e}')

def classify(images, labels):
    try:
        headers = {
            'Authorization': f'Bearer {JINA_API_KEY}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        data = {
            'model': 'jina-clip-v1',
            'input': [{'image': image} for image in images],
            'labels': labels
        }
        response = requests.post('https://api.jina.ai/v1/classify', headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'An error occurred: {e}')

def read(url):
    try:
        headers = {
            'Authorization': f'Bearer {JINA_API_KEY}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-No-Cache': 'true'
        }
        data = {
            'url': url,
            'options': 'Default'
        }
        response = requests.post('https://r.jina.ai/', headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'An error occurred: {e}')

def main():
    # Example usage of embed API
    texts = ["Hello, world!", "How can I use Jina AI's APIs?"]
    embeddings_response = embed(texts)
    print(embeddings_response)
    
    # Example usage of classify API
    images = ['base64_image_string']
    labels = ['positive', 'negative']
    classification_response = classify(images, labels)
    print(classification_response)
    
    # Example usage of read API
    page_content = read('https://github.com/jeff-dh/SolidPython')
    print(page_content)

if __name__ == "__main__":
    main()