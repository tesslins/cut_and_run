#!/usr/bin/env python

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03' #copied secret key -- need to figure out what's up with this ish -- is it supposed to be auto-generated or something?

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)