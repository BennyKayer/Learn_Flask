import os
from flask import Flask, render_template, send_from_directory
app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>Homepage</h1>"


@app.route('/<username>/<int:id>')
def hello_world(username=None, id=None):
    return render_template('./index.html', name=username, id=id)


@app.route('/blog/<name>')
def blog(name):
    return "<h1>Hello {{ name }}</h1>"


@app.route('/blog/2020/dogs')
def blog2():
    return 'this is my dog'
