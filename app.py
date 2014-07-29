#!/usr/bin/env python
from flask import Flask, abort, request, render_template, jsonify,  session
from flask.views import View
from flask.ext.sqlalchemy import SQLAlchemy
from mapmyfitness import MapMyFitness
import requests
import requests.auth
import json
import model

app = Flask(__name__, static_url_path='')

mapmyfitness = MapMyFitness(api_key='hhp3ye7mq97jnuz8rxfzwc3fz39ef3rp',
                    access_token='4636bdf2cb0b82b456a855808925c42b67cab7ae')
                    # add cache_finds=True ?
                
@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/api')
def get_routes():
    '''Search for all routes near latitute-longitude, maximum and minimum
    distance are optional. Distances currently input in miles and default to
    minimum of 1 mile (1609 meters) and 10 miles (16093 meters) and are
    converted to meters. Object returned from API call is directly entered
    into database table, post-processed data is also entered in seperate table.
    '''
    print "*****get_routes function******"
    lat = request.args.get('lat') # lat comes in as type: unicode
    lng = request.args.get('lng') # lng comes in as type: unicode
    lat_lng = []
    lat_lng.append(lat)
    lat_lng.append(lng)
    min_distance = (request.args.get('minDistance', 1, type=int)) * 1609.34
    max_distance = (request.args.get('maxDistance', 10, type=int)) * 1609.34
    routes_object = mapmyfitness.route.search(close_to_location=lat_lng,
                                        minimum_distance=min_distance,
                                        maximum_distance=max_distance)
    if routes_object: # and hasattr(routes_object, 'page_range')
        print "MapMyFitness API call made."
        create_route_object(routes_object, lat, lng)
        return "Carry on javascript!"
    else:
        print "Warning! No routes returned from MapMyFitness API."

def create_route_object(routes_object, lat, lng):
    '''Creates single route objects, pulls route_id and route_geojson.'''
    print "*****create_route_object function******"
    total_count = routes_object.count
    page_range = routes_object.page_range
    single_page = page_range[0]
    the_page = routes_object.page(single_page)
    for route in the_page:
        # add route to database here! just using first page (max 40) for now.
        # !! weird bug with moving on to second page !!
        if route.id:
            route_id = route.id # <type 'int'>
        search_lat = lat
        search_lng = lng
        if route.name:
            name = route.name # <type 'unicode'>
        if route.description:
            description = route.description # <type 'unicode'>
        if route.distance:
            distance = route.distance # <type 'float'>
        if route.ascent:
            ascent = route.ascent # <type 'float'>
        if route.descent:
            descent = route.descent # <type 'float'>
        if route.min_elevation:
            min_elevation = route.min_elevation # <type 'float'>
        if route.max_elevation:
            max_elevation = route.max_elevation # <type 'float'>
        if route.city:
            city = route.city # <type 'unicode'>
        if route.state:
            state = route.state # <type 'unicode'>
        route_points = route.points(geojson=True)
        # previous line ALMOST creates a geoJSON, requires the next 3 lines
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
                            }]
                            }
        route_points_geojson['features'][0]['geometry'] = route_points
        
        route = model.Route(route_id, search_lat, search_lng, name, description,
                           distance, ascent, descent, min_elevation,
                           max_elevation, city, state)
        model.session.add(route)
        model.session.commit()
        
if __name__ == '__main__':
    app.run(debug=True, port=5001)

