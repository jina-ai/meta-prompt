import os
import requests
from datetime import datetime

# Load the environment variable for the Jina API key
token = os.environ["JINA_API_KEY"]

# Endpoint and headers for the g.reader API to check the statement's validity
endpoint = "https://g.jina.ai"
headers = {
    "Authorization": f"Bearer {token}",  # Use the loaded API key for authorization
    "Accept": "application/json"  # Request JSON response for ease of parsing
}

# The statement to check
statement = "The UK government has announced a new law that will require social media companies to verify the age of their users."

# Prepare and send the request
response = requests.get(endpoint, params={"query": statement}, headers=headers)

# Parsing the response to handle the JSON data
if response.status_code == 200:
    data = response.json()
    # Check if the statement is found to be true or false based on the g.reader API response
    if data["data"]["result"] == True:
        result = "verified as true"
    else:
        result = "found to be false"
    references = data["data"].get("references", "No references provided")
    print(f"The statement was {result}.\nReferences: {references}")
else:
    # Handle API errors or issues
    print("Failed to verify the statement due to an error with the g.reader API.")

# Optionally, log or handle the verification result further, e.g., by storing it in a database or file for record-keeping.
# Record the date and time of the verification attempt for future reference.
verification_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"Verification attempt time: {verification_time}")