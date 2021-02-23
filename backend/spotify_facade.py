import requests
from enum import Enum
from flask import Blueprint, request, abort, jsonify, Response, g
from .auth import extract_credentials
from .mood_generator import MoodGenerator, CreateOrUpdateMoodStrategy, \
		GetMoodFromDBStrategy, DeleteMoodFromDBStrategy
import json

class Constants(Enum):
	LIMIT = '10'
	MARKET = 'US'
	OFFSET = '0'

	SPOTIFY_SEARCH = 'https://api.spotify.com/v1/search'
	SPOTIFY_RECOMMENDATIONS = 'https://api.spotify.com/v1/recommendations'
	SPOTIFY_TOP_ARTISTS_AND_TRACKS = 'https://api.spotify.com/v1/me/top/{0}'
	SPOTIFY_MAKE_PLAYLIST = 'https://api.spotify.com/v1/users/{0}/playlists'
	SPOTIFY_ADD_TO_PLAYLIST = 'https://api.spotify.com/v1/playlists/{0}/tracks'
	
spotify_api = Blueprint('spotify_api', __name__)
spotify_api.before_request(extract_credentials)

# Reference: https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-recommendations
@spotify_api.route("/playlist-from-mood", methods=['GET'])
def get_playlist_from_mood():
	if not request.args:
		abort(400, description="Malformed syntax")

	if request.args.get('mood_name') is None: # ?mood_name = mood name string
		abort(422, description="Unprocessable entity: missing mood name")

	generator = MoodGenerator(request.args.get('mood_name'), g.user_id, None, GetMoodFromDBStrategy)
	mood = generator.generate()
	if mood is None:
		return Response(status = 404)
	mood = mood.params

	get_args = {}
	if 'limit' not in request.args:
		get_args['limit'] = Constants.LIMIT.value
	if 'market' not in request.args:
		get_args['market'] = Constants.MARKET.value
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
		top_artists = requests.get(Constants.SPOTIFY_TOP_ARTISTS_AND_TRACKS.value.format('artists'), params={'limit': Constants.LIMIT.value}, headers=headers)
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
		top_tracks = requests.get(Constants.SPOTIFY_TOP_ARTISTS_AND_TRACKS.value.format('tracks'), params={'limit': Constants.LIMIT.value}, headers=headers)
		if not top_tracks.ok:
			print(top_tracks.text)
			abort(500, "Error in retrieving user's top tracks")
		top_tracks = top_tracks.json()
		get_args['seed_tracks'] = []
		for track in top_tracks['items']:
			get_args['seed_tracks'].append(track['id'])

	print(get_args)
	return requests.get(Constants.SPOTIFY_RECOMMENDATIONS.value, params=get_args, headers=headers).json()

# Returns Spotify ID of queried track/artist
# Reference: https://developer.spotify.com/documentation/web-api/reference/#endpoint-search
@spotify_api.route("/search", methods=['GET'])
def get_spotify_id():
	if not request.args:
		abort(400, description="Malformed syntax")

	if request.args.get('query') is None: # ?query = query string
		abort(422, description="Unprocessable entity: missing query")

	if request.args.get('type') is None: # ?type = query string (artist or track)
		abort(422, description="Unprocessable entity: missing query type")

	get_args = {}
	if 'limit' not in request.args:
		get_args['limit'] = Constants.LIMIT.value
	if 'market' not in request.args:
		get_args['market'] = Constants.MARKET.value
	if 'offset' not in request.args:
		get_args['offset'] = Constants.OFFSET.value
	for k, v in request.args.items():
		get_args[k] = v

	oauth_access_token = g.access_token
	headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + oauth_access_token}

	return requests.get(Constants.SPOTIFY_SEARCH.value, params=get_args, headers=headers).json()

# Makes playlist with given tracks
# Reference: https://developer.spotify.com/documentation/web-api/reference/#endpoint-create-playlist
@spotify_api.route("/make-playlist", methods=["POST"])
def make_playlist():
	print(request.data)
	if not request.data:
		abort(400, description="Malformed syntax")

	data = json.loads(request.data.decode("utf8"))
	if 'playlist_name' not in data:
		abort(422, description="Unprocessable entity: missing playlist name")
	if 'track_uris' not in data:
		abort(422, description="Unprocessable entity: missing track URIs")

	oauth_access_token = g.access_token
	headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + oauth_access_token}

	post_data = {
		'name': data['playlist_name'],
		'public': 'false'
	}
	resp = requests.post(Constants.SPOTIFY_MAKE_PLAYLIST.value.format(g.user_id), data=post_data)
	if not resp.ok:
		print(resp.text)
		abort(500, "Error in making playlist")
	playlist_id = resp.json()['id']

	post_data = {
		'uris': data['track_uris']
	}
	resp = requests.post(Constants.SPOTIFY_ADD_TO_PLAYLIST.value.format(playlist_id), data=post_data)
	if not resp.ok:
		print(resp.text)
		abort(500, "Error in adding to playlist")

	return jsonify({'playlist_id': playlist_id})

