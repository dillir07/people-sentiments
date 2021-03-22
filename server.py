# import flask
from flask import Flask, request, jsonify, render_template
from textblob import TextBlob

from twitter_api_handler import get_tweets_with_sentiment

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/get_sentiments", methods=["POST"])
def get_sentiments():
    """"""
    search_term = request.args["q"]
    items_count = int(request.args["count"])

    response = get_tweets_with_sentiment(query=search_term, count=items_count)
    return jsonify(response)


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
