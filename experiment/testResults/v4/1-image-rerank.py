import os
import requests

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
JINA_API_KEY = os.getenv("JINA_API_KEY")

def classify_images(image_paths, labels):
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Accept": "application/json"
    }
    url = "https://api.jina.ai/v1/classify"
    predictions = []

    for image_path in image_paths:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
            base64_image = base64.b64encode(image_bytes).decode("utf-8")

        body = {
            "model": "jina-clip-v1",
            "input": [{"image": base64_image}],
            "labels": labels
        }

        response = requests.post(url, json=body, headers=headers)

        if response.status_code == 200:
            predictions.append(response.json()['data'][0]['prediction'])
        else:
            predictions.append("Error")

    return predictions


def main(image_paths, labels):
    predictions = classify_images(image_paths, labels)
    for path, prediction in zip(image_paths, predictions):
        print(f"{path}: {prediction}")

if __name__ == "__main__":
    # Example usage
    images = ["./path/to/image1.jpg", "./path/to/image2.jpg"]
    labels = ["animal", "vehicle", "scenery", "food"]
    main(images, labels)