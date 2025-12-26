from flask import Flask, render_template, request
import requests
from newspaper import Article

app = Flask(__name__)

# 🔑 Put your Hugging Face API token here
HF_API_TOKEN = "YOUR_HUGGINGFACE_API_KEY"

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

def summarize_text(text):
    payload = {
        "inputs": text[:3500]  # limit input to stay fast & cheap
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
    result = response.json()
    return result[0]["summary_text"]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    user_input = request.form.get("text")
    summary = ""

    try:
        if user_input.startswith("http"):
            article = Article(user_input)
            article.download()
            article.parse()
            text = article.text
        else:
            text = user_input

        summary = summarize_text(text)

    except Exception as e:
        summary = f"Error: {str(e)}"

    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
