import os
import requests

# Get your Jina AI API key for free: https://jina.ai/?sui=apikey
JINA_API_KEY = os.environ["JINA_API_KEY"]
HEADERS = {
    "Authorization": f"Bearer {JINA_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

def classify_images(image_paths, labels):
    classify_url = "https://api.jina.ai/v1/classify"
    images_base64 = []
    for path in image_paths:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            images_base64.append({"image": encoded_string})
    data = {
        "model": "jina-clip-v1",
        "input": images_base64,
        "labels": labels,
    }
    response = requests.post(classify_url, headers=HEADERS, json=data)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        return response.json()

def main():
    image_paths = ["path/to/your/image1.jpg", "path/to/your/image2.jpg"]
    labels = ["domain1", "domain2", "domain3"]
    classifications = classify_images(image_paths, labels)
    print(classifications)

if __name__ == "__main__":
    main()