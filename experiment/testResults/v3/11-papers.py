```python
import os
import requests
from rich.console import Console
from rich.traceback import install
from rich.logging import RichHandler
import logging

# Setup rich logging and traceback
install()
console = Console()
logging.basicConfig(level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger("rich")

JINA_API_KEY = os.getenv("JINA_API_KEY")

def get_latest_papers(search_term):
    """
    Search arxiv.org for the 3 latest papers with the provided search term.
    """
    endpoint = f"https://api.jina.ai/v1/search?q={search_term}&size=3"
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        papers = response.json().get("data", [])
        logger.info("Found the following papers:")
        for paper in papers:
            logger.info(paper["title"])
        return papers
    except requests.RequestException as e:
        logger.error(f"An error occurred: {e}")
        return []

def scrape_papers(papers):
    """
    Scrape each paper's PDF and store the text and title using Jina's Reader API.
    """
    texts = []
    for paper in papers:
        endpoint = f"https://r.jina.ai/{paper['url']}"
        headers = {
            "Authorization": f"Bearer {JINA_API_KEY}",
            "Accept": "application/json"
        }
        
        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            data = response.json().get("data", {})
            texts.append({"title": paper["title"], "text": data.get("content", "")})
            logger.info(f"Scraped text for paper: {paper['title']}")
        except requests.RequestException as e:
            logger.error(f"An error occurred while scraping {paper['title']}: {e}")
    
    return texts

def segment_texts(texts):
    """
    Break the texts into segments using Jina's Segmenter API.
    """
    endpoint = "https://segment.jina.ai"
    segments = []
    for text in texts:
        payload = {
            "content": text["text"],
            "return_chunks": True
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {JINA_API_KEY}",
            "Accept": "application/json"
        }
        
        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json().get("data", {})
            segments.append({
                "title": text["title"],
                "chunks": data.get("chunks")
            })
            logger.info(f"Segmented text for paper: {text['title']}")
        except requests.RequestException as e:
            logger.error(f"An error occurred while segmenting {text['title']}: {e}")
    
    return segments

def generate_embeddings(segments, task_type):
    """
    Generate embeddings for each segment, using the specifed task type.
    """
    endpoint = "https://api.jina.ai/v1/embeddings"
    for paper in segments:
        for chunk in paper["chunks"]:
            payload = {
                "model": "jina-clip-v1", 
                "input": [{"text": chunk}],
                "task_type": task_type
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {JINA_API_KEY}",
                "Accept": "application/json"
            }
            
            try:
                response = requests.post(endpoint, json=payload, headers=headers)
                response.raise_for_status()
                logger.info(f"Generated embeddings for a segment in {paper['title']}")
            except requests.RequestException as e:
                logger.error(f"An error occurred while generating embeddings for {paper['title']}: {e}")

def search_query(query, segments):
    """
    Allow the user to enter a search query to search through the papers, using task_type retrieval.query
    """
    endpoint = "https://api.jina.ai/v1/embeddings"
    payload = {
        "model": "jina-clip-v1",
        "input": [{"text": query}],
        "task_type": "retrieval.query"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Accept": "application/json"
    }

    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        logger.info(f"Processed search query: {query}")
        query_embedding = response.json().get("data", [])[0]["embedding"]
        
        # Match query embedding with segments' embeddings (simplified mockup - actual matching requires cosine similarity etc.)
        for paper in segments:
            logger.info(f"Title: {paper['title']}")
            for chunk in paper["chunks"]:
                logger.info(f"Matching Passage: {chunk[:200]}...")
    except requests.RequestException as e:
        logger.error(f"An error occurred while processing query {query}: {e}")

def main():
    search_term = "embeddings"
    query = input("Enter your search query: ")
    
    papers = get_latest_papers(search_term)
    scraped_texts = scrape_papers(papers)
    segmented_texts = segment_texts(scraped_texts)
    generate_embeddings(segmented_texts, task_type="retrieval.passage")
    search_query(query, segmented_texts)

if __name__ == "__main__":
    main()
```