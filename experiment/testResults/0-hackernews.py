import os
import requests
import matplotlib.pyplot as plt
import umap
import numpy as np

# Load API token from environment variable
token = os.environ["JINA_API_KEY"]

# Define headers for Jina API request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# Define the endpoint for the r.reader API to fetch data from Hacker News
r_reader_endpoint = "https://r.jina.ai"
# Hacker News front page URL (as an example, usually this would be dynamic)
hn_front_page_url = "https://news.ycombinator.com"

# Fetch the front page of Hacker News
response = requests.get(f"{r_reader_endpoint}/{hn_front_page_url}", headers=headers)
data = response.json()

# Extract text content from the response
content_text = data["data"]["content"]

# Get embeddings for each sentence using Jina's embeddings API
embeddings_endpoint = "https://api.jina.ai/v1/embeddings"

# Split the content into sentences (here, we simply split by periods for demonstration purposes)
sentences = content_text.split('. ')

embeddings_data = {
    "model": "jina-clip-v1",
    "input": [{"text": sentence} for sentence in sentences if sentence]
}

# Fetch embeddings
embeddings_response = requests.post(embeddings_endpoint, headers=headers, json=embeddings_data)
embeddings = embeddings_response.json()

# Extract and normalize embeddings
embeddings_list = [item["embedding"] for item in embeddings["data"]]

# Use UMAP to reduce the dimensions of embeddings
reducer = umap.UMAP(n_components=2, random_state=42)
umap_embeddings = reducer.fit_transform(embeddings_list)

# Plotting the sentences as points on a 2D graph
plt.figure(figsize=(12, 10))
plt.scatter(umap_embeddings[:, 0], umap_embeddings[:, 1], alpha=0.5)
plt.title('Sentences from Hacker News Front Page in 2D Space')
plt.xlabel('UMAP Dimension 1')
plt.ylabel('UMAP Dimension 2')

# Optionally, annotate points with text (might clutter the graph if too many points)
for i, text in enumerate(sentences[:len(umap_embeddings)]):
    plt.annotate(text, (umap_embeddings[i, 0], umap_embeddings[i, 1]))

plt.show()