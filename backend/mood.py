"""
Mood API
==============

This module contains the endpoints for generating and retrieving moods.
All endpoints prefixed with **/api/v1/mood** are redirected to one of these handlers.

Required Header - Authorization: Bearer *jwt*
"""
from flask import Blueprint, request, abort, jsonify, Response, g
from marshmallow import exceptions
import copy
import json
from .auth import extract_credentials
from .mood_generator import MoodGenerator, CreateOrUpdateMoodStrategy, \
		GetMoodFromDBStrategy, DeleteMoodFromDBStrategy, GetRecentMoodsFromDBStrategy

mood_api = Blueprint('mood_api', __name__)
mood_api.before_request(extract_credentials)


# Create OR update mood (PUT request)
@mood_api.route("/mood", methods=['PUT'])
def create_update_custom_mood():
	"""
		Endpoint to create or update a mood.
		
		* URI path: /api/v1/mood/mood
		* Methods: PUT
		* Required Query Params:
		
			- **name**: *String* - name of the mood
		
		* Response Body: *JSON* - object with fields
		
			- instrumentalness: *Array[float]*
			- speechiness: *Array[float]*
			- danceability: *Array[float]*
			- valence: *Array[float]*
			- energy: *Array[float]*
			- mood_id: *Integer*
	"""
	if not request.data or not request.args:
		abort(400, description="Malformed syntax")

	name = request.args.get('name') # ?name=query string
	if name is None:
		abort(422, description="Unprocessable entity: missing mood name query string")

	# Request body validation
	# Reference: https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-recommendations
	data = request.data.decode("utf8")
	generator = MoodGenerator(name, g.user_id, data, None, CreateOrUpdateMoodStrategy)
	try:
		mood = generator.generate()
	except exceptions.ValidationError as err:
		abort(422, description="Unprocessable entity: " + str(err.messages))

	data = {**mood.params, 'mood_id':mood.mood_id}

	print(data)
	return jsonify(data)

# Delete mood (DELETE request)
@mood_api.route("/mood", methods=['DELETE'])
def delete_custom_mood():
	"""
		Endpoint to delete mood by mood name.
		
		* URI path: /api/v1/mood/mood
		* Methods: DELETE
		* Required Query Params:
		
			- **name**: *String* - name of the mood
		
		* Response Body: *JSON* - object with fields (if mood was found in database, empty response otherwise)
		
			- instrumentalness: *Array[float]*
			- speechiness: *Array[float]*
			- danceability: *Array[float]*
			- valence: *Array[float]*
			- energy: *Array[float]*
			- mood_id: *Integer*
	"""
	if not request.args:
		abort(400, description="Malformed syntax")

	name = request.args.get('name') # ?name= query string
	if name is None:
		abort(422, description="Unprocessable entity: missing mood name query string")

	generator = MoodGenerator(name, g.user_id, None, None, DeleteMoodFromDBStrategy)
	mood = generator.generate()

	if not mood is None:
		data = {**mood.params, 'mood_id': mood.mood_id}
		return jsonify(data)
	return Response(status = 200)

# Read mood (GET request)
@mood_api.route("/mood", methods=['GET'])
def get_custom_mood():
	"""
		Endpoint to get mood by mood name.
		
		* URI path: /api/v1/mood/mood
		* Methods: GET
		* Required Query Params:
		
			- **name**: *String* - name of the mood
		
		* Response Body: *JSON* - object with fields
		
			- instrumentalness: *Array[float]*
			- speechiness: *Array[float]*
			- danceability: *Array[float]*
			- valence: *Array[float]*
			- energy: *Array[float]*
			- mood_id: *Integer*
	"""
	if not request.args:
		abort(400, description="Malformed syntax")

	name = request.args.get('name') # ?name= query string
	if name is None:
		abort(422, description="Unprocessable entity: missing mood name query string")

	generator = MoodGenerator(name, g.user_id, None, None, GetMoodFromDBStrategy)
	mood = generator.generate()

	if not mood is None:
		data = {**mood.params, 'mood_id': mood.mood_id}
		return jsonify(data)
	return Response(status = 404)

# Get most recent moods from other users for Explore page (GET request)
@mood_api.route("/recent-moods", methods=["GET"])
def get_explore_moods():
	"""
		Endpoint to get moods for the user to explore.
		
		* URI path: /api/v1/mood/recent-moods
		* Methods: GET
		* Required Query Params:
		
			- **name**: *String* - name of the mood
		
		* Response Body: *JSON* - list of moods, each containing mood_id, params, etc.
	"""
	generator = MoodGenerator(None, g.user_id, None, None, GetRecentMoodsFromDBStrategy)
	recent_moods = generator.generate()
	return jsonify([{**mood.params, 'mood_id': mood.mood_id, 'creator_id': mood.creator_id, 'mood_name': mood.mood_name} for mood in recent_moods])
