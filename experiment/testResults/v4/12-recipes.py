import os
import requests

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
JINA_API_KEY = os.environ['JINA_API_KEY']

def get_headers():
    """
    Prepare the headers for authorization and accept JSON responses.
    """
    return {
        'Authorization': f'Bearer {JINA_API_KEY}',
        'Accept': 'application/json'
    }

def search_recipes(ingredients):
    """
    Search for recipes using specified ingredients.
    """
    query = f'Recipes with {", ".join(ingredients)}'
    url = 'https://s.jina.ai/'
    headers = get_headers()
    payload = {
        'q': query,
        'options': 'Text'
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print("Error searching for recipes:", response.json())
        return []

def summarize_recipe(url):
    """
    Summarize the specified recipe from a URL.
    """
    summarizer_url = 'https://r.jina.ai/'
    headers = get_headers()
    payload = {
        'url': url
    }
    response = requests.post(summarizer_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['data']['content']
    else:
        print("Error summarizing recipe:", response.json())
        return ""

def rank_recipes_by_healthiness(recipes):
    """
    Re-rank recipes by their healthiness based on ingredients and content.
    NOT IMPLEMENTABLE with Jina AI's current API set as there's no direct healthiness rating API.
    Placeholder function for potential future capabilities.
    """
    # A placeholder implementation as direct recipe healthiness ranking isn't available.
    # One might use predefined criteria or look for specific health-related words/phrases instead.
    return recipes

def main():
    ingredients = ["Onion", "Chickpeas", "Tinned chopped tomatoes", "Chicken thighs", "EVOO", "S+P", "Cumin", "Garlic", "Ginger", "Italian seasoning", "Chilli flakes", "Sweet potato", "Peanut butter", "Chicken stock", "Milk", "Sugar"]
    
    recipe_links = search_recipes(ingredients)
    if not recipe_links:
        print("No recipes found.")
        return
    
    for recipe in recipe_links:
        summary = summarize_recipe(recipe['url'])
        print(f"Recipe Name: {recipe['title']}\nSummary: {summary}\nLink: {recipe['url']}\n")
        # Note: The summary could be empty if there was an error.

if __name__ == "__main__":
    main()