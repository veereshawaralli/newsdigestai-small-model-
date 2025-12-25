
from flask import Flask, render_template, request
from transformers import pipeline
from newspaper import Article
import re

app = Flask(__name__)

# Lightweight model for free hosting
summarizer = pipeline("summarization", model="t5-small")

def is_url(text):
    return re.match(r'https?://\S+', text)

def extract_article_from_url(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

@app.route("/", methods=["GET", "POST"])
def index():
    summary_text = ""
    if request.method == "POST":
        user_input = request.form["text"]

        if is_url(user_input):
            text = extract_article_from_url(user_input)
        else:
            text = user_input

        summary = summarizer(
            "summarize: " + text,
            max_length=150,
            min_length=50,
            do_sample=False
        )

        summary_text = summary[0]["summary_text"]

    return render_template("index.html", summary=summary_text)

if __name__ == "__main__":
    app.run(debug=True)
