#!/usr/bin/env python
from flask import Flask, abort, request, render_template, jsonify
from mapmyfitness import MapMyFitness
import requests
import requests.auth
import json

app = Flask(__name__, static_url_path='') #what is static_url_path ?


mmf = MapMyFitness(api_key='hhp3ye7mq97jnuz8rxfzwc3fz39ef3rp',
                   access_token='4636bdf2cb0b82b456a855808925c42b67cab7ae')
                # add cache_finds=True ?

@app.route('/')
def homepage():
    lat_lng = (37.8,-122.2) #tuple
    #lat_lng=json.dumps(lat_lng) #list (the initialize_map.js seems to require a tuple!)
    return render_template("index.html", lat_lng=lat_lng)

@app.route('/route')
def search_route():
    '''Search for all routes near latitute-longitude, maximum and minimum distance are optional. Distances currently in meters and  default to minimum of 1 mile (1609 meters) and 10 miles (16093 meters). '''
    lat_lng = lat_lng #add check here - request lat_long to continue if none is entered
    min_distance = request.args.get('min_distance', 1609, type=int)
    max_distnace = request.args.get('max_distance', 16093, type=int)
    routes_paginator = mmf.route.search(close_to_location=[lat_lng],
                                        minimum_distance=min_distance,
                                        maximum_distance=max_distance)
    page_range = routes_paginator.page_range
    route_list = []
    the_page = routes_paginator.page(page_range[0])
    for route in the_page:
        route_list.append(route)
    return route_list

def render_route(route_list):
    '''Search for a route by ID, get points as lat/lng tuples, turn into a geoJSON of lat/lng lists.'''
    i = 0
    for route[i] in route_list:
        route = mmf.route.find(route.id)
        route_points = route.points(geojson=True) #this only ALMOST creates a geoJSON, requires the next 3 lines
        lat_lng_tuples = route_points['coordinates']
        lat_lng_lists = [list(point) for point in lat_lng_tuples]
        route_points['coordinates'] = lat_lng_lists
        return route_points
        
if __name__ == '__main__':
    app.run(debug=True, port=5001)

