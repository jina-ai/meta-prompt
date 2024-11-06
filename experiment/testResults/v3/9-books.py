import json
import os
import requests
from rich.console import Console
from rich.traceback import install
from dotenv import load_dotenv

# Initialize rich console and traceback
console = Console()
install()

# Load environment variables
load_dotenv()

# Jina API Key
JINA_API_KEY = os.getenv('JINA_API_KEY')

# Base headers for Jina API requests
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "application/json"
}

# Authors and genres mapping based on author nature
genres = {
    "Terry Pratchett": "Fantasy",
    "William Shakespeare": "Other"
}

# Function to classify genre based on book description
def get_genre(description):
    data = {
        "model": "jina-embeddings-v3", 
        "input": [ {"text": description} ],
        "labels": ["Science-fiction", "Fantasy", "Non-fiction", "Other"]
    }
    response = requests.post("https://api.jina.ai/v1/classify", json=data, headers=headers)
    if response.status_code == 200:
        # Return the genre with the highest score
        return max(response.json()['data'][0]['predictions'], key=lambda x: x['score'])['label']
    else:
        console.log(f"Error classifying genre: {response.json()}")


# Function to fetch and process books for an author
def fetch_books_for_author(author):
    url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:\"{author}\"&langRestrict=en&maxResults=30&printType=books&orderBy=newest"
    response = requests.get(url)
    if response.status_code == 200:
        books_data = response.json().get('items', [])
        processed_books = []
        for book in books_data[:10]:  # Limit to latest 10 books
            book_info = book['volumeInfo']
            title = book_info.get('title', 'N/A')
            published_date = book_info.get('publishedDate', 'N/A')
            description = book_info.get('description', 'N/A')
            # Use predefined genre based on the author; this could be enhanced by analyzing the description
            genre = genres[author]

            # Generate embedding
            embedding_data = {
                "model": "jina-clip-v1",
                "input": [{"text": description}]
            }
            embedding_response = requests.post("https://api.jina.ai/v1/embeddings", json=embedding_data, headers=headers)
            if embedding_response.status_code == 200:
                embedding = embedding_response.json()['data'][0]['embedding']
                console.log(f"Embedding generated for {title}")
            else:
                console.log(f"Failed to generate embedding for {title}: {embedding_response.json()}")
                embedding = []

            processed_books.append({
                "author": author,
                "title": title,
                "published_date": published_date,
                "description": description,
                "genre": genre,
                "embedding": embedding
            })
        return processed_books
    else:
        console.log(f"Failed to fetch books for {author}: {response.json()}")
        return []

# Main function to process authors and generate files
def main():
    authors = ["Terry Pratchett", "William Shakespeare"]
    all_books = []
    for author in authors:
        books = fetch_books_for_author(author)
        all_books.extend(books)
    
    # Write to books-embeddings.json including embeddings
    with open("books-embeddings.json", 'w') as file:
        json.dump(all_books, file, indent=4)
        console.log("books-embeddings.json has been written successfully.")
    
    # Exclude embeddings for books.json
    for book in all_books:
        book.pop('embedding', None)
    
    # Write to books.json excluding embeddings
    with open("books.json", 'w') as file:
        json.dump(all_books, file, indent=4)
        console.log("books.json has been written successfully.")

main()