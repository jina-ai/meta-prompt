```python
import os
import requests
import json
from rich.console import Console
from rich.progress import track

# Ensure the JINA_API_KEY is set in your environment variables
JINA_API_KEY = os.environ.get("JINA_API_KEY", "")
if JINA_API_KEY == "":
    raise ValueError("Please set the JINA_API_KEY environment variable.")

headers = {"Authorization": f"Bearer {JINA_API_KEY}"}

# Initialize console for rich logging
console = Console()

def fetch_latest_books(author):
    """
    Fetch the latest 10 unique books by the author from Google Books API.
    """
    url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:\"{author}\"&langRestrict=en&maxResults=30&printType=books&orderBy=newest"
    response = requests.get(url)
    if response.status_code != 200:
        console.log(f"Error fetching books for author {author}. HTTP Status Code: {response.status_code}")
        return []
    books_data = response.json().get("items", [])
    
    books = []
    seen_titles = set()
    for book in books_data:
        if len(books) >= 10:
            break
        title = book["volumeInfo"].get("title", "")
        if title not in seen_titles:
            seen_titles.add(title)
            published_date = book["volumeInfo"].get("publishedDate", "")
            description = book["volumeInfo"].get("description", "")
            books.append({
                "author": author,
                "title": title,
                "published_date": published_date,
                "description": description
            })
    return books

def classify_genre(description):
    """
    Basic example of genre classification based on keywords.
    """
    keywords = {
        "Science-fiction": ["space", "planet", "alien", "universe", "sci-fi"],
        "Fantasy": ["dragon", "magic", "wizard", "sorcerer", "dwarf", "elf", "fairy"],
        "Non-fiction": ["history", "biography", "autobiography", "documentary"],
    }
    genre = "Other"
    for gen, keys in keywords.items():
        if any(word in description.lower() for word in keys):
            return gen
    return genre

def generate_embeddings(desc):
    """
    Generate embeddings for the given description.
    """
    data = {
        "model": "jina-embeddings-v3",
        "input": [desc],
        "task": "retrieval.passage",
        "late_chunking": True
    }
    response = requests.post("https://api.jina.ai/v1/embeddings", headers=headers, json=data)
    if response.status_code != 200:
        console.log(f"Error generating embedding. HTTP Status Code: {response.status_code}")
        return []
    return response.json()["data"][0]["embedding"]

# Main process
def main():
    authors = ["Terry Pratchett", "William Shakespeare"]
    all_books = []

    for author in authors:
        console.log(f"Fetching books for {author}")
        books = fetch_latest_books(author)
        for book in track(books, description=f"Processing {author}'s books..."):
            book['genre'] = classify_genre(book['description'])
            book['embedding'] = generate_embeddings(book['description'])
            all_books.append(book)
    
    # Save all data including embeddings
    with open('books-embeddings.json', 'w') as file:
        json.dump(all_books, file, indent=4)
    
    # Save data excluding embeddings
    for book in all_books:
        del book['embedding']
    with open('books.json', 'w') as file:
        json.dump(all_books, file, indent=4)

    console.log(f"Books data has been saved successfully.")

# Run main process
if __name__ == "__main__":
    main()
```