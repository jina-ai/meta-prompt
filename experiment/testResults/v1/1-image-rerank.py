import os
import requests

# Read Jina API key from environment variable
JINA_API_KEY = os.getenv('JINA_API_KEY')
auth_headers = {'Authorization': f'Bearer {JINA_API_KEY}'}

def classify_images(images, labels):
    """
    Classify images based on the given labels using Jina Classifier API.
    :param images: List of base64-encoded image strings.
    :param labels: List of labels for classification.
    :return: Classification results.
    """
    classify_endpoint = "https://api.jina.ai/v1/classify"
    payload = {
        "model": "jina-clip-v1",
        "input": [{"image": img} for img in images],
        "labels": labels
    }
    try:
        response = requests.post(classify_endpoint, json=payload, headers=auth_headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        return str(err)
    except Exception as e:
        return str(e)

def main():
    # Example images and labels
    images = ["base64_image_string1", "base64_image_string2"]  # Replace with actual base64-encoded image strings
    labels = ["domain1", "domain2", "domain3"]  # Replace with your actual labels

    # Classify Images
    classification_results = classify_images(images, labels)
    print(classification_results)

if __name__ == "__main__":
    main()