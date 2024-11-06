import os
import requests
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

JINA_API_KEY = os.getenv("JINA_API_KEY")
HEADERS = {"Authorization": f"Bearer {JINA_API_KEY}"}

def get_recipes(ingredients):
    """
    Get a list of recipe names based on available ingredients.
    """
    query = ", ".join(ingredients)
    response = requests.post(
        "https://s.jina.ai/",
        headers=HEADERS,
        json={"q": query, "count": 5, "respondWith": "json"}
    )
    if response.status_code != 200:
        logging.error(f"Failed to search for recipes: {response.text}")
        return []
    
    recipes = [result["title"] for result in response.json()["data"]]
    logging.info(f"Found recipes: {recipes}")
    return recipes

def recipe_summaries(recipes):
    """
    Retrieve summaries for each recipe.
    """
    summaries = []
    for recipe in recipes:
        response = requests.post(
            "https://r.jina.ai/",
            headers=HEADERS,
            json={"url": recipe["link"], "respondWith": "json"}
        )
        if response.status_code != 200:
            logging.error(f"Failed to fetch recipe summary for {recipe['name']}: {response.text}")
            continue
        
        summary = response.json()["data"]
        summaries.append({"name": recipe["name"], "link": recipe["link"], "summary": summary})
    
    return summaries

def rerank_by_healthiness(summaries):
    """
    Re-ranks recipes by healthiness.
    """
    rerank_query = "healthiness"
    documents = [summary["summary"] for summary in summaries]
    
    response = requests.post(
        "https://api.jina.ai/v1/rerank",
        headers=HEADERS,
        json={"model": "jina-reranker-v2-base-multilingual", "query": rerank_query, "documents": documents, "top_n": len(documents), "return_documents": True}
    )
    
    if response.status_code != 200:
        logging.error(f"Failed to rerank recipes: {response.text}")
        return []

    reranked_summaries = response.json()["results"]
    sorted_summaries = [summaries[result["index"]] for result in reranked_summaries]
    return sorted_summaries

def recommend_recipes(ingredients):
    """
    Main function to recommend recipes.
    """
    logging.info("Starting recipe recommendation process...")
    
    recipe_names = get_recipes(ingredients)
    if not recipe_names:
        logging.warning("No recipes found.")
        return
    
    summaries = recipe_summaries(recipe_names)
    if not summaries:
        logging.warning("No summaries available for the found recipes.")
        return
    
    reranked_summaries = rerank_by_healthiness(summaries)
    
    for recipe in reranked_summaries:
        print(f"Recipe Name: {recipe['name']}\nSummary: {recipe['summary']}\nLink: {recipe['link']}\n")

# Example ingredients
ingredients = [
    "Onion", "Chickpeas", "Tinned chopped tomatoes", "Chicken thighs",
    "EVOO", "S+P", "Cumin", "Garlic", "Ginger", "Italian seasoning", 
    "Chilli flakes", "Sweet potato", "Peanut butter", "Chicken stock", "Milk", "Sugar"
]

try:
    recommend_recipes(ingredients)
except Exception as e:
    logging.error(f"An error occurred: {str(e)}")