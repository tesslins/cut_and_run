#!/usr/bin/env python
from flask import Flask, abort, request, render_template, jsonify
from mapmyfitness import MapMyFitness
import requests
import requests.auth
import json

app = Flask(__name__, static_url_path='')


mmf = MapMyFitness(api_key='hhp3ye7mq97jnuz8rxfzwc3fz39ef3rp',
                   access_token='4636bdf2cb0b82b456a855808925c42b67cab7ae')

@app.route('/')
def homepage():
    return render_template("new_index_copy.html")

@app.route('/route')
def plot_route():
    #route = mmf.route.find(348949363)  # search for route by ID
    #route_points = route.points(geojson=True)  # .points() method to get all route points as geoJSON
    return render_template("new_index_copy.html")

#routes_paginator = mmf.route.search(close_to_location=[35.555, -80.934], minimum_distance=9000, maximum_distance=11000)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

