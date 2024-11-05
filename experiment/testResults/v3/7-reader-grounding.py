import os
import requests

# Fetch the API token from environment variables
jina_api_key = os.environ.get("JINA_API_KEY")

# Setup the header with authorization and content type
headers = {
    "Authorization": f"Bearer {jina_api_key}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Define the statement to be checked
statement = "The UK government has announced a new law that will require social media companies to verify the age of their users."

# Setup the request data for g.reader fact-checker API
data = {
    "query": statement
}

# Send the request to the g.reader API endpoint
response = requests.post("https://g.jina.ai", json=data, headers=headers)

if response.status_code == 200:
    # Parse the JSON response
    result = response.json()
    
    # Extract the factuality result, true or false
    is_statement_valid = result["data"]["result"]
    
    # Print out the validity of the statement
    print(f"The statement is: {'valid' if is_statement_valid else 'invalid'}")

else:
    print("Failed to check the statement's validity.")