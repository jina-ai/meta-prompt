import requests
import os

# Your Jina API key, read from the environment variable
JINA_API_KEY = os.getenv("JINA_API_KEY")

def generate_embeddings(text_list, model="jina-embeddings-v3"):
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "input": text_list
    }
    
    response = requests.post("https://api.jina.ai/v1/embeddings", json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to generate embeddings", "details": response.text}

def main():
    text_numbers = [str(i) for i in range(1, 101)]
    
    embeddings_response = generate_embeddings(text_numbers)
    
    if "error" in embeddings_response:
        print(embeddings_response["error"])
    else:
        embeddings = embeddings_response.get("data", [])
        for i, embedding in enumerate(embeddings):
            print(f"Embedding {i+1}: {embedding['embedding'][:10]}...")

if __name__ == "__main__":
    main()
Remember to set the JINA_API_KEY environment variable before running the script.