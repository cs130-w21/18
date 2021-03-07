"""
User API
=======================

This module contains the endpoints to user data such as moods and playlists of a user.
All endpoints prefixed with **/api/v1/user** are redirected to one of these handlers.

Required Header - Authorization: Bearer *jwt*
"""
from flask import Blueprint, request, g, abort, jsonify, Response
from .utils.db import DB
from .auth import extract_credentials

user_api = Blueprint('user_api', __name__)
user_api.before_request(extract_credentials)

@user_api.route("/moods", methods=['GET'])
def get_user_moods():
    """
        Endpoint to get a list of moods either created or liked by the user. 

        * URI path: /api/v1/user/moods
        * Methods: GET
        * Response: *JSON* - object containing

            - created_moods: *JSON* - list of mood objects (see next item for schema)
            - external_moods: *JSON* - list of mood objects, each containing

                + mood_id: *String* - ID of mood
                + mood_name: *String* - name of mood
                + params: *JSON* - parameters of mood (danceability, speechiness, instrumentalness, valence, energy)
    """
    moods = None
    with DB() as db:
        moods = db.get_user_moods(g.user_id)
    if moods is None:
        abort(500, "Could not retrive user's moods")
    return jsonify(moods)

@user_api.route("/external_mood", methods=['PUT'])
def add_external_mood():
    """
        Endpoint to add a mood not created by the user to their account. 

        * URI path: /api/v1/user/external_mood
        * Methods: PUT
        * Required Query Params:
            
            - mood_id: *Integer* - ID of mood to be added

        * Response: *empty*
    """
    if not request.args:
        abort(400, description="Malformed Syntax")
    mood_id = request.args.get('mood_id') #?mood_id=query string
    if mood_id is None:
        abort(422, description="Unprocessable entity: missing mood id query string")

    try:
        mood_id = int(mood_id)
    except:
        abort(422, description="Unprocessable entity: invalid mood id")

    with DB() as db:
        try:
            db.add_mood_for_user(g.user_id, mood_id, is_external=True)
        except:
            abort(500, "Could not add mood to user's list of moods")
    return Response(status=200)

