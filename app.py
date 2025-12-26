from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# ✅ Read token from environment (REQUIRED)
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

if not HF_API_TOKEN:
    raise RuntimeError("HF_API_TOKEN not set")

# ✅ Lightweight summarization model
API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"

HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

def summarize_text(text):
    payload = {
        "inputs": text[:2000]  # keep input small for speed + memory
    }
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload,
        timeout=25
    )
    result = response.json()
    return result[0]["summary_text"]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.form.get("text", "")
    summary = ""

    try:
        summary = summarize_text(text)
    except Exception as e:
        summary = "⚠️ Unable to summarize right now. Please try again."

    return render_template("index.html", summary=summary, article=text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
