from flask import Flask, abort, request
from uuid import uuid4
import requests
import requests.auth
import urllib
import json

CLIENT_ID = "hhp3ye7mq97jnuz8rxfzwc3fz39ef3rp"
CLIENT_SECRET = "rcZHsyFknu4WA47AyDgJtagveHw479rUhnKX2qhj3dm"
REDIRECT_URI = "http://localhost.mapmyapi.com:5001/callback"

app = Flask(__name__)
@app.route('/')
def homepage():
    text = '<a href="%s">Authenticating....</a>'
    return text % make_authorization_url()

@app.route('/callback')
def callback():
    error=request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # if request was not started by me
        abort(403)
    code = request.args.get('code')
    #return "got a code! %s" % code
    return 'got an access token! %s' % get_token(code)
    

def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    from uuid import uuid4
    state = str(uuid4())
    save_created_state(state)
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "state": state,
              "redirect_uri": REDIRECT_URI,
              "duration": "temporary",
              "scope": "identity"
              }
    import urllib
    #url = "https://www.mapmyfitness.com/v7.0/oauth2/authorize/?" + urllib.urlencode(params) #original URL in this example
    url = 'https://www.mapmyfitness.com/v7.0/oauth2/authorize/?client_id=%s&response_type=code&redirect_uri=%s' % (CLIENT_ID, REDIRECT_URI) #pulled from map my run oauth 2 example
    return url

def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    print "This is client_auth: " , client_auth
    post_data = {"grant_type": "client_credentials",
                 "code": code,
                 "redirect_uri": REDIRECT_URI}
    print "This is post_data: ", post_data
    response = requests.post("https://oauth2-api.mapmyapi.com/v7.0/oauth2/access_token/",
                             auth=client_auth,
                             data=post_data)
    print "This is the response: " , response
    token_json = response.json()
    print "This is the token_json: ", token_json
    return token_json["access_token"]

#code pulled from MapMyRun oauth2 example
'''# Get an Access Token by calling the MapMyFitness access token endpoint with the Authorization Code and your application's client ID and secret
def get_token(code):
    access_token_url = 'https://oauth2-api.mapmyapi.com/v7.0/oauth2/access_token/'
    access_token_data = {'grant_type': 'authorization_code',
                         'client_id': CLIENT_ID,
                         'client_secret': client_secret,
                         'code': authorize_code}
    response = requests.post(url=access_token_url,
                             data=access_token_data,
                             headers={'Api-Key': CLIENT_ID})

    # Inspect the actual details of the request
    response.request.headers['Content-Type']
    response.request.body
    
    # Verify you have an Access Token
    access_token = response.json()
    access_token'''


# Left as an exercise to the reader.
# You may want to store valid states in a database or memcache,
# or perhaps cryptographically sign them and verify upon retrieval.
def save_created_state(state):
    pass
def is_valid_state(state):
    return True


if __name__ == '__main__':
    app.run(debug=True, port=5001)#