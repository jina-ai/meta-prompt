import os
import requests

# Read JINA_API_KEY from environment
JINA_API_KEY = os.getenv("JINA_API_KEY")
AUTH_HEADER = {"Authorization": f"Bearer {JINA_API_KEY}"}

def verify_statement(statement):
    url = "https://g.jina.ai/"
    headers = {**AUTH_HEADER, "Content-Type": "application/json"}
    data = {"statement": statement}
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error verifying statement: {e}")
        return None

def main():
    statement = "The UK government has announced a new law that will require social media companies to verify the age of their users."
    result = verify_statement(statement)
    if result and result.get("status") == 20000:
        print("Statement verification result:", result["data"]["factuality"])
        if result["data"]["factuality"] == 1:
            print("The statement is verified to be true based on the references provided.")
        else:
            print("The statement could not be verified.")
        print("References:", result["data"]["references"])
    else:
        print("Failed to verify the statement.")

if __name__ == "__main__":
    main()