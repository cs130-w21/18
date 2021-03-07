"""
Auth API
================

This module contains the endpoints for authenticating and logging in a user.
All endpoints prefixed with **/api/v1/login** are redirected to one of these handlers.
"""

import requests
from flask import Blueprint, request, abort, Response, jsonify, url_for, redirect, g
from jwt import InvalidTokenError
import json
import os
import base64
from .utils.jwt import JWT
from datetime import datetime, timedelta
from .utils.constants import Scopes
from .utils.db import DB

auth_api = Blueprint('auth_api', __name__)
SPOTIFY_URL = 'https://accounts.spotify.com/api/token'
GRANT_TYPE = 'authorization_code'

@auth_api.route("/callback", methods=['GET'])
def get_access_token():
    """
        Callback endpoint to authenticate a user with the backend. Spotify hits
        this endpoint with an authorization code. The backend performs a back-and-forth
        with Spotify to obtain an access token, a refresh token and the user's ID and 
        display name. The browser is redirected to the URI for the front-end application
        along with authentication credentials in the query params.

        Note: This endpoint is NOT to be called by a front end application. It is only to
        be used as Spotify's callback.

        * URI path: /api/v1/login/callback
        * Methods: GET
        * Required Query Params:
        
            - **code**: *String* - Spotify authorization code
        
        * Response: Redirect to front end with query params:
            
            - jwt: *String* - jwt containing user's Spotify ID and access token
            - username: *String* - user's Spotify display name
    """
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
    #save refresh token and user_id
    with DB() as db:
        db.create_or_update_user(user_id, refresh_token)
    front_end_uri = os.environ['FRONT_END_URI']
    redirect_uri = f"{front_end_uri}/?username={display_name}&jwt={jwt}"
    return redirect(redirect_uri)

@auth_api.route("/appdetails", methods=["GET"])
def get_app_details():
    """
        Endpoint to provide app details required by front end to perform login.

        * URI path: /api/v1/login/appdetails
        * Methods: GET
        * Response Body: *JSON* - object containing
            
            - redirect_uri: *String* - absolute URI of backend.mood.get_access_token()
            - client_id: *String* - ID of application registered with Spotify
            - scopes: *String* - space separated list of Spotify access scopes
    """
    redirect_uri = os.environ['SPOTIFY_REDIRECT_URI']
    client_id = os.environ['CLIENT_ID']
    scopes = Scopes.get_all()
    data = {
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'scopes': scopes
            }
    return jsonify(data)
        
def extract_credentials():
    headers = request.headers
    if not 'Authorization' in headers:
        return jsonify({'error': 'JWT not provided'})
    auth = headers['Authorization']
    auth = auth.split(' ')
    if len(auth) < 2:
        return jsonify({'error': 'Malformed Header Syntax'})
    jwt = auth[1]
    try:
        payload = JWT.decode(jwt)
    except InvalidTokenError as e:
        return jsonify({'error': f"Invalid Token\n{str(e)}"})
    if not 'user_id' in payload or not 'access_token' in payload or not 'expires_at' in payload:
        return jsonify({'error': 'Invalid JWT payload'})
    now = datetime.timestamp(datetime.utcnow())
    expires_at = payload['expires_at']

    if now >= expires_at:
        return jsonify({'error': 'Access Token expired'})
    g.user_id = payload['user_id']
    g.access_token = payload['access_token']


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
