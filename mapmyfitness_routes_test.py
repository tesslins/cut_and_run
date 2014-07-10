#!/usr/bin/env python
from flask import Flask, abort, request, render_template
from mapmyfitness import MapMyFitness
import requests
import requests.auth

app = Flask(__name__)


mmf = MapMyFitness(api_key='hhp3ye7mq97jnuz8rxfzwc3fz39ef3rp',
                   access_token='501883a24f7f7be9fe96d9f9909776dc44a1d37c')

@app.route('/')
def homepage():
    return render_template("index.html")

#print(route.id)
#print(route.name)
#print(route.description)
#print(route.privacy)
#print(route.distance)
#print(route.ascent)
#print(route.descent)
#print(route.min_elevation)
#print(route.max_elevation)
#print(route.city)
#print(route.state)
#print(route.country)
#print(route.created_datetime)
#print(route.updated_datetime)

@app.route('/route')
def plot_route():
    route = mmf.route.find(348949363)
    route_points = route.points()
    one_point = route_points[0]
    lat = one_point.get('lat')
    lng = one_point.get('lng')
    for route in route_points:
        pass
    return render_template("index.html", lat=lat, lng=lng)
    


#routes_paginator = mmf.route.search(close_to_location=[35.555, -80.934], minimum_distance=9000, maximum_distance=11000)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

