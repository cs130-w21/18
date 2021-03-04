import requests
from enum import Enum
from flask import Blueprint, request, abort, jsonify, Response, g
from .auth import extract_credentials
from .spotify_facade import spotify_api
from .playlist_generator import PlaylistGenerator, GetPlaylistsFromDBStrategy
import json

playlist_api = Blueprint('playlist_api', __name__)
playlist_api.before_request(extract_credentials)

class Constants(Enum):
	GET_PLAYLIST_FROM_MOOD = 'https://musaic-13018.herokuapp.com/api/v1/spotify/playlist-from-mood'
	MAKE_PLAYLIST = 'https://musaic-13018.herokuapp.com/api/v1/spotify/make-playlist'

@playlist_api.route("/playlist-from-mood", methods=['GET'])
def get_playlist_from_mood():
	# request.args should contain mood_id, mood_name and idx (i.e. playlist idx)
	resp = requests.get(Constants.GET_PLAYLIST_FROM_MOOD.value, params=request.args, headers=request.headers)
	if not resp.ok:
		return resp.json()
	resp_json = resp.json()

	track_uris = []
	for track in resp_json['tracks']:
		track_uris.append(track['uri'])

	# mood_id already handled by get_playlist_by_mood
	if 'idx' not in request.args:
		abort(422, description="Unprocessable entity: missing playlist idx")

	if 'mood_name' not in request.args:
		abort(422, description="Unprocessable entity: missing mood name")

	headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': request.headers['Authorization']}
	resp = requests.post(Constants.MAKE_PLAYLIST.value, json={'playlist_name': request.args['mood_name'] + ' ' + request.args['idx'], \
		'track_uris': track_uris}, headers=headers)
	if not resp.ok:
		return resp.json()
	playlist_id = resp.json()['playlist_id']

	resp_json['playlist_id'] = playlist_id
	return jsonify(resp_json)

@playlist_api.route("/playlists", methods=["GET"])
def get_playlists():
	if not request.args:
		abort(400, description="Malformed syntax")

	mood_id = request.args.get('mood_id') # ?mood_id = query string
	if mood_id is None:
		abort(422, description="Unprocessable entity: missing mood id query string")

	generator = PlaylistGenerator(mood_id, g.user_id, None, GetPlaylistsFromDBStrategy)
	playlists = generator.generate()

	if not playlists is None:
		data = {**playlists.params, 'mood_id': mood_id}
		return jsonify(data)
	return Response(status = 404)
