#!/usr/bin/env python
from flask import Flask, request, render_template, session
from flask.ext.mobility import Mobility
from flask.ext.mobility.decorators import mobile_template
import requests
import requests.auth
import json
import geojson
import os
import pdb #call with pdb.set_trace()

# App info
app = Flask(__name__, static_url_path='')
Mobility(app)

# API key
# Under Armour calls this Client ID
MAPMYAPI_KEY = '62xb5fhesk3gb3fj3yttw2mh4yn54krt'
# Under Armour calls this Client Secret
MAPMYAPI_SECRET = 'JJYKeRZXEFvvQ8uTzCrZCQjkwqv6TuphxFHmjcsBwu4'

access_token = {u'access_token': u'a26d95f8560d358f3c2dd39dff7a2d27eb29f50e', 
                u'token_type': u'Bearer', 
                u'expires_in': 2148789, 
                u'scope': u'read'}

# Routes
@app.route('/')
# messing around with adaptive mobile template           
@mobile_template('{mobile/}index.html')
def homepage(template): 
    return render_template("index.html")

@app.route('/api')
def get_routes():
    '''UnderArmor (previously MapMyFitness) query for routes near location with 
    parameters of location (input is zipcode) and distance (input is single 
    distance, in miles). Minimum and maximum distance are set to +/-.5 mile of 
    input distance, then converted to meters. API call returns json, which is 
    passed to create_route function for processing route data before entry into 
    database.'''
    lat = request.args.get('lat') # lat comes in as type: unicode
    lng = request.args.get('lng') # lng comes in as type: unicode
    if not lat:
        print "Valid location not passed (latitude)."
    elif not lng:
        print "Valid location not passed (longitude)."
    else:
        # create single lat_lng variable for future use with 
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
            # to do: add close_to_location database query before API call
            # min_distance and max_distance to str
            mapmyapi_url = 'https://oauth2-api.mapmyapi.com/v7.1/route/?close_to_location=' + lat + '%2C' + lng + '&maximum_distance=' + str(max_distance) + '&minimum_distance=' + str(min_distance)
            response = requests.get(url=mapmyapi_url, verify=False,
                        headers={'api-key': MAPMYAPI_KEY, 'authorization': 'Bearer %s' % access_token['access_token']})
            print 'Made close-to-location API Call.'
            retVal = response.json()
            routes_json = json.dumps(retVal, sort_keys=False, indent=4, separators=(',',':'))
            return create_route_ids_list(routes_json)

def create_route_ids_list(routes_json):
    '''Add and commit routes as database rows.'''
    print "in create_routes"
    route_ids = [] #used to send to javascript for database queries
    route_dict = json.loads(routes_json)
    route_list = route_dict['_embedded']['routes']

    ''' Ensure the initial search returned routes. '''
    if len(route_list) == 0:
        print "No routes returned from search."
        #to do: return error message to user
    elif len(route_list) <10:
        print "%d routes returned." % (len(route_list))
        #to do: return non-error message to user
    else:
        print "%d routes returned." % (len(route_list))

    for route in route_list:
        route_id = route['_links']['self'][0]['id'] # <type 'unicode'>
        route_ids.append(route_id)

    # returns route_ids as object to js
    return json.dumps(route_ids)

@app.route('/markers')
def get_route_points():
    ''' Second API call to get points for each route and convert to geojson. '''
    route = request.args.get('route_id')
    print route
    print type(route)
    # format can be json, gpx, or kml
    mapmyapi_url = 'https://oauth2-api.mapmyapi.com/v7.1/route/' + route + '/?field_set=detailed&format=json'
    response = requests.get(url=mapmyapi_url, verify=False,
                    headers={'api-key': MAPMYAPI_KEY, 'authorization': 'Bearer %s' % access_token['access_token']})
    print 'Made single route id API call.'
    route_data = response.json()
    return json.dumps(route_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

