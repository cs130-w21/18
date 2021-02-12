import requests
from flask import Blueprint, request, abort, Response, jsonify
import json
import os
import base64
from .utils.jwt import JWT
from datetime import datetime, timedelta

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
    resp = requests.post(SPOTIFY_URL, data=data, headers=headers)
    if resp.status_code == 200:
        jwt = create_jwt(resp)
        return jsonify({'jwt':jwt})
    else:
        print(resp.text)
        abort(500, "Error in retreiving access token")

def create_jwt(spotify_resp):
    spotify_json = spotify_resp.json()
    expiration = datetime.utcnow() + timedelta(seconds=spotify_json['expires_in'] - 120)
    payload = {
            'access_token': spotify_json['access_token'],
            'expires_at': datetime.timestamp(expiration)
            }
    return JWT.encode(payload)

def create_headers_for_spotify_auth():
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    encoded = f"{client_id}:{client_secret}".encode('ascii')
    encoded = base64.b64encode(encoded).decode('ascii')
    headers = {'Authorization': f"Basic {encoded}"}
    return headers

