# import flask
from flask import Flask, request, jsonify, render_template
from textblob import TextBlob
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/get_sentiment", methods=["POST"])
def get_sentiment():
    sentiment = None
    if request.method == "POST":
        text = request.form["text"]
        sentiment = TextBlob(text).sentiment
        return render_template("result.html", sentiment_output=sentiment)
    else:
        return render_template("error.html")


@app.route("/get_sentiment_api", methods=["POST"])
def get_sentiment_api():
    sentiment = None
    if request.method == "POST":
        # note for api it is not request.from use request.args instead
        if not "text" in request.args.keys():
            res = {"ct": request.content_type, "args": request.args}
            return jsonify(res)
        text = request.args["text"]
        sentiment = TextBlob(text).sentiment
        return jsonify(sentiment)
    else:
        return jsonify("error")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
