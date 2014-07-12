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
    '''Search for a route by ID, get points as lat/lng tuples, turn into a geoJSON of lat/lng lists.'''
    route = mmf.route.find(348949363) 
    route_points = route.points(geojson=True)
    lat_lng_tuples = route_points['coordinates'] 
    lat_lng_lists = [list(point) for point in lat_lng_tuples] 
    route_points['coordinates'] = lat_lng_lists
    return render_template("new_index_copy.html")

@app.route('/route_search')
def search_route():
    '''Search for all routes near Oakland with min & max distance.'''
    routes_paginator = mmf.route.search(close_to_location=[35.555, 80.934])
    return render_template("new_index_copy.html")

if __name__ == '__main__':
    app.run(debug=True, port=5001)

