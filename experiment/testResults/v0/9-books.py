import os
import requests
from rich import console
from rich.console import Console

console = Console()

jina_api_key = os.getenv("JINA_API_KEY")

# Function to get embeddings for book descriptions
def get_embeddings(descriptions):
    headers = {
        "Authorization": f"Bearer {jina_api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "jina-embeddings-v3",
        "input": descriptions,
        "task": "retrieval.passage",
        "late_chunking": True,
    }

    response = requests.post(
        "https://api.jina.ai/v1/embeddings", headers=headers, json=data
    )
    
    if response.status_code == 200:
        return response.json()['data']
    else:
        console.log(f"Error getting embeddings: {response.text}")
        return []

# Function to classify genres
def classify_genres(descriptions):
    headers = {
        "Authorization": f"Bearer {jina_api_key}",
        "Content-Type": "application/json",
    }
    labels = ["Science-fiction", "Fantasy", "Non-fiction", "Other"]
    data = {
        "model": "jina-embeddings-v3",
        "input": [{"text": desc} for desc in descriptions],
        "labels": labels,
    }

    response = requests.post(
        "https://api.jina.ai/v1/classify", headers=headers, json=data
    )
    
    if response.status_code == 200:
        return [item['prediction'] for item in response.json()['data']]
    else:
        console.log(f"Error classifying genres: {response.text}")
        return []

# Function to search and process books
def search_books(authors):
    books_data = []
    embeddings_data = []
    for author in authors:
        # API Request
        url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:%22{author}%22&langRestrict=en&maxResults=40&printType=books&orderBy=newest"
        response = requests.get(url)
        if response.status_code == 200:
            items = response.json().get('items', [])
            descriptions = []
            for item in items[:10]: # Limit to 10 latest books
                volume_info = item['volumeInfo']
                title = volume_info.get('title', 'N/A')
                published_date = volume_info.get('publishedDate', 'N/A')
                description = volume_info.get('description', 'No description available.')

                # Temporary store description for embedding and classification
                descriptions.append(description)

                book_entry = {
                    "author": author,
                    "title": title,
                    "published_date": published_date,
                    "description": description,
                }
                books_data.append(book_entry)

            # Get genres and embeddings in bulk to reduce API calls
            genres = classify_genres(descriptions)
            embeddings = get_embeddings(descriptions)

            for i, book in enumerate(books_data[len(books_data)-len(items[:10]):]):
                book["genre"] = genres[i]
                book["embedding"] = embeddings[i]['embedding'] if i < len(embeddings) else []

                # Separate data excluding embeddings for books.json
                embeddings_data.append({
                    **book,
                    "embedding": book["embedding"]
                })
                # Exclude embedding for books.json
                book.pop("embedding", None)

            console.log(f"Processed {author}'s books")
        else:
            console.log(f"Error fetching books for {author}: {response.text}")

    with open("books.json", "w") as bj:
        bj.write(json.dumps(books_data, indent=4))

    with open("books-embeddings.json", "w") as be:
        be.write(json.dumps(embeddings_data, indent=4))

    console.log("Books data saved!")

# Search and interact
def search_query(query):
    embeddings = get_embeddings([query])[0]['embedding'] if get_embeddings([query]) else None
    if embeddings:
        # Calculate closeness between query embedding and book embeddings
        closeness_scores = []
        for book in embeddings_data:
            book_embedding = book['embedding']
            score = 1 - spatial.distance.cosine(embeddings, book_embedding) # Example calculation, replace with actual
            closeness_scores.append((book, score))

        # Sort based on closeness
        sorted_books = sorted(closeness_scores, key=lambda x: x[1], reverse=True)[:10]

        # Rerank the sorted books
        reranked_books = rerank_books(query, [book[0]['title'] for book in sorted_books])
        return reranked_books
    else:
        console.log("Error generating query embeddings")
        return []

def rerank_books(query, documents):
    headers = {
        "Authorization": f"Bearer {jina_api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "jina-reranker-v2-base-multilingual",
        "query": query,
        "documents": documents,
        "top_n": len(documents),
        "return_documents": True,
    }

    response = requests.post("https://api.jina.ai/v1/rerank", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['results']
    else:
        console.log(f"Error reranking: {response.text}")
        return []

search_books(["Terry Pratchett", "William Shakespeare"])
# Later, use search_query("your search term") to search through the processed books.