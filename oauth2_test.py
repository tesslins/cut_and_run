# mapmyfitness oauth2 client credential example
# from https://github.com/fdac/MapMyFitness/blob/master/authorize_examples/oauth_demo_client_credential.py

import logging
import os
import sys
import urlparse
import webbrowser
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import requests
import json

logging.basicConfig(level=logging.DEBUG)

# Store your client ID and secret in your OS's environment using these keys, or
# redefine these values here.
#CLIENT_ID = os.environ.get('MMF_CLIENT_ID')
#CLIENT_SECRET = os.environ.get('MMF_CLIENT_SECRET')
CLIENT_ID = os.environ['MAPMYAPI_KEY']
CLIENT_SECRET = os.environ['MAPMYAPI_SECRET']
print CLIENT_ID
print CLIENT_SECRET

if CLIENT_ID is None or CLIENT_SECRET is None:
    print 'Please ensure $MMF_CLIENT_ID and #MMF_CLIENT_SECRET environment variables are set.'
    exit()

# As a convenience, localhost.mapmyapi.com redirects to localhost.
redirect_uri = 'http://localhost.mapmyapi.com:5000/callback'
authorize_url = 'https://www.mapmyfitness.com/v7.0/oauth2/authorize/?' \
                'client_id={0}&response_type=code&redirect_uri={1}'.format(CLIENT_ID, redirect_uri)


# Set up a basic handler for the redirect issued by the mapmyfitness
# authorize page. For any GET request, it simply returns a 200.
# When run interactively, the request's URL will be printed out
class AuthorizationHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.server.path = self.path


parsed_redirect_uri = urlparse.urlparse(redirect_uri)
server_address = parsed_redirect_uri.hostname, parsed_redirect_uri.port

print 'server_address:', server_address

# NOTE: Don't go to the web browser just yet...
# webbrowser.open(authorize_url)

# Start our web server, handle_request() will block until a request comes in.
# httpd = HTTPServer(server_address, AuthorizationHandler)
# print 'Now waiting for the user to authorize the application...'
# httpd.handle_request()

# At this point a request has been handled. Let's parse its URL.
# httpd.server_close()
# callback_url = urlparse.urlparse(httpd.path)
# authorize_code = urlparse.parse_qs(callback_url.query)['code'][0]
# authorize_code = '0f7604e92b92e1d437b8ff8b65e3b750aa191ff4'

# print 'Got an authorize code:', authorize_code

access_token_url = 'https://api.mapmyfitness.com/v7.0/oauth2/access_token/'
# access_token_data = {'grant_type': 'authorization_code',
                     # 'client_id': CLIENT_ID,
                     # 'client_secret': CLIENT_SECRET,
                     # 'code': authorize_code}

access_token_data = {'grant_type': 'client_credentials',
                     'client_id': CLIENT_ID,
                     'client_secret': CLIENT_SECRET}

response = requests.post(url=access_token_url,
                         data=access_token_data,
                         headers={'Api-Key': CLIENT_ID})

print 'Request details:'
print 'Content-Type:', response.request.headers['Content-Type']
print 'Request body:', response.request.body

# retrieve the access_token from the response
try:
    access_token = response.json()
    print 'Got an access token:', access_token
except:
    print 'Did not get JSON. Here is the response and content:'
    print response
    print response.content

# Use the access token to request a resource on behalf of the user
#activity_type_url = 'https://oauth2-api.mapmyapi.com/v7.0/activity_type/'
activity_type_url = 'https://oauth2-api.mapmyapi.com/v7.1/route/?close_to_location=30.2688%2C-97.7489&maximum_distance=5000&minimum_distance=1'
response = requests.get(url=activity_type_url, verify=False,
                        headers={'api-key': CLIENT_ID, 'authorization': 'Bearer %s' % access_token['access_token']})

print 'Made API Call:'
#print response.json()
retVal = response.json()
print json.dumps(retVal, sort_keys=False, indent=4, separators=(',',';'))

# Refresh a client's credentials to prevent expiration
# refresh_token_url = 'https://oauth2-api.mapmyapi.com/v7.0/oauth2/access_token/'
# refresh_token_data = {'grant_type': 'refresh_token',
                      # 'client_id': CLIENT_ID,
                      # 'client_secret': CLIENT_SECRET,
                      # 'refresh_token': access_token['refresh_token']}

# response = requests.post(url=refresh_token_url, data = refresh_token_data,
                         # headers={'api-key': CLIENT_ID, 'authorization': 'Bearer %s' % access_token['access_token']})

# print 'Request details:'
# print 'Content-Type:', response.request.headers['Content-Type']
# print 'Request body:', response.request.body

# try:
    # access_token = response.json()
    # print 'Got an access token:', access_token
# except:
    # print 'Did not get JSON. Here is the response and content:'
    # print response
    # print response.content

# Attempt another request on the user's behalf using the token
refresh_token = response.json()
response = requests.get(url=activity_type_url, verify=False,
                        headers={'api-key': CLIENT_ID, 'authorization': 'Bearer %s' % access_token['access_token']})





