#!/usr/bin/env python

from flask import Flask, abort, request, render_template
import requests
import requests.auth
import os
import urllib

CLIENT_ID = os.environ['MAPMYAPI_KEY']
CLIENT_SECRET = os.environ['MAPMYAPI_SECRET']
REDIRECT_URI = u'http://localhost.mapmyapi.com:5000/callback'
print REDIRECT_URI
print urllib.quote(REDIRECT_URI.encode('utf-8'))

app = Flask(__name__, static_url_path='')

@app.route('/')
def homepage():
    access_token = {u'access_token': u'8cb56219e3b3c3e198efc452763822b33816f435', 
                    u'token_type': u'Bearer', 
                    u'expires_in': 2241332, 
                    u'scope': 
                    u'read'} # hard code access token
    if access_token:
        print "if access_token"
        return render_template('index.html')
    else:
        print "else"
        get_access_token()
        return render_template('index.html')
    
def get_access_token():
    print "IN THE get_token FUNCTION NOW"
    access_token_url = 'https://api.ua.com/v7.0/oauth2/uacf/access_token/'
    access_token_data = {'grant_type': 'client_credentials',
                         'client_id': CLIENT_ID,
                         'client_secret': CLIENT_SECRET
                        }
    print "THIS IS THE access_token_data: " , access_token_data
    response = requests.post(url=access_token_url,
                             data=access_token_data,
                             headers={'Api-Key': CLIENT_ID})
    print "THIS IS THE response: " , response # ensure response = 200

    # Inspect request details
    print response.request.headers['Content-Type']
    print response.request.body
    
    # Verify Access Token
    access_token = response.json()
    access_token
    print "THIS IS THE access_token: " , access_token
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)

