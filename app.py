from flask import Flask, render_template, request
from newspaper import Article
from transformers import pipeline

app = Flask(__name__)

# Load summarizer (lightweight)
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=-1   # CPU only
)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    article_input = request.form.get("article")

    if article_input.startswith("http"):
        article = Article(article_input)
        article.download()
        article.parse()
        text = article.text
    else:
        text = article_input

    summary = summarizer(
        text,
        max_length=150,
        min_length=60,
        do_sample=False
    )[0]["summary_text"]

    return render_template(
        "index.html",
        summary=summary,
        article=article_input
    )

if __name__ == "__main__":
    app.run(debug=True)
