import os
import requests

# Environment variable for Jina API Key
jina_api_key = os.getenv('JINA_API_KEY')

# S.reader API endpoint for searching
endpoint = 'https://s.jina.ai'
headers = {
    'Authorization': f'Bearer {jina_api_key}'
}
params = {
    'query': 'The UK government has announced a new law that will require social media companies to verify the age of their users.',
    'lang': 'en-US'
}

# Sending the GET request
response = requests.get(endpoint, headers=headers, params=params)

# Parsing the response
if response.status_code == 200:
    data = response.json()
    articles = data.get('data', {})
    relevant_articles = [article for article in articles if 'bbc.com' in article.get('url', '')]
    if relevant_articles:
        print("Found relevant articles on BBC.com:")
        for article in relevant_articles:
            print(article.get('title'), '-', article.get('url'))
    else:
        print("No relevant articles found on BBC.com regarding the statement.")
else:
    print("Failed to fetch data from API.")