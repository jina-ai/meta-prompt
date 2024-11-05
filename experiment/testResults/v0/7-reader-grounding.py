import os
import requests

# Retrieve API key from environment variable
api_key = os.getenv('JINA_API_KEY')

def check_statement_validity(statement):
    # Grounding API request
    grounding_api_url = "https://g.jina.ai/"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    data = {
        "q": "fact check query",
        "statement": statement
    }
    
    response = requests.post(grounding_api_url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if result["status"] == "success":
            fact_check_result = result["data"]["factCheckResult"]
            reason = result["data"]["reason"]
            sources = result["data"]["sources"]
            print(f"Fact Check Result: {fact_check_result}")
            print(f"Reason: {reason}")
            if sources:
                print("Sources:")
                for source in sources:
                    print(source)
        else:
            print("Fact check failed.")
    else:
        print(f"API Error: {response.status_code}")

# Example statement from bbc.com to verify
statement_to_verify = "The UK government has announced a new law that will require social media companies to verify the age of their users."
check_statement_validity(statement_to_verify)