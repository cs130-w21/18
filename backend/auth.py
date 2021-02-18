import requests
from flask import Blueprint, request, abort, Response, jsonify, url_for, redirect
import json
import os
import base64
from .utils.jwt import JWT
from datetime import datetime, timedelta
from .utils.constants import Scopes

auth_api = Blueprint('auth_api', __name__)
SPOTIFY_URL = 'https://accounts.spotify.com/api/token'
GRANT_TYPE = 'authorization_code'
refresh_token_cache = {}

@auth_api.route("/callback", methods=['GET'])
def get_access_token():
    if not request.args:
        print("No args provided")
        abort(400, description="Malformed syntax")
    #send code to Spotify
    code = request.args.get('code')
    data = {
        'code': code, 
        'grant_type': GRANT_TYPE, 
        'redirect_uri': os.environ['SPOTIFY_REDIRECT_URI']
    }
    headers = create_headers_for_spotify_auth()
    resp = requests.post(SPOTIFY_URL, data=data, headers=headers)
    #get data from Spotify response
    if resp.status_code != 200:
        print(resp.text)
        abort(500, "Error in retreiving access token")
    resp_json = resp.json()
    access_token = resp_json['access_token']
    refresh_token = resp_json['refresh_token']
    expires_in = resp_json['expires_in']
    #get user info from Spotify
    headers = {
            'Authorization': f"Bearer {access_token}"
            }
    resp = requests.get('https://api.spotify.com/v1/me', headers=headers)
    #prepare jwt
    if resp.status_code != 200:
        print(resp.text)
        abort(500, "Error in retrieving user name")
    resp_json = resp.json()
    display_name = resp_json['display_name']
    uri = resp_json['uri']
    user_id = uri.split(':')[2]
    jwt = create_jwt(access_token, user_id, expires_in)
    #save refresh token TODO: persist in DB
    refresh_token_cache[user_id] = refresh_token
    front_end_uri = os.environ['FRONT_END_URI']
    redirect_uri = f"{front_end_uri}/?username={display_name}&jwt={jwt}"
    return redirect(redirect_uri)

@auth_api.route("/appdetails", methods=["GET"])
def get_app_details():
    redirect_uri = os.environ['SPOTIFY_REDIRECT_URI']
    client_id = os.environ['CLIENT_ID']
    scopes = Scopes.get_all()
    data = {
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'scopes': scopes
            }
    return jsonify(data)
        

def create_jwt(access_token, user_id, expires_in):
    expiration = datetime.utcnow() + timedelta(seconds=expires_in - 120)
    payload = {
            'access_token': access_token,
            'expires_at': datetime.timestamp(expiration),
            'user_id': user_id
            }
    return JWT.encode(payload)

def create_headers_for_spotify_auth():
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    encoded = f"{client_id}:{client_secret}".encode('ascii')
    encoded = base64.b64encode(encoded).decode('ascii')
    headers = {'Authorization': f"Basic {encoded}"}
    return headers
