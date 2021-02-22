import requests
from enum import Enum
from flask import Blueprint

class Constants(Enum):
	LIMIT = '10'
	MARKET = 'US'
	OFFSET = '0'

	SPOTIFY_SEARCH = 'https://api.spotify.com/v1/search'
	SPOTIFY_RECOMMENDATIONS = 'https://api.spotify.com/v1/recommendations'

spotify_api = Blueprint('spotify_api', __name__)

# Reference: https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-recommendations
def get_tracks(mood, authorization, **kwargs):
	get_args = {}
	if 'limit' not in kwargs:
		get_args['limit'] = Constants.LIMIT
	if 'market' not in kwargs:
		get_args['market'] = Constants.MARKET
	for k, v in mood.items():
		# separate Spotify parameters
		if 'seed' not in k:
			get_args['min_' + k] = v[0]
			get_args['max_' + k] = v[1]
			get_args['target_' + k] = v[2]
		else:	# seed parameters
			get_args[k] = v

	# TODO: default values for seeds
	# References: https://developer.spotify.com/console/get-current-user-top-artists-and-tracks/?type=artists,,
	# https://developer.spotify.com/console/get-available-genre-seeds/

	# TODO: how to get OAuth access token?
	oauth_access_token = ''
	headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + oauth_access_token}

	return requests.get(Constants.SPOTIFY_RECOMMENDATIONS, params=get_args, headers=headers).json()

# Reference: https://developer.spotify.com/documentation/web-api/reference/#endpoint-search
@spotify_api.route("/search", methods=['GET'])
def get_spotify_id():
	if not request.args:
		abort(400, description="Malformed syntax")

	if request.args.get('query') is None: # ?query = query string
		abort(422, description="Unprocessable entity: missing query")

	if request.args.get('type') is None: # ?type = query string (artist, genre, or track)
		abort(422, description="Unprocessable entity: missing query type")

	get_args = {}
	if 'limit' not in request.args:
		get_args['limit'] = Constants.LIMIT
	if 'market' not in request.args:
		get_args['market'] = Constants.MARKET
	if 'offset' not in request.args:
		get_args['offset'] = Constants.OFFSET
	for k, v in request.args.items():
		get_args[k] = v

	# TODO: how to get OAuth access token?
	oauth_access_token = ''
	headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + oauth_access_token}

	return requests.get(Constants.SPOTIFY_SEARCH, params=get_args, headers=headers).json()

