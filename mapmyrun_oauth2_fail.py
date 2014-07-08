# From OAuth 2.0 Tutorial on MapMyFitness GitHub @ https://gist.github.com/ThatsAMorais/e3078ed18d97c414f9d6

from __future__ import unicode_literals
import webbrowser
import urlparse
import requests
import json
from requests_oauthlib import OAuth2
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

# Specify client ID / secret for your client
client_id = 'hhp3ye7mq97jnuz8rxfzwc3fz39ef3rp'
client_secret = 'rcZHsyFknu4WA47AyDgJtagveHw479rUhnKX2qhj3dm'

# Specify the authorization and redirection URLs
redirect_uri = 'http://localhost.mapmyapi.com:5001/callback'
authorize_url = 'https://www.mapmyfitness.com/v7.0/oauth2/authorize/?client_id=%s&response_type=code&redirect_uri=%s' % (client_id, redirect_uri)

# Direct the user's browser to the authorization URL
webbrowser.open(authorize_url)

# Start an HTTP server
class AuthorizationHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.server.path = self.path
server_address = (urlparse.urlparse(redirect_uri).hostname, urlparse.urlparse(redirect_uri).port)
print "This is the server address:", server_address
#httpd = HTTPServer(server_address, AuthorizationHandler)
#httpd = HTTPServer(server_address, AuthorizationHandler)
#httpd.handle_request()

# Parse the Authorization Code from the request query string
#httpd.server_close()
#callback_url = urlparse.urlparse(httpd.path)
authorize_code = urlparse.parse_qs(callback_url.query)['code'][0]

# Verify you have an Authorization Code
authorize_code

# Get an Access Token by calling the MapMyFitness access token endpoint with the Authorization Code and your application's client ID and secret
access_token_url = 'https://oauth2-api.mapmyapi.com/v7.0/oauth2/access_token/'
access_token_data = {'grant_type': 'authorization_code', 'client_id': client_id, 'client_secret': client_secret, 'code': authorize_code}
response = requests.post(url=access_token_url, data=access_token_data, headers={'Api-Key': client_id})

# Inspect the actual details of the request
response.request.headers['Content-Type']
response.request.body

# Verify you have an Access Token
access_token = response.json()
access_token

# Sign a resource request with the user's token credentials to access resources
oauth = OAuth2(client_id=client_id, token={'token_type': 'Bearer','access_token': access_token['access_token']})
activity_type_url = 'https://oauth2-api.mapmyapi.com/v7.0/activity_type/'
response = requests.get(url=activity_type_url, auth=oauth, verify=False, headers={'Api-Key': client_id})

# Verify the response
response.status_code

# Refresh the tokens to prevent a loss of access
refresh_token_url = 'https://oauth2-api.mapmyapi.com/v7.0/oauth2/access_token/'
refresh_token_data = {'grant_type': 'refresh_token', 'client_id': client_id, 'client_secret': client_secret, 'refresh_token': access_token['refresh_token']}
response = requests.post(url=refresh_token_url, data=refresh_token_data, headers={'Api-Key': client_id})
refresh_token = response.json()
oauth = OAuth2(client_id=client_id, token={'token_type': 'Bearer','access_token': refresh_token['access_token']})
response = requests.get(url=activity_type_url, auth=oauth, verify=False, headers={'Api-Key': client_id})

# Verify the response
response.status_code