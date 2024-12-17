from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# File to store articles
ARTICLE_FILE = "articles.json"

# Load existing articles
if os.path.exists(ARTICLE_FILE):
    with open(ARTICLE_FILE, "r") as f:
        articles = json.load(f)
else:
    articles = {}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        article_id = str(len(articles) + 1)  # Generate article ID
        
        # Save article
        articles[article_id] = {"title": title, "content": content}
        with open(ARTICLE_FILE, "w") as f:
            json.dump(articles, f)
        
        # Redirect to article page
        return redirect(url_for("view_article", article_id=article_id))
    return render_template("index.html")


@app.route("/article/<article_id>")
def view_article(article_id):
    article = articles.get(article_id)
    if article:
        return render_template("article.html", title=article["title"], content=article["content"])
    return "Article Not Found", 404


@app.route("/api/articles", methods=["GET"])
def api_articles():
    return jsonify(articles)

@app.route("/articles")
def list_articles():
    return render_template("articles.html", articles=articles)

if __name__ == "__main__":
    app.run(debug=True)
