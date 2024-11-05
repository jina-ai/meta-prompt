import os
import requests

JINA_API_KEY = os.getenv("JINA_API_KEY")
headers = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Content-Type": "application/json"
}

def classify_images(images, labels):
    url = "https://api.jina.ai/v1/classify"
    data = {
        "model": "jina-clip-v1",
        "input": [{"image": image} for image in images],
        "labels": labels
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

def main():
    images = ["base64_image_string1", "base64_image_string2"]  # Your base64 encoded images here
    labels = ["domain1", "domain2", "domain3"]  # Your classification labels here

    classification_results = classify_images(images, labels)
    print(classification_results)

if __name__ == "__main__":
    main()