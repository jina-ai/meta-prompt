import os
import requests
import json
from flask import Flask, request

app = Flask(__name__)

JINA_API_KEY = os.getenv("JINA_API_KEY")

# Handling segmentation and indexing of specified pages
def segment_and_index():
    urls = [
        "https://github.com/jeff-dh/SolidPython",
        "https://github.com/jeff-dh/SolidPython/wiki",
    ]

    segments = []
    for url in urls:
        response = requests.get(
            f"https://r.jina.ai/{url}",
            headers={"Authorization": f"Bearer {JINA_API_KEY}", "Accept": "application/json"}
        )
        data = response.json()
        content = data.get("data", {}).get("content", "")
        segments += [content]

    wiki_subpages = [
        "Installation",
        "Basic-Usage",
        "Advanced-Features",
        "Contributing",
    ]
    for page in wiki_subpages:
        response = requests.get(
            f"https://r.jina.ai/https://github.com/jeff-dh/SolidPython/wiki/{page}",
            headers={"Authorization": f"Bearer {JINA_API_KEY}", "Accept": "application/json"}
        )
        data = response.json()
        content = data.get("data", {}).get("content", "")
        segments += [content]

    # Save segments to a JSON file
    with open("segments.json", "w") as f:
        json.dump(segments, f)


@app.route('/ask', methods=['POST'])
def answer_question():
    question = request.json.get('question', '')

    # Load segments from stored JSON
    try:
        with open("segments.json", "r") as f:
            segments = json.load(f)
    except FileNotFoundError:
        return "Error: Segment data not found. Please ensure data is segmented and indexed before querying."

    # Call Jina API to generate embeddings for the question and documents
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {
        "model": "jina-clip-v1",
        "input": [{"text": question}] + [{"text": segment} for segment in segments],
    }

    embeddings_response = requests.post("https://api.jina.ai/v1/embeddings", headers=headers, json=data)
    embeddings = embeddings_response.json().get("data", [])

    # Using embeddings to find top 3 segments relevant to the question
    question_embedding = embeddings[0]["embedding"]
    segment_embeddings = embeddings[1:]

    similarities = [
        {"index": i, "similarity": sum([a * b for a, b in zip(question_embedding, segment["embedding"])])}
        for i, segment in enumerate(segment_embeddings)
    ]

    # Sorting by similarity score, highest first
    top3 = sorted(similarities, key=lambda x: x["similarity"], reverse=True)[:3]

    # Passing the top 3 segments to the LLM for answering the question
    segments_text = "\n- ".join([segments[i["index"]] for i in top3])
    command = f"""Based on these segments:\n\n- {segments_text}\nAnswer the question: {question}"""
    llm_response = requests.post(
        "https://api.jina.ai/v1/llm",
        headers={"Authorization": f"Bearer {JINA_API_KEY}", "Accept": "application/json"},
        json={"prompt": command, "model": "claude-3.5-sonnet"}
    )

    answer = llm_response.json().get("choices", [{}])[0].get("message", "No answer generated.")
    return {"answer": answer}


if __name__ == '__main__':
    segment_and_index()  # Ensure segments are indexed before starting server
    app.run(debug=True)