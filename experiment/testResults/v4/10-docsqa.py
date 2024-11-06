import json
import requests
import os

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
JINA_API_KEY = os.getenv("JINA_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def read(url):
    try:
        response = requests.post(
            "https://r.jina.ai/",
            headers=HEADERS,
            json={"url": url}
        )
        response.raise_for_status()
        data = response.json()
        return data["data"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the content: {e}")
        return None

def segment(content):
    try:
        response = requests.post(
            "https://segment.jina.ai/",
            headers=HEADERS,
            json={"content": content, "return_chunks": True}
        )
        response.raise_for_status()
        data = response.json()
        return data["chunks"]
    except requests.exceptions.RequestException as e:
        print(f"Error segmenting the content: {e}")
        return None

def rerank(query, documents):
    try:
        response = requests.post(
            "https://api.jina.ai/v1/rerank",
            headers=HEADERS,
            json={"model": "jina-reranker-v2-base-multilingual", "query": query, "documents": documents}
        )
        response.raise_for_status()
        data = response.json()
        return data["results"]
    except requests.exceptions.RequestException as e:
        print(f"Error reranking the documents: {e}")
        return None

def main():
    # Reading web content
    content_solidpython = read("https://github.com/jeff-dh/SolidPython")
    content_wiki = read("https://github.com/jeff-dh/SolidPython/wiki")
    
    # this is a placeholder for actual scraping and indexing process which we can't perform here directly
    index_content = ["Sample index content 1 from SolidPython repo", "Sample index content 2 from SolidPython wiki"]
    
    # Assuming content is segmented and indexed, now prompting user for a question
    question = input("What would you like to know about SolidPython? ")
    
    # For simplicity, instead of matching question with indexed segments,
    # I'll just simulate finding top 3 segments from index
    top_segments = segment("\n\n".join(index_content))[:3]  # Simulate top 3 segments
    
    # Now assuming we have top 3 segments, let's use rerank to find the most relevant
    # In a real scenario, you'll match these against the question or pass directly to LLM
    # Here, reranking is more for demonstration
    reranked_segments = rerank(question, top_segments)
    
    # Constructing the prompt for LLM (Large Language Model)
    llm_prompt = f"Based on these segments:\n\n- {reranked_segments[0]['document']['text']}\n- {reranked_segments[1]['document']['text']}\n- {reranked_segments[2]['document']['text']}\n\nAnswer the question: {question}"
    
    # Normally we would now call an LLM API with this prompt to generate an answer,
    # but since we don't have an actual LLM endpoint, we'll print the prompt for now
    print("\nPrompt for LLM:\n")
    print(llm_prompt)


if __name__ == "__main__":
    main()