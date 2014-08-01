#!/usr/bin/env python
from flask import Flask, abort, request, render_template, jsonify, session, url_for
from flask.views import View
from flask.ext.sqlalchemy import SQLAlchemy
from mapmyfitness import MapMyFitness
import requests
import requests.auth
import json
import geojson
import model
import pdb #pdb.set_trace()

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
    distance are optional. Distance is input in miles with default of 5 miles.
    Min and max distance set to .5 mile on either side, then converted to
    meters.
    Object returned from API call is passed to create_route function
    for pre-processing before entry into database.'''
    print "*****get_routes function******"
    lat = request.args.get('lat') # lat comes in as type: unicode
    lng = request.args.get('lng') # lng comes in as type: unicode
    lat_lng = []
    lat_lng.append(lat)
    lat_lng.append(lng)
    conversion = 1609.34 # convert miles to meters
    distance = (request.args.get('distance', 5, type=int))
    min_distance = (distance - .5) * conversion
    max_distance = (distance + .5) * conversion
    pdb.set_trace()
    routes_object = mapmyfitness.route.search(close_to_location=lat_lng,
                                        minimum_distance=min_distance,
                                        maximum_distance=max_distance)
    if routes_object: # and hasattr(routes_object, 'page_range')
        print "MapMyFitness API call made."
        return create_route(routes_object, lat, lng)
    else:
        print "Warning! No routes returned from MapMyFitness API."

def create_route(routes_object, lat, lng):
    '''Add and commit routes as database rows.'''
    print "*****create_route_object function******"
    route_ids = [] #send to javascript for database queries
    total_count = routes_object.count
    page_range = routes_object.page_range
    single_page = page_range[0]
    the_page = routes_object.page(single_page)
    for route in the_page:
        # add route to database here! just using first page (max 40) for now.
        # !! weird bug with moving on to second page !!
        if route.id:
            route_id = route.id # <type 'int'>
            route_ids.append(route_id)
        search_lat = lat
        search_lng = lng
        if route.name:
            name = route.name # <type 'unicode'>
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
        start_lat = lat_lng_lists[0][0]
        start_lng = lat_lng_lists[0][-1]
        end_lat = lat_lng_lists[-1][0]
        end_lng = lat_lng_lists[-1][-1]
        # !! need to write check if start == end, it is a loop
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
        # !! json vs geojson for dump?..same result I believe !!
        route_points_geojson = geojson.dumps(route_points_geojson,
                                             ensure_ascii=False)
        route = model.Route(route_id, search_lat, search_lng, name,
                           distance, ascent, descent, min_elevation,
                           max_elevation, city, state, route_points_geojson,
                           start_lat, start_lng, end_lat, end_lng)
        # !! add a check to make sure route_id is not already in db !!
        model.session.add(route)
        print "route added to session"
        model.session.commit()
        print "route committed"
    return json.dumps(route_ids)

@app.route('/route/<route_id>')
def query_db(route_id):
    '''Query database by route_id to get geoJSON to URL.'''
    route_id = int(route_id)
    r = model.session.query(model.Route).filter_by(route_id = route_id).first()
    return r.route_points_geojson

@app.route('/markers')
def query_db_markers():
    '''Query database by route_id to get latitude and longitudes for start and
    end markers.'''
    route_id = request.args.get('route_id')
    r = model.session.query(model.Route).filter_by(route_id = route_id).first()
    points = {}
    points["start_lat"] = r.start_lat
    points["start_lng"] = r.start_lng
    points["end_lat"] = r.end_lat
    points["end_lng"] = r.end_lng
    return json.dumps(points)
    
        
if __name__ == '__main__':
    app.run(debug=True, port=5001)

