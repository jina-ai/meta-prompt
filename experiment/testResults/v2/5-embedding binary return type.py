import os
import requests

def generate_embedding(input_text, return_type="binary"):
    api_key = os.getenv("JINA_API_KEY")
    url = "https://api.jina.ai/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "jina-embeddings-v3",
        "input": [input_text],
        "embedding_type": return_type
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)

# Example of usage
embedding = generate_embedding("Jina", "binary")
print(embedding)