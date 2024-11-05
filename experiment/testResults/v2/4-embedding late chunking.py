import requests
import os

def generate_embeddings(input_text, late_chunking=True):
    # Read the API key from the environment variable
    api_key = os.getenv("JINA_API_KEY")
    if not api_key:
        raise ValueError("JINA_API_KEY environment variable is not set.")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "jina-embeddings-v3",
        "input": [input_text],
        "late_chunking": late_chunking
    }
    
    try:
        response = requests.post("https://api.jina.ai/v1/embeddings", json=payload, headers=headers)
        response.raise_for_status()
        embedding = response.json()["data"][0]["embedding"]
        return embedding
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        
# Example usage
if __name__ == "__main__":
    try:
        input_text = "Jina"
        embedding = generate_embeddings(input_text)
        print("Generated Embedding:", embedding)
    except Exception as e:
        print(e)