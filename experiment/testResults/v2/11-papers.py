import os
import requests
from rich.console import Console
from rich.traceback import install
from urllib.parse import quote

# Rich setup for beautiful logging
console = Console()
install(show_locals=True)

# Environment variable for Jina API Key
JINA_API_KEY = os.environ.get('JINA_API_KEY')

# Headers for authorization
headers = {
    'Authorization': f'Bearer {JINA_API_KEY}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Function to search for the latest papers on arxiv with the term "embeddings"
def search_papers():
    search_url = 'https://s.jina.ai/'
    search_payload = {
        "q": "embeddings site:arxiv.org",
        "options": "Text"
    }
    
    try:
        response = requests.post(search_url, json=search_payload, headers=headers)
        response.raise_for_status()
        papers = response.json()['data'][:3]  # Get the top 3 results
        console.log(f"[green]Found {len(papers)} papers related to 'embeddings'")
        return papers
    except Exception as e:
        console.log("[red]Failed to search for papers:", e)
        return []

# Function to scrape each paper's PDF and store the text and title
def scrape_paper(url):
    reader_url = 'https://r.jina.ai/'
    reader_payload = {
        "url": url,
        "options": "Text"  # Assuming we want to retrieve text for simplicity
    }
    
    try:
        response = requests.post(reader_url, json=reader_payload, headers=headers)
        response.raise_for_status()
        data = response.json()['data']
        console.log(f"[green]Scraped paper: {data['title']}")
        return data['content'], data['title']
    except Exception as e:
        console.log(f"[red]Failed to scrape {url}:", e)
        return "", ""

# Function to segment text
def segment_text(text):
    segment_url = 'https://segment.jina.ai/'
    segment_payload = {
        "content": text,
        "return_chunks": True
    }
    
    try:
        response = requests.post(segment_url, json=segment_payload, headers=headers)
        response.raise_for_status()
        chunks = response.json()['chunks']
        console.log(f"[green]Segmented text into {len(chunks)} chunks")
        return chunks
    except Exception as e:
        console.log("[red]Failed to segment text:", e)
        return []

# Function to generate embeddings for text segments
def generate_embeddings(chunks):
    embeddings_url = 'https://api.jina.ai/v1/embeddings'
    embeddings_payload = {
        "model": "jina-embeddings-v3",
        "input": chunks,
        "task": "retrieval.passage"
    }
    
    try:
        response = requests.post(embeddings_url, json=embeddings_payload, headers=headers)
        response.raise_for_status()
        embeddings = response.json()['data']
        console.log("[green]Generated embeddings for text segments")
        return embeddings
    except Exception as e:
        console.log("[red]Failed to generate embeddings:", e)
        return []

# Main process
def main():
    papers = search_papers()
    for paper in papers:
        url = paper['url']
        text, title = scrape_paper(url)
        if text and title:
            chunks = segment_text(text)
            if chunks:
                embeddings = generate_embeddings(chunks)
                console.log(f"[green]Processed {title} successfully")
            else:
                console.log(f"[red]No chunks to process for {title}")
        else:
            console.log(f"[red]Failed to process {title}")

if __name__ == "__main__":
    main()