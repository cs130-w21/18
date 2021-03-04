import requests
from enum import Enum
from flask import Blueprint, request, abort, jsonify, Response, g
from .auth import extract_credentials
from .spotify_facade import spotify_api
from .playlist_generator import PlaylistGenerator, GetPlaylistsFromDBStrategy, StorePlaylistInDBStrategy
import json
from .utils.db import DB

playlist_api = Blueprint('playlist_api', __name__)
playlist_api.before_request(extract_credentials)

class Constants(Enum):
	GET_PLAYLIST_FROM_MOOD = 'https://musaic-13018.herokuapp.com/api/v1/spotify/playlist-from-mood'
	MAKE_PLAYLIST = 'https://musaic-13018.herokuapp.com/api/v1/spotify/make-playlist'

@playlist_api.route("/playlist-from-mood", methods=['GET'])
def get_playlist_from_mood():
	# request.args should contain mood_id and mood_name
	resp = requests.get(Constants.GET_PLAYLIST_FROM_MOOD.value, params=request.args, headers=request.headers)
	if not resp.ok:
		return resp.json()
	resp_json = resp.json()

	track_uris = []
	for track in resp_json['tracks']:
		track_uris.append(track['uri'])

	# mood_id already handled by get_playlist_by_mood
	idx = None
	with DB() as db:
		idx = db.get_next_playlist_idx_for_mood(g.user_id, request.args['mood_id'])
	if idx is None:
		abort(500, description="Server error: Unable to get next idx for playlist")

	if 'mood_name' not in request.args:
		abort(422, description="Unprocessable entity: missing mood name")

	headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': request.headers['Authorization']}
	resp = requests.post(Constants.MAKE_PLAYLIST.value, json={'playlist_name': request.args['mood_name'] + ' ' + str(idx), \
		'track_uris': track_uris}, headers=headers)
	if not resp.ok:
		return resp.json()
	playlist_uri = resp.json()['playlist_uri']

	generator = PlaylistGenerator(request.args['mood_id'], g.user_id, playlist_uri, StorePlaylistInDBStrategy)
	playlist = generator.generate()

	if playlist is None:
		abort(500, description="Server error: Could not save playlist")

	resp_json = {**playlist.to_dict(), **resp_json}
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
		data = [playlist.to_dict() for playlist in playlists]
		return jsonify(data)
	return Response(status = 404)
