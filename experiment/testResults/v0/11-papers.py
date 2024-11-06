import os
import requests
from rich.console import Console
from rich.traceback import install
from urllib.parse import urlencode

install()
console = Console()

JINA_API_KEY = os.getenv("JINA_API_KEY")
headers = {"Authorization": f"Bearer {JINA_API_KEY}"}

def search_papers(query="embeddings", count=3):
    search_url = "https://s.jina.ai/"
    params = {
        "q": query,
        "count": count,
        "respondWith": "json"
    }
    try:
        response = requests.post(search_url, headers=headers, data=urlencode(params))
        if response.status_code == 200:
            papers = response.json()["data"]
            console.log(f"Found {len(papers)} papers.")
            return [(paper["title"], paper["url"]) for paper in papers]
        else:
            console.log("Failed to search for papers", style="bold red")
    except Exception as e:
        console.log(f"Error during search: {str(e)}", style="bold red")

def scrape_paper(url):
    reader_api = "https://r.jina.ai/"
    data = {"url": url}
    try:
        response = requests.post(reader_api, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            console.log("Failed to scrape paper", style="bold red")
    except Exception as e:
        console.log(f"Error during scraping: {str(e)}", style="bold red")

def segment_text(text):
    segment_api = "https://segment.jina.ai"
    try:
        response = requests.post(segment_api, headers=headers, json={"input": [text]})
        if response.status_code == 200:
            return response.json()["chunks"]
        else:
            console.log("Failed to segment text", style="bold red")
    except Exception as e:
        console.log(f"Error during segmentation: {str(e)}", style="bold red")

def generate_embeddings(texts, task_type="retrieval.passage"):
    embeddings_url = "https://api.jina.ai/v1/embeddings"
    data = {
        "model": "jina-embeddings-v3",
        "input": texts,
        "task": task_type
    }
    try:
        response = requests.post(embeddings_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            console.log("Failed to generate embeddings", style="bold red")
    except Exception as e:
        console.log(f"Error generating embeddings: {str(e)}", style="bold red")

def main():
    query = input("Enter your search query: ")
    papers = search_papers()
    for title, url in papers:
        console.log(f"Processing paper: {title}")
        paper_text = scrape_paper(url)
        segments = segment_text(paper_text)
        embeddings = generate_embeddings(segments)
        query_embedding = generate_embeddings([query], task_type="retrieval.query")[0]["embedding"]
        matches = []
        # Assuming cosine similarity function for simplicity, though it's not directly available here
        for segment, embedding in zip(segments, embeddings):
            # This part is simplified and demonstrates the concept, actual implementation of finding matches varies
            cos_sim = cosine_similarity(query_embedding, embedding["embedding"])
            if cos_sim > 0.5:  # A threshold for matching, for the demonstration purpose
                matches.append(segment)
        console.log(f"Matches in '{title}':")
        for match in matches:
            console.log(match)

if __name__ == "__main__":
    main()