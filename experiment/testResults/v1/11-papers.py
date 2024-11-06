import os
import requests
from rich.console import Console
from rich.logging import RichHandler
import logging

# Setup rich logging
logging.basicConfig(level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger("rich")

# Jina API Key
JINA_API_KEY = os.getenv("JINA_API_KEY")
if not JINA_API_KEY:
    logger.error("JINA_API_KEY environment variable not set. Please set it before running this code.")
    exit(1)

# Headers for API requests
headers = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def search_papers(search_term):
    """Search for the latest papers with the search term"""
    url = "https://s.jina.ai/"
    payload = {
        "q": search_term,
        "options": "Default"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        papers = response.json()["data"][:3]  # Get the top 3 papers
        logger.info("Successfully found papers based on the term.")
        return [(paper["title"], paper["url"]) for paper in papers]
    except Exception as e:
        logger.error(f"Error searching for papers: {e}")
        return []


def read_content(url):
    """Read contents of a paper using the Reader API"""
    read_url = "https://r.jina.ai/"
    payload = {
        "url": url
    }
    
    try:
        response = requests.post(read_url, json=payload, headers=headers)
        response.raise_for_status()
        content = response.json()["data"]["content"]
        logger.info("Successfully read the paper content.")
        return content
    except Exception as e:
        logger.error(f"Error reading content from {url}: {e}")
        return ""


def generate_embeddings(text_segments, task_type="retrieval.passage"):
    """Generate embeddings for each text segment"""
    url = "https://api.jina.ai/v1/embeddings"
    payload = {
        "model": "jina-embeddings-v3",
        "input": text_segments,
        "task": task_type,
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        embeddings = response.json()["data"]
        logger.info("Successfully generated embeddings.")
        return embeddings
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        return []


def search_in_paper(segments, query):
    """Search a query within the paper's segments"""
    embeddings = generate_embeddings([query] + segments, task_type="retrieval.query")
    query_embedding = embeddings[0]['embedding_vector']
    segment_embeddings = embeddings[1:]
    scores = [(index, cosine_similarity(query_embedding, segment['embedding_vector'])) for index, segment in enumerate(segment_embeddings)]
    scores.sort(key=lambda x: x[1], reverse=True)  # Sort by score highest to lowest
    top_matches = scores[:3]  # Top 3 matches
    logger.info("Successfully searched within the paper.")
    return [segments[index] for index, score in top_matches]


def cosine_similarity(vec1, vec2):
    """Calculate the cosine similarity between two vectors"""
    dot_product = sum(p*q for p,q in zip(vec1, vec2))
    magnitude = lambda vec: sum(x**2 for x in vec) ** .5
    return dot_product / (magnitude(vec1) * magnitude(vec2))


def main():
    search_term = "embeddings"
    papers = search_papers(search_term)
    
    for title, url in papers:
        logger.info(f"Reading {title}")
        content = read_content(url)
        segments = [content[i:i+512] for i in range(0, len(content), 512)]  # Simple segmentation
        embeddings = generate_embeddings(segments)
        logger.info(f"Generated embeddings for segments in {title}")
        
        # Assuming a user query for demonstration purposes
        user_query = "deep learning"
        matching_segments = search_in_paper(segments, user_query)
        
        logger.info(f"Matching segments for '{user_query}':")
        for segment in matching_segments:
            logger.info(f"Segment: {segment[:200]}...")  # Show a snippet


if __name__ == "__main__":
    main()