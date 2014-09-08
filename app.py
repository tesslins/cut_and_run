#!/usr/bin/env python
from flask import Flask, abort, request, render_template, jsonify, session
from flask import url_for, flash
from flask.views import View
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mobility import Mobility
from flask.ext.mobility.decorators import mobile_template
from geoalchemy2.elements import WKTElement
from mapmyfitness import MapMyFitness
import requests
import requests.auth
import json
import geojson
import os
import model
import pdb #call with pdb.set_trace()

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') else 'postgresql+psycopg2://localhost'

Mobility(app)

mapmyfitness = MapMyFitness(api_key='hhp3ye7mq97jnuz8rxfzwc3fz39ef3rp',
                    access_token='038d9fcf6684536df308f074d8b8bcba7ee574f9')
                
@app.route('/')
@mobile_template('{mobile/}index.html')
def homepage(template): 
    return render_template(template)

@app.route('/api')
def get_routes():
    '''MapMyFitness query for routes near latitute-longitude, maximum and
    minimum distance are optional. Distance is input in miles. Min and max
    distance set to +/-.5 mile, then converted to meters.
    Object returned from API call is passed to create_route function
    for processing route data before entry into database.'''
    lat = request.args.get('lat') # lat comes in as type: unicode
    lng = request.args.get('lng') # lng comes in as type: unicode
    if not lat:
        print "Valid location not passed (latitude)."
    elif not lng:
        print "Valid location not passed (longitude)."
    else:
        lat_lng = []
        lat_lng.append(lat)
        lat_lng.append(lng)
        conversion = 1609.34 # convert miles to meters
        distance = (request.args.get('distance', 5, type=int)) #5 = default
        if not distance:
            print "Valid distance not passed."
        else:
            min_distance = (distance - .5) * conversion
            max_distance = (distance + .5) * conversion
            # !! add close_to_location database query before API call !!
            routes_object = mapmyfitness.route.search(close_to_location=lat_lng,
                                                minimum_distance=min_distance,
                                                maximum_distance=max_distance)
            if routes_object:
                print routes_object
                print "MapMyFitness API call made."
                return create_route(routes_object)
            else:
                print "No routes returned from MapMyFitness API call."

def create_route(routes_object):
    '''Add and commit routes as database rows.'''
    print "in create_routes"
    route_ids = [] #used to send to javascript for database queries
    total_count = routes_object.count
    if total_count == 0:
        print "No routes returned from search."
        #return error message to user
    elif total_count <10:
        print "%d routes returned." % (total_count)
        #return non-error message to user
    page_range = routes_object.page_range
    single_page = page_range[0]
    the_page = routes_object.page(single_page)
    for route in the_page:
        # adding first page (maximum 40 routes) for now.
        # !! fix bug with moving on to second page !!
        if route.id:
            route_id = route.id # <type 'int'>
            route_ids.append(route_id)
            if not model.session.query(model.Route).filter_by(route_id=route_id).count():
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
                if route.points:
                    route_points = route.points(geojson=True)
                    # previous line ALMOST creates a geoJSON, requires next 3 lines
                    lat_lng_tuples = route_points['coordinates']
                    lat_lng_lists = [list(point) for point in lat_lng_tuples]
                    route_points['coordinates'] = lat_lng_lists
                    start_lng = lat_lng_lists[0][-1]
                    start_lat = lat_lng_lists[0][0]
                    end_lng = lat_lng_lists[-1][-1]
                    end_lat = lat_lng_lists[-1][0]
                    start_point = WKTElement('POINT({0} {1})'.format(start_lng, start_lat),
                                            srid=4326)
                    end_point = WKTElement('POINT({0} {1})'.format(end_lng, end_lat),
                                        srid=4326)
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
                    route_points_geojson = geojson.dumps(route_points_geojson,
                                                         ensure_ascii=False)
                # ?? more elegant way to do the following if ??
                # perhaps check that there are 16 attributes of route
                route = model.Route(route_id, name, distance, ascent, descent,
                                    min_elevation, max_elevation, city, state,
                                    start_lng, start_lat, end_lng, end_lat,
                                    start_point, end_point,
                                    route_points_geojson)

                model.session.add(route)
                model.session.commit()
    return json.dumps(route_ids)

@app.route('/route/<route_id>')
def query_db(route_id):
    '''Query database by route_id to return route geoJSON to URL.'''
    route_id = int(route_id)
    r = model.session.query(model.Route).filter_by(route_id = route_id).first()
    print r.distance
    if r:
        return r.route_points_geojson
    else:
        print "No route found in database with route id %d." % (route_id)

@app.route('/markers')
def query_db_markers():
    '''Query database by route_id to get latitude and longitude for start and
    end markers.'''
    route_id = request.args.get('route_id')
    r = model.session.query(model.Route).filter_by(route_id = route_id).first()
    if r:
        points = {}
        points["start_lng"] = float(r.start_lng)
        points["start_lat"] = float(r.start_lat)
        points["end_lng"] = float(r.end_lng)
        points["end_lat"] = float(r.end_lat)
        return json.dumps(points)
    else:
        print "No route found in database with id %d." % (route_id)
    
        
if __name__ == '__main__':
    session = model.session
    app.run(debug=True, port=5000)

