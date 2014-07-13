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
    lat_lng = (39.7392,-104.9847) #tuple
    #lat_lng=json.dumps(lat_lng) #list (the initialize_map.js seems to require a tuple!)
    return render_template("index_v2.html", lat_lng=lat_lng)

@app.route('/route')
def plot_route():
    '''Search for a route by ID, get points as lat/lng tuples, turn into a geoJSON of lat/lng lists.'''
    route = mmf.route.find(348949363) 
    route_points = route.points(geojson=True) #this does not actually create a geoJSON...booo
    lat_lng_tuples = route_points['coordinates'] 
    lat_lng_lists = [list(point) for point in lat_lng_tuples] 
    route_points['coordinates'] = lat_lng_lists
    return render_template("route.html", route_points=route_points)

#@app.route('/route_search')
#def search_route(lat_lng):
#    '''Search for all routes near latitute-longitude. The close_to_location search query does not work, why???? Pls help me Jason Sanford!'''
#    routes_paginator = mmf.route.search(close_to_location=[lat_lng])
#    return render_template("index_v2.html")

if __name__ == '__main__':
    app.run(debug=True, port=5001)

