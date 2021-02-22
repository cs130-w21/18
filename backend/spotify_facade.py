import requests
from enum import Enum
from flask import Blueprint, g
from .auth import extract_credentials
from .mood_generator import MoodGenerator, CreateOrUpdateMoodStrategy, \
		GetMoodFromDBStrategy, DeleteMoodFromDBStrategy

class Constants(Enum):
	LIMIT = '10'
	MARKET = 'US'
	OFFSET = '0'

	SPOTIFY_SEARCH = 'https://api.spotify.com/v1/search'
	SPOTIFY_RECOMMENDATIONS = 'https://api.spotify.com/v1/recommendations'
	SPOTIFY_TOP_ARTISTS_AND_TRACKS = 'https://api.spotify.com/v1/me/top/{0}'
	
spotify_api = Blueprint('spotify_api', __name__)
spotify_api.before_request(extract_credentials)

# Reference: https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-recommendations
@mood_api.route("/playlist-from-mood", methods=['GET'])
def get_playlist_from_mood(mood_name, **kwargs):
	generator = MoodGenerator(mood_name, g.user_id, None, GetMoodFromDBStrategy)
	mood = generator.generate()
	if mood is None:
		return Response(status = 404)
	mood = mood.params

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

	oauth_access_token = g.access_token
	headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + oauth_access_token}

	if 'seed_artists' not in get_args or 'seed_genres' not in get_args:
		# Reference: https://developer.spotify.com/console/get-current-user-top-artists-and-tracks/
		top_artists = requests.get(Constants.SPOTIFY_TOP_ARTISTS_AND_TRACKS.format('artists'), params={'limit': Constants.LIMIT}, headers=headers)
		if not top_artists.ok:
			print(top_artists.text)
			abort(500, "Error in retrieving user's top artists")
		top_artists = top_artists.json()
		seed_artists = []
		top_genres = set()
		for artist in top_artists['items']:
			seed_artists.append(artist['id'])
			top_genres.update(artist['genres'])

		if 'seed_artists' not in get_args:
			get_args['seed_artists'] = seed_artists
		if 'seed_genres' not in get_args:
			get_args['top_genres'] = list(top_genres)

	if 'seed_tracks' not in get_args:
		# Reference: https://developer.spotify.com/console/get-current-user-top-artists-and-tracks/
		top_tracks = requests.get(Constants.SPOTIFY_TOP_ARTISTS_AND_TRACKS.format('tracks'), params={'limit': Constants.LIMIT}, headers=headers)
		if not top_tracks.ok:
			print(top_tracks.text)
			abort(500, "Error in retrieving user's top tracks")
		top_tracks = top_tracks.json()
		get_args['seed_tracks'] = []
		for track in top_tracks['items']:
			get_args['seed_tracks'].append(track['id'])

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

	oauth_access_token = g.access_token
	headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + oauth_access_token}

	return requests.get(Constants.SPOTIFY_SEARCH, params=get_args, headers=headers).json()
