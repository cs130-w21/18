import requests
from enum import Enum
from flask import Blueprint, g, request
from .auth import extract_credentials
from .spotify_facade import spotify_api

playlist_api = Blueprint('playlist_api', __name__)
playlist_api.before_request(extract_credentials)

class Constants(Enum):
	GET_PLAYLIST_FROM_MOOD = 'https://musaic-13018.herokuapp.com/api/v1/spotify/playlist-from-mood'
	MAKE_PLAYLIST = 'https://musaic-13018.herokuapp.com/api/v1/spotify/make-playlist'

@playlist_api.route("/playlist-from-mood", methods=['GET'])
def get_playlist_from_mood():
	# request.args should contain mood_name and idx (i.e. playlist idx)
	resp = requests.get(Constants.GET_PLAYLIST_FROM_MOOD.value, params=request.args, headers=request.headers)
	if not resp.ok:
		return resp.json()
	resp_json = resp.json()
	print(resp_json)

	track_uris = []
	for track in resp_json['tracks']:
		track_uris.append(track['uri'])

	# mood_name already handled by get_playlist_by_mood
	if 'idx' not in request.args:
		abort(422, description="Unprocessable entity: missing playlist idx")

	resp = requests.post(Constants.MAKE_PLAYLIST.value, data={'playlist_name': mood_name + ' ' + request.args['idx'], \
		'track_uris': track_uris}, headers=request.headers)
	if not resp.ok:
		return resp.json()
	playlist_id = resp.json()['playlist_id']

	resp_json['playlist_id'] = playlist_id
	return jsonify(resp_json)
