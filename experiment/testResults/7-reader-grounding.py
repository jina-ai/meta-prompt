import requests
import os

token = os.environ["JINA_API_KEY"]
endpoint = "https://g.jina.ai"
query = "The UK government has announced a new law that will require social media companies to verify the age of their users."

headers = {
  "Accept": "application/json",
  "Authorization": f"Bearer {token}"
}

response = requests.get(f"{endpoint}", params={"q": query}, headers=headers)
data = response.json()

print(data)