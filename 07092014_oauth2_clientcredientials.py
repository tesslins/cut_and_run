#!/usr/bin/env python

from flask import Flask, abort, request, render_template
import requests
import requests.auth

CLIENT_ID = "hhp3ye7mq97jnuz8rxfzwc3fz39ef3rp"
CLIENT_SECRET = "rcZHsyFknu4WA47AyDgJtagveHw479rUhnKX2qhj3dm"
REDIRECT_URI = "http://localhost.mapmyapi.com:5001/callback"

app = Flask(__name__)

@app.route('/')
def homepage():
    access_token = {u'access_token': u'501883a24f7f7be9fe96d9f9909776dc44a1d37c',
                    u'token_type': u'Bearer',
                    u'expires_in': 5182593,
                    u'scope': u'read'} #hard code access_token in for now
    if access_token:
        return render_template("index.html")
    else:
        make_authorization_url()
        return render_template("index.html")


@app.route('/callback')
def callback():
    print "IN THE CALLBACK FUNCTION"
    code = request.args.get('code')
    print "THIS IS THE code: " , code
    #return "got a code! %s" % code
    return 'got an access token! %s' % get_token(code)

def make_authorization_url():
    print "IN MAKE_ATHORIZATION_URL FUNCTION"    
    url = 'https://www.mapmyfitness.com/v7.0/oauth2/authorize/?client_id=%s&response_type=code&redirect_uri=%s' % (CLIENT_ID, REDIRECT_URI)
    print "THIS IS THE url: " , url
    return url
    
def get_token(code):
    print "IN THE GET_TOKEN FUNCTION NOW"
    access_token_url = 'https://oauth2-api.mapmyapi.com/v7.0/oauth2/access_token/'
    access_token_data = {'grant_type': 'client_credentials',
                         'client_id': CLIENT_ID,
                         'client_secret': CLIENT_SECRET,
                         'code': code}
    print "THIS IS THE access_token_data: " , access_token_data
    response = requests.post(url=access_token_url,
                             data=access_token_data,
                             headers={'Api-Key': CLIENT_ID}) #response is 200
    print "THIS IS THE response: " , response

    # Inspect the actual details of the request
    response.request.headers['Content-Type']
    response.request.body
    
    # Verify you have an Access Token
    access_token = response.json()
    access_token
    print "THIS IS THE access_token: " , access_token

    
if __name__ == '__main__':
    app.run(debug=True, port=5001)

