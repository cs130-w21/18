import requests
from flask import Blueprint, request, abort, Response, jsonify
import json
import os
import base64

auth_api = Blueprint('auth_api', __name__)
SPOTIFY_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI = 'https://musaic-13018.herokuapp.com/login/callback'
GRANT_TYPE = 'authorization_code'
refresh_token_cache = {}

@auth_api.route("/callback", methods=['GET'])
def get_access_token():
    if not request.args:
        print("No args provided")
        abort(400, description="Malformed syntax")
    code = request.args.get('code')
    data = {
        'code': code, 
        'grant_type': GRANT_TYPE, 
        'redirect_uri': REDIRECT_URI
    }
    headers = create_headers_for_spotify_auth()
    resp = requests.post(url, data=data, headers=headers)
    if resp.status_code == 200:
        return jsonify(resp.json())
    else:
        print(resp.text)
        abort(500, "Error in retreiving access token")

def create_headers_for_spotify_auth():
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    encoded = f"{client_id}:{client_secret}".encode('ascii')
    encoded = base64.b64encode(encoded).decode('ascii')
    headers = {'Authorization': f"Basic {encoded}"}
    return headers

