import requests
import os
import json

# Initialize variables
JINA_API_KEY = os.getenv("JINA_API_KEY")
HEADERS = {"Authorization": f"Bearer {JINA_API_KEY}"}
JSON_FILE = "rag_system_data.json"

# Function to extract and save data in JSON file
def extract_save_data():
    urls = ["https://github.com/jeff-dh/SolidPython", "https://github.com/jeff-dh/SolidPython/wiki"]
    all_data = []
    
    for url in urls:
        response = requests.post("https://r.jina.ai/", headers=HEADERS, json={"url": url, "respondWith": "text"})
        if response.status_code == 200:
            data = response.json()["data"]
            all_data.append(data)
    
    with open(JSON_FILE, 'w') as file:
        json.dump(all_data, file)

# Extract and save data
extract_save_data()

def answer_question(question):
    # Load JSON data
    with open(JSON_FILE, 'r') as file:
        data = json.load(file)
    
    # Embed question
    embed_response = requests.post(
        "http://api.jina.ai/v1/embeddings",
        headers={"Authorization": f"Bearer {JINA_API_KEY}", "Content-Type": "application/json"},
        json={"model": "jina-embeddings-v3", "input": [question], "task": "retrieval.query"}
    )
    question_vector = embed_response.json()["data"][0]["embedding"]
    
    # Embed data paragraphs
    paragraphs = [para for sublist in data for para in sublist.split('\n\n')]
    embed_response = requests.post(
        "http://api.jina.ai/v1/embeddings",
        headers={"Authorization": f"Bearer {JINA_API_KEY}", "Content-Type": "application/json"},
        json={"model": "jina-embeddings-v3", "input": paragraphs, "task": "retrieval.passage"}
    )
    para_vectors = [x["embedding"] for x in embed_response.json()["data"]]
    
    # Find top 3 paragraphs
    similarities = [sum([a*b for a, b in zip(question_vector, para)]) for para in para_vectors]
    top_3_index = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[:3]
    
    # Formulating prompt for the LLM
    top_3_segments = [paragraphs[i] for i in top_3_index]
    prompt = f"Based on these segments:\n\n- {top_3_segments[0]}\n- {top_3_segments[1]}\n- {top_3_segments[2]}\n\nAnswer the question: {question}"
    
    # Querying the LLM
    llm_response = requests.post(
        "http://llm.jina.ai/v1/predict",
        headers={"Authorization": f"Bearer {JINA_API_KEY}", "Content-Type": "application/json"},
        json={"prompt": prompt, "model": "claude-3.5-sonnet"}
    )
    
    # Print LLM response
    if llm_response.status_code == 200:
        print(llm_response.json()["data"][0]["generated_text"])
    else:
        print("Error querying LLM")

# Example usage
question_prompt = input("Please ask a question related to the SolidPython project: ")
answer_question(question_prompt)