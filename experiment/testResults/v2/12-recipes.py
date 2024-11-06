import os
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read the API key from environment
JINA_API_KEY = os.getenv("JINA_API_KEY")
if not JINA_API_KEY:
    raise EnvironmentError("JINA_API_KEY environment variable not found. Please set it before running the script.")

# Headers required for API calls
headers = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

def llm(query, model="claude-3.5-sonnet"):
    """
    Calls the LLM API to execute a query with a specific model.
    """
    try:
        payload = {"query": query, "model": model}
        response = requests.post("https://api.jina.ai/llm", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Failed to get response from LLM API: {str(e)}")
        return None

def read_recipe_page(url):
    """
    Uses the Reader API to retrieve content from the given recipe URL.
    """
    try:
        response = requests.post('https://r.jina.ai/', headers=headers, json={"url": url})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Failed to retrieve recipe page: {str(e)}")
        return None

def get_recipe_summary(page_content):
    """
    Summarizes the recipe content into a paragraph using LLM.
    """
    try:
        summary_query = f"Summarize this recipe: {page_content['data']['content']}"
        summary_response = llm(summary_query)
        if summary_response:
            return summary_response['choices'][0]['message']
        else:
            logging.error("Failed to summarize recipe content.")
            return None
    except Exception as e:
        logging.error(f"Failed to generate recipe summary: {str(e)}")
        return None

def main():
    # Ingredients list for brainstorming recipes
    ingredients = "Onion, Chickpeas, Tinned chopped tomatoes, Chicken thighs, EVOO, S+P, Herbs and spices: Cumin, garlic, ginger, Italian seasoning, chili flakes, Sweet potato, Peanut butter, Chicken stock, Milk, Sugar"
    
    # Query LLM for recipe names
    recipe_names_query = f"Generate recipe names using these ingredients: {ingredients}"
    recipe_names_response = llm(recipe_names_query)
    if not recipe_names_response:
        logging.error("No recipe names generated.")
        return
    
    recipe_names = recipe_names_response.get("results", [])
    for recipe_name in recipe_names:
        logging.info(f"Found recipe: {recipe_name}")
        
        # For each recipe, search the internet for the recipe page
        search_query = f"Recipe for {recipe_name}"
        search_response = requests.post('https://s.jina.ai/', headers=headers, json={"q": search_query})
        if search_response.status_code == 200:
            search_data = search_response.json()
            if search_data["results"]:
                recipe_page_url = search_data["results"][0]["url"]
                logging.info(f"Retrieved recipe page URL: {recipe_page_url}")
                
                # Summarize the recipe content
                page_content = read_recipe_page(recipe_page_url)
                if page_content:
                    summary = get_recipe_summary(page_content)
                    if summary:
                        logging.info(f"Recipe summary: {summary}")
                    else:
                        logging.error("Failed to summarize recipe.")
                else:
                    logging.error("Failed to retrieve recipe page content.")
            else:
                logging.error("No recipe page found for the generated recipe name.")
        else:
            logging.error("Failed to perform search for the recipe.")

if __name__ == "__main__":
    main()