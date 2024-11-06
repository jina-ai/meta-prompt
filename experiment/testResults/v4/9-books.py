```python
import os
import requests
import json
from rich.console import Console
from rich.logging import RichHandler
import logging

# Setup rich logging
console = Console()
logging.basicConfig(level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger("rich")

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
JINA_API_KEY = os.getenv("JINA_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "application/json"
}

def generate_embeddings(description):
    data = {
        "model": "jina-embeddings-v3",
        "input": [description],
        "task": "retrieval.passage",
        "late_chunking": True
    }
    try:
        response = requests.post("https://api.jina.ai/v1/embeddings", json=data, headers=HEADERS)
        response.raise_for_status()
        embedding = response.json()['data'][0]['embedding']
        return embedding
    except requests.exceptions.HTTPError as err:
        logger.error(f"Error generating embedding: {err}")
        return None

def classify_genre(description):
    # For simplicity, genre classification is done based on keywords. This should ideally be replaced with a more robust method.
    if any(word in description.lower() for word in ["discworld", "magic", "wizard", "fantasy"]):
        return "Fantasy"
    elif any(word in description.lower() for word in ["science", "space", "future", "sci-fi"]):
        return "Science-fiction"
    elif "non-fiction" in description.lower():
        return "Non-fiction"
    else:
        return "Other"

def fetch_books_by_author(author):
    books = []
    url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:%22{author}%22&langRestrict=en&maxResults=30&printType=books&orderBy=newest"
    try:
        response = requests.get(url)
        response.raise_for_status()
        items = response.json().get("items", [])
        seen_titles = set()
        for item in items:
            if len(books) >= 10:
                break
            info = item.get("volumeInfo", {})
            title = info.get("title", "")
            published_date = info.get("publishedDate", "")
            description = info.get("description", "")

            if title not in seen_titles:
                seen_titles.add(title)
                genre = classify_genre(description)
                embedding = generate_embeddings(description)
                
                books.append({
                    "author": author,
                    "title": title,
                    "published_date": published_date,
                    "description": description,
                    "genre": genre,
                    "embedding": embedding
                })

    except requests.exceptions.HTTPError as err:
        logger.error(f"Failed to fetch books for {author}: {err}")
    
    return books

def main():
    authors = ["Terry Pratchett", "William Shakespeare"]
    all_books = []
    for author in authors:
        logger.info(f"Fetching books for {author}")
        books = fetch_books_by_author(author)
        all_books.extend(books)

    with open("books.json", "w") as f:
        json_books = [book for book in all_books if book.get("embedding") is None]
        json.dump(json_books, f, indent=4)
    
    with open("books-embeddings.json", "w") as f:
        json.dump(all_books, f, indent=4)

    logger.info("Books and their embeddings have been saved.")

if __name__ == "__main__":
    main()
```