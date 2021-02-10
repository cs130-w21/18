from flask import Blueprint, request, abort, jsonify, Response
# TODO: add marshmallow to requirements file
from marshmallow import Schema, fields, validate, exceptions
import copy
import json

mood_api = Blueprint('mood_api', __name__)

# TODO: use non-volatile memory to preserve moods even if server crashes
mood_cache = {}

# (Create or Update) Mood Schema
class CreateUpdateMood(Schema):
	seed_artists = fields.List(fields.String(), required=True, validate=validate.Length(min=1))
	seed_genres = fields.List(fields.String(), required=True, validate=validate.Length(min=1))
	seed_tracks = fields.List(fields.String(), required=True, validate=validate.Length(min=1))

	# each is num list [min, max, target]
	# TODO: check if min < target < max
	danceability = fields.List(fields.Number(), required=False, validate=validate.Length(equal=3))
	instrumentalness = fields.List(fields.Number(), required=False, validate=validate.Length(equal=3))
	popularity = fields.List(fields.Number(), required=False, validate=validate.Length(equal=3))
	speechiness = fields.List(fields.Number(), required=False, validate=validate.Length(equal=3))
	valence = fields.List(fields.Number(), required=False, validate=validate.Length(equal=3))
	energy = fields.List(fields.Number(), required=False, validate=validate.Length(equal=3))

# Create OR update mood (PUT request)
@mood_api.route("/<user>/mood", methods=['PUT'])
def create_update_custom_mood(user):
	if not request.data or not request.args:
		abort(400, description="Malformed syntax")

	name = request.args.get('name') # ?name=query string
	if name is None:
		abort(422, description="Unprocessable entity: missing mood name query string")

	# Request body validation
	# Reference: https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-recommendations
	try:
		data = CreateUpdateMood().loads(request.data.decode("utf8"))
	except exceptions.ValidationError as err:
		abort(422, description="Unprocessable entity: " + str(err.messages))

	if user not in mood_cache:
		mood_cache[user] = {}
	mood_cache[user][name] = data

	print(data)
	return jsonify(data)

# Delete mood (DELETE request)
@mood_api.route("/<user>/mood", methods=['DELETE'])
def delete_custom_mood(user):
	if not request.args:
		abort(400, description="Malformed syntax")

	name = request.args.get('name') # ?name= query string
	if name is None:
		abort(422, description="Unprocessable entity: missing mood name query string")

	# Don't bother checking if mood actually exists
	# Only need to delete if it exists
	if user in mood_cache and name in mood_cache[user]:
		mood_to_del = copy.deepcopy(mood_cache[user][name])
		del mood_cache[user][name]
		return jsonify(mood_to_del)
	return Response(status = 200)

# Read mood (GET request)
@mood_api.route("/<user>/mood", methods=['GET'])
def get_custom_mood(user):
	if not request.args:
		abort(400, description="Malformed syntax")

	name = request.args.get('name') # ?name= query string
	if name is None:
		abort(422, description="Unprocessable entity: missing mood name query string")

	if user in mood_cache and name in mood_cache[user]:
		return jsonify(mood_cache[user][name])
	return Response(status = 404)
