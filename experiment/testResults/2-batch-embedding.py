import os
import requests

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
JINA_API_KEY = os.getenv('JINA_API_KEY')
headers = {
    'Authorization': f'Bearer {JINA_API_KEY}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

def generate_embeddings(input_texts):
    url = 'https://api.jina.ai/v1/embeddings'
    data = {
        'model': 'jina-embeddings-v3',
        'input': input_texts,
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Error in generate_embeddings: {response.json()}")
        return None

def main():
    input_texts = [str(i) for i in range(1, 101)]
    embeddings = generate_embeddings(input_texts)
    if embeddings:
        for i, embedding in enumerate(embeddings, 1):
            print(f"Embedding for {i}: {embedding['embedding'][:10]}...")  # Showing first 10 characters of each embedding for brevity

if __name__ == "__main__":
    main()