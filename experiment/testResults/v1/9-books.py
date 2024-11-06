I'm unable to execute or simulate live API calls, including those to Jina AI's services, or directly generate, modify, or manage external files or databases from this platform. However, I can provide you with a detailed Python script that shows how to achieve the tasks you described, using Jina AI Search Foundation APIs, including handling embedding generation, classification, and search functionalities. Remember to replace `"YOUR_JINA_API_KEY"` with your actual Jina API key.

```python
import requests
import json
import os
from rich import console

console = console.Console()

JINA_API_KEY = os.getenv("JINA_API_KEY")
headers = {"Authorization": f"Bearer {JINA_API_KEY}"}

def get_book_info(author):
    url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}&langRestrict=en&maxResults=30&printType=books&orderBy=newest"
    response = requests.get(url)
    if response.status_code == 200:
        books = response.json().get("items", [])
        no_dup_books = []
        titles = set()
        for book in books:
            info = book.get("volumeInfo", {})
            title = info.get("title", "")
            if title not in titles:
                titles.add(title)
                no_dup_books.append({
                    "author": author,
                    "title": title,
                    "published_date": info.get("publishedDate", ""),
                    "description": info.get("description", ""),
                    "genre": classify_genre(info.get("categories", []))
                })
        return no_dup_books[:10]
    else:
        console.log(f"Error fetching books for author {author}: {response.status_code}")
        return []

def classify_genre(categories):
    if "Science Fiction" in categories or "Fantasy" in categories:
        return "Fantasy"
    elif "Non-fiction" in categories:
        return "Non-fiction"
    else:
        return "Other"

def generate_embeddings(descriptions):
    data = {
        "model": "jina-embeddings-v3",
        "input": descriptions,
        "task": "retrieval.passage",
        "late_chunking": True,
    }
    response = requests.post("https://api.jina.ai/v1/embeddings", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        console.log(f"Error generating embeddings: {response.status_code}")
        return None

def main():
    authors = ["Terry Pratchett", "William Shakespeare"]
    books_with_embeddings = []

    for author in authors:
        books = get_book_info(author)
        descriptions = [book["description"] for book in books]
        embeddings = generate_embeddings(descriptions)
        
        if embeddings:
            for book, embedding in zip(books, embeddings):
                book["embedding"] = embedding["embedding_vector"]
                books_with_embeddings.append(book)
    
    # Save all data excluding embeddings to books.json and all data to books-embeddings.json
    with open("books.json", "w") as f:
        json.dump([book for book in books_with_embeddings if "embedding" not in book], f, indent=4)

    with open("books-embeddings.json", "w") as f:
        json.dump(books_with_embeddings, f, indent=4)
    
    console.log("Saved book data and embeddings.")

if __name__ == "__main__":
    main()
```

This script fetches the latest books from the given authors, attempts to classify their genre, generates embeddings for their descriptions, and finally saves the processed data into JSON files. Remember, this script requires your Jina AI API key to be available as an environment variable `JINA_API_KEY`.

You'll need to fill in the parts related to error logging, embedding generation adjustment according to the response format you plan to use them in, and modify the `classify_genre` function based on the actual category data you receive from Google Books API.