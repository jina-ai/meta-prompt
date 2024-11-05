import os
import requests

# Read environment variable for API key
JINA_API_KEY = os.getenv('JINA_API_KEY')

# Headers for authentication
headers = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

def read_bbc_content(url):
    """
    Reads the content of a BBC article URL using Jina AI's Reader API
    """
    reader_api_url = "https://r.jina.ai/"
    payload = {
        "url": url,
        "options": "Default"
    }
    
    try:
        response = requests.post(reader_api_url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("content", "")
    except requests.RequestException as e:
        print(f"Error fetching URL content: {e}")
        return ""

def check_statement_validity(statement, content):
    """
    Checks if a given statement is valid within the provided content using Jina AI's Embeddings API
    """
    embeddings_api_url = "https://api.jina.ai/v1/embeddings"
    payload = {
        "model": "jina-embeddings-v3",
        "input": [statement, content],
        "embedding_type": "float",
        "task": "text-matching"
    }
    
    try:
        response = requests.post(embeddings_api_url, headers=headers, json=payload)
        response.raise_for_status()
        embeddings = response.json().get("data", [])
        # Here a more sophisticated similarity check could be performed
        # For simplicity, we just outline hypothetical embedding comparison.
        print("Embeddings obtained. Compare embeddings for validation.")
    except requests.RequestException as e:
        print(f"Error generating embeddings: {e}")

def main():
    bbc_url = "https://www.bbc.com/news/technology"
    statement = "The UK government has announced a new law that will require social media companies to verify the age of their users."
    
    # Step 1: Read content from BBC URL
    content = read_bbc_content(bbc_url)
    if content:
        print("Content fetched. Checking statement...")
        # Step 2: Verify the statement using embeddings
        check_statement_validity(statement, content)
    else:
        print("Failed to fetch content.")

# Run the main function
if __name__ == "__main__":
    main()