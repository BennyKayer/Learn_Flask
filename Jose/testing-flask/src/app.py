from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def getHome():
    return jsonify({"message": "Hello World"})

