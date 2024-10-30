import os
import requests

token = os.environ["JINA_API_KEY"]

# Use the g.reader API to check the validity of the statement from bbc.com
endpoint = "https://g.jina.ai"
headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}
data = {
    "statement": "The UK government has announced a new law that will require social media companies to verify the age of their users.",
    "source": ["https://bbc.com"]
}

response = requests.post(endpoint, json=data, headers=headers)

# Output the response from the API call
print(response.json())