from flask import Flask, render_template, request, jsonify
from newspaper import Article
import requests
import os

app = Flask(__name__)

# 🔐 Hugging Face API
HF_API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
HF_TOKEN = os.environ.get("HF_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def summarize_text(text):
    payload = {"inputs": text}
    response = requests.post(HF_API_URL, headers=HEADERS, json=payload)
    result = response.json()

    if isinstance(result, list):
        return result[0]["summary_text"]
    else:
        return "Error generating summary"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    text = data.get("text", "").strip()

    if text.startswith("http"):
        article = Article(text)
        article.download()
        article.parse()
        text = article.text

    summary = summarize_text(text)
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run()
