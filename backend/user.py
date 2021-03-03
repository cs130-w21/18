from flask import Blueprint, request, g, abort, jsonify, Response
from .utils.db import DB
from .auth import extract_credentials

user_api = Blueprint('user_api', __name__)
user_api.before_request(extract_credentials)

@user_api.route("/moods", methods=['GET'])
def get_user_moods():
    moods = None
    with DB() as db:
        moods = db.get_user_moods(g.user_id)
    if moods is None:
        abort(500, "Could not retrive user's moods")
    return jsonify(moods)

@user_api.route("/external_mood", methods=['PUT'])
def add_external_mood():
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

