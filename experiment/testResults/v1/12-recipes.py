import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
JINA_API_KEY = os.getenv("JINA_API_KEY")

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Headers for API requests
API_HEADERS = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Content-Type": "application/json"
}

# Function to perform web search
def search(query):
    try:
        response = requests.post(
            'https://s.jina.ai/',
            headers=API_HEADERS,
            json={"q": query, "options": "Default"}
        )
        response.raise_for_status()
        search_results = response.json()["data"]
        logging.info("Web search successful.")
        return search_results
    except Exception as e:
        logging.error(f"Web search failed: {e}")
        return []

# Function to summarize a webpage content
def summarize(url):
    try:
        response = requests.post(
            'https://r.jina.ai/',
            headers={**API_HEADERS, "X-No-Cache": "true"},
            json={"url": url}
        )
        response.raise_for_status()
        content = response.json()["data"]["content"]
        logging.info("Webpage summarization successful.")
        return content
    except Exception as e:
        logging.error(f"Webpage summarization failed: {e}")
        return ""

# Main execution function
def main():
    recipes_queries = [
        "chicken thighs with chickpeas recipe",
        "sweet potato peanut butter stew recipe",
        "spicy chicken with tinned tomatoes recipe"
    ]
    
    # Search for recipes
    all_search_results = []
    for query in recipes_queries:
        search_results = search(query)
        if search_results:
            for result in search_results:
                all_search_results.append({"title": result["title"], "url": result["url"]})
    
    if not all_search_results:
        logging.info("No recipes found matching the criteria.")
        return
    
    # Summarize the content of the recipe pages
    recipes_summaries = []
    for result in all_search_results:
        summary = summarize(result["url"])
        if summary:
            recipes_summaries.append({"title": result["title"], "summary": summary, "url": result["url"]})
    
    # Since we can't directly rank by healthiness without further data,
    # we encourage users to review the summaries and pick based on their dietary preferences.
    for recipe in recipes_summaries:
        print(f"Recipe Name: {recipe['title']}\nSummary:\n{recipe['summary']}\nLink: {recipe['url']}\n\n")

if __name__ == "__main__":
    main()