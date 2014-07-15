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
    return render_template("index.html")

@app.route('/_route')
def search_route():
    '''Search for all routes near latitute-longitude, maximum and minimum distance are optional. Distances currently in meters and  default to minimum of 1 mile (1609 meters) and 10 miles (16093 meters). '''
    lat_lng = lat_lng #add check here - request lat_long to continue if none is entered
    min_distance = request.args.get('min_distance', 1609, type=int)
    max_distnace = request.args.get('max_distance', 16093, type=int)
    routes_paginator = mmf.route.search(close_to_location=[lat_lng],
                                        minimum_distance=min_distance,
                                        maximum_distance=max_distance)
    page_range = routes_paginator.page_range
    if len(page_range) > 0:
        route_list = []
        the_page = routes_paginator.page(page_range[0])
        for route in the_page:
            route_list.append(route)
        return render_route(route_list) #add check here (if length of route_list = 0, maybe if length of route_list < 5, hollaback with a message)
    else: #add check here (if length of page_range = 0, tell the user something? the "close" in close_to_location is not specified)
        print "Warning! Page_range length is: " , page_range

def render_route(route_list):
    '''Search for a route by ID, get points as lat/lng tuples, turn into a geoJSON of lat/lng lists.'''
    i = 0
    for route[i] in route_list:
        route = mmf.route.find(route.id)
        route_points = route.points(geojson=True) #this ALMOST creates a geoJSON, requires the next 3 lines
        lat_lng_tuples = route_points['coordinates']
        lat_lng_lists = [list(point) for point in lat_lng_tuples]
        route_points['coordinates'] = lat_lng_lists
        return route_points
        #i += 1 #need to figure looping through route in response to click on "no" on map page
        
if __name__ == '__main__':
    app.run(debug=True, port=5001)

