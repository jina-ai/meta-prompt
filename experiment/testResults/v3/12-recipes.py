import os
import requests
import logging
from typing import List, Dict, Tuple

# Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Reading API Key from environment variable
JINA_API_KEY = os.environ["JINA_API_KEY"]

# Headers required for Jina API
headers = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Ingredients at home
ingredients = [
    "Onion", "Chickpeas", "Tinned chopped tomatoes", "Chicken thighs",
    "EVOO", "S+P", "Cumin", "Garlic", "Ginger", "Italian seasoning",
    "Chilli flakes", "Sweet potato", "Peanut butter", "Chicken stock",
    "Milk", "Sugar"
]

# Equipment at home
equipment = ["Stove top", "Pots and pans", "Slow cooker", "Various utensils"]

def brainstorm_recipes(ingredients: List[str]) -> List[str]:
    """
    Generate a list of possible recipe names based on the provided ingredients.
    """
    query = f"Provide recipe names using these ingredients: {', '.join(ingredients)}."
    data = {"prompt": query, "temperature": 0.7, "max_tokens": 150, "model": "claude-3.5-sonnet"}
    response = requests.post("https://api.jina.ai/v1/generate", json=data, headers=headers)
    
    if response.status_code == 200:
        recipes = response.json()['choices'][0]['text'].splitlines()
        logger.info("Brainstorming recipes...")
        return recipes
    else:
        logger.error("Failed to generate recipes.")
        return []

def search_and_summarize_recipes(recipe_names: List[str]) -> List[Dict[str, str]]:
    """
    For each recipe name, search the web, summarize the recipe, and return a list of summaries.
    """
    summaries = []
    for recipe in recipe_names:
        try:
            # Using s.reader to search the web for recipes
            search_endpoint = f"https://s.jina.ai/{recipe}"
            response = requests.get(search_endpoint, headers=headers)
            results = response.json()['data'] if response.status_code == 200 else []

            if results:
                # Taking first search result for simplification
                url = results[0]['url']
                # Retrieving and summarizing the web page using r.reader
                r_reader_endpoint = f"https://r.jina.ai/{url}"
                r_reader_response = requests.get(r_reader_endpoint, headers=headers)
                if r_reader_response.status_code == 200:
                    summary = r_reader_response.json()['data']['content'][:500]  # Getting a part of the content
                    summaries.append({"name": recipe, "summary": summary, "url": url})
        except Exception as e:
            logger.error(f"Error processing {recipe}: {str(e)}")
    return summaries

def rerank_recipes_by_healthiness(recipe_summaries: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Rerank the provided recipe summaries by healthiness using a basic heuristic (e.g., mentions of "fried" or "sugar").
    """
    # Simplified healthiness scoring: fewer mentions of unhealthy terms score higher
    unhealthy_terms = ['fried', 'sugar', 'cream']
    for recipe in recipe_summaries:
        recipe['health_score'] = sum(recipe['summary'].lower().count(term) for term in unhealthy_terms)
    ranked_recipes = sorted(recipe_summaries, key=lambda x: x['health_score'])
    return ranked_recipes

def main():
    logger.info("Starting recipe recommendation process...")
    recipe_names = brainstorm_recipes(ingredients)
    recipe_summaries = search_and_summarize_recipes(recipe_names)
    ranked_recipes = rerank_recipes_by_healthiness(recipe_summaries)

    for recipe in ranked_recipes:
        logger.info(f"Recipe Name: {recipe['name']}\nSummary: {recipe['summary']}\nLink: {recipe['url']}\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"An error occurred during the recipe recommendation process: {str(e)}")