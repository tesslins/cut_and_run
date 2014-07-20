#!/usr/bin/env python
from flask import Flask, abort, request, render_template, jsonify
from flask.views import View
from mapmyfitness import MapMyFitness
import requests
import requests.auth
import json
import geojson


app = Flask(__name__, static_url_path='') #what is static_url_path?


mmf = MapMyFitness(api_key='hhp3ye7mq97jnuz8rxfzwc3fz39ef3rp',
                   access_token='4636bdf2cb0b82b456a855808925c42b67cab7ae')
                # add cache_finds=True ?
                
ROUTES_OBJECT = None              

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/api_call')
def call_mmf_api():
    '''Search for all routes near latitute-longitude, maximum and minimum distance are optional. Distances currently in meters and default to minimum of 1 mile (1609 meters) and 10 miles (16093 meters). Returned query is currently global variable. :('''
    print "*****search_route function******"
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    lat_lng = []
    lat_lng.append(lat)
    lat_lng.append(lng)
    min_distance = request.args.get('minDistance', 1609, type=int) 
    max_distance = request.args.get('maxDistance', 16093, type=int)
    global ROUTES_OBJECT
    ROUTES_OBJECT = mmf.route.search(close_to_location=lat_lng,
                                        minimum_distance=min_distance,
                                        maximum_distance=max_distance)
    if ROUTES_OBJECT: #improve this check
        return create_route_object()
    else:
        print "Warning! No routes returned from MapMyFitness API."
        
@app.route('/pass_index')
def pass_index():
    print "*****pass_index function******"
    ''' Retrives index from javascript for incrementing through routes.'''
    index = request.args.get('index', '0', type=str)
    print json.dumps(index)
    print type(json.dumps(index))
    return json.dumps(index)
    
@app.route('/create_route')
def create_route_object():
    print "*****create_route_object function******"
    '''Returns single route object from routes object.'''
    #figure a better way to call this so it's not just the first page? although perhaps 40 = enough?
    global ROUTES_OBJECT
    route_request = request.args.get('getroute', 'firstroute', type=str)
    page_range = ROUTES_OBJECT.page_range
    page_num = page_range[0]
    single_page = ROUTES_OBJECT.page(page_num)
    index = pass_index()
    index = json.loads(index)
    index = int(index)
    route_object = single_page[index]
    return render_route(route_object)

def render_route(route_object):
    print "*****render_route function******"
    '''Get route points as lat/lng tuples, turn into a geoJSON of lat/lng lists.'''
    route_points = route_object.points(geojson=True) #this ALMOST creates a geoJSON, requires the next 3 lines to actually get to geoJson format  
    lat_lng_tuples = route_points['coordinates']
    lat_lng_lists = [list(point) for point in lat_lng_tuples]
    route_points['coordinates'] = lat_lng_lists
    route_points_geojson = {
        "type": "FeatureCollection",
        "features": [{
        "type": "Feature",
        "geometry": {
        # route_points inserted here
        }
        }
        ]
    }
    route_points_geojson['features'][0]['geometry'] = route_points
    route_points_geojson = str(route_points_geojson)
    return geojson.dumps(route_points_geojson) #appears to be identical to normal json
    
if __name__ == '__main__':
    app.run(debug=True, port=5001)

