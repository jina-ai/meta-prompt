import os
import requests
import json

JINA_API_KEY = os.getenv("JINA_API_KEY")

def embed_texts(texts, model="jina-embeddings-v3"):
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "input": texts
    }
    try:
        response = requests.post("https://api.jina.ai/v1/embeddings", headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return {"error": "Failed to get embeddings", "status_code": response.status_code}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def main():
    texts_to_embed = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    embeddings = embed_texts(texts_to_embed)
    
    if "error" in embeddings:
        print(embeddings["error"])
    else:
        print(embeddings)

if __name__ == "__main__":
    main()