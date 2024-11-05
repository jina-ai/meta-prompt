import os
import requests
import json

# Reading the Jina API key from environment variable
JINA_API_KEY = os.environ.get("JINA_API_KEY")

# Function to generate embeddings for text inputs
def generate_embeddings(model: str, inputs: list, embedding_type="float"):
    url = "https://api.jina.ai/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "input": inputs,
        "embedding_type": embedding_type
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()  # If successful, return the JSON response
        else:
            return {"error": "Failed to generate embeddings", "status_code": response.status_code}
    except Exception as e:
        return {"error": str(e)}

# Main function to process list of numbers
def main():
    numbers_text = [str(i) for i in range(1, 101)]  # Converting numbers 1 to 100 into text
    model = "jina-embeddings-v3"  # Using the model jina-embeddings-v3 for embeddings
    embeddings_response = generate_embeddings(model, numbers_text)
    
    if "error" not in embeddings_response:
        print("Embeddings generated successfully.")
        # Do something with embeddings_response, like saving or further processing
        print(embeddings_response)  # For demonstration, printing the response
    else:
        print("Error:", embeddings_response.get("error"), "Status Code:", embeddings_response.get("status_code"))

# Execute the main function
if __name__ == "__main__":
    main()