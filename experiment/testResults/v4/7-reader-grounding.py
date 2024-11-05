import os
import requests

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
JINA_API_KEY = os.getenv("JINA_API_KEY")
HEADER = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def verify_statement(statement):
    url = "https://g.jina.ai/"
    payload = {"statement": statement}
    try:
        response = requests.post(url, json=payload, headers=HEADER)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"error": "Failed to verify the statement due to API error."}
    except Exception as e:
        return {"error": str(e)}

def main():
    statement = 'The UK government has announced a new law that will require social media companies to verify the age of their users.'
    result = verify_statement(statement)
    print(result)

if __name__ == "__main__":
    main()