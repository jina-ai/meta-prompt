import os
import requests
from rich.console import Console

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
JINA_API_KEY = os.getenv("JINA_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

console = Console()

def search_papers(term="embeddings", max_results=3):
    search_url = "https://s.jina.ai/"
    body = {
        "q": term,
        "options": "Text"
    }
    try:
        response = requests.post(search_url, json=body, headers=HEADERS)
        response.raise_for_status()
        data = response.json().get("data", [])[:max_results]
        papers = [{"title": item["title"], "url": item["url"]} for item in data]
        return papers
    except Exception as e:
        console.log(f"[bold red]Error searching for papers: {e}[/bold red]")
        return []

def scrape_paper(paper):
    reader_url = "https://r.jina.ai/"
    body = {
        "url": paper["url"]
    }
    try:
        response = requests.post(reader_url, json=body, headers=HEADERS)
        response.raise_for_status()
        data = response.json()["data"]
        return {"title": data["title"], "content": data["content"]}
    except Exception as e:
        console.log(f"[bold red]Error scraping paper: {e}[/bold red]")
        return None

def segment_content(content):
    segment_url = "https://segment.jina.ai/"
    body = {
        "content": content,
        "return_chunks": True
    }
    try:
        response = requests.post(segment_url, json=body, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data.get("chunks")
    except Exception as e:
        console.log(f"[bold red]Error segmenting content: {e}[/bold red]")
        return []

def generate_embeddings(segments):
    embeddings_url = "https://api.jina.ai/v1/embeddings"
    body = {
        "model": "jina-embeddings-v3",
        "input": segments,
        "task": "retrieval.passage"
    }
    try:
        response = requests.post(embeddings_url, json=body, headers=HEADERS)
        response.raise_for_status()
        embeds = response.json().get("data", [])
        return [embed for embed in embeds]
    except Exception as e:
        console.log(f"[bold red]Error generating embeddings: {e}[/bold red]")
        return []

def search_within_papers(query, papers_embeddings):
    embeddings_url = "https://api.jina.ai/v1/embeddings"
    body = {
        "model": "jina-embeddings-v3",
        "input": [query],
        "task": "retrieval.query"
    }
    matching_passages = []
    try:
        query_embed_response = requests.post(embeddings_url, json=body, headers=HEADERS)
        query_embed_response.raise_for_status()
        query_embed = query_embed_response.json().get("data", [])[0]["embedding"]

        for paper, segments_embeddings in papers_embeddings.items():
            for segment, embed in segments_embeddings:
                # Example condition for similarity (this should be an actual embedding comparison calculation)
                if query_embed[:5] == embed["embedding"][:5]:  # Placeholder similarity check
                    matching_passages.append((paper, segment))
        return matching_passages
    except Exception as e:
        console.log(f"[bold red]Error searching within papers: {e}[/bold red]")
        return []

def main():
    papers = search_papers()
    if papers:
        papers_contents = {}
        papers_embeddings = {}
        for paper in papers:
            console.log(f"Scraping paper: [bold green]{paper['title']}[/bold green]")
            content = scrape_paper(paper)
            if content:
                segments = segment_content(content["content"])
                embeddings = generate_embeddings(segments)
                papers_contents[paper["title"]] = content
                papers_embeddings[paper["title"]] = zip(segments, embeddings)

        query = console.input("Enter your search query: ")
        matches = search_within_papers(query, papers_embeddings)
        for title, segment in matches:
            console.log(f"Match found in  [bold]{title}[/bold]: {segment}")
            
if __name__ == "__main__":
    main()