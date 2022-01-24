from flask import Flask, redirect, request, jsonify, Response,render_template
from threading import Thread
app = Flask("Embed Generator")

@app.route("/")
def home():
    return "Im alive"

@app.route("/embed")
def embeds():
    return render_template("index.html")

def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
