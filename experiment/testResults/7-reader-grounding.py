import os
import requests

def check_statement_validity(statement):
    """
    Uses Jina AI's grounding API to check the validity of the given statement.
    Requires the JINA_API_KEY to be set as an environment variable.

    Args:
    - statement (str): The statement to verify for factual accuracy.

    Returns:
    - dict: The result including whether the statement is supported, the reason, and references.
    """

    # Get your Jina AI API key for free: https://jina.ai/?sui=apikey
    api_key = os.getenv("JINA_API_KEY")
    if not api_key:
        raise ValueError("The 'JINA_API_KEY' environment variable is not set.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
        "statement": statement
    }

    response = requests.post("https://g.jina.ai/", headers=headers, json=payload)

    # Check if the request was successfully
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error during API call: {response.text}")

def main():
    statement = "The UK government has announced a new law that will require social media companies to verify the age of their users."
    try:
        validity_result = check_statement_validity(statement)
        print("Validity check result:", validity_result)
    except Exception as e:
        print("Error checking statement validity:", e)

if __name__ == "__main__":
    main()