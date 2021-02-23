import requests
from enum import Enum
from flask import Blueprint, g, request, url_for
from .auth import extract_credentials
from .spotify_facade import spotify_api

playlist_api = Blueprint('playlist_api', __name__)
playlist_api.before_request(extract_credentials)

@playlist_api.route("/playlist-from-mood", methods=['GET'])
def get_playlist_from_mood():
	GET_PLAYLIST_FROM_MOOD = url_for('spotify_api.get_playlist_from_mood')
	MAKE_PLAYLIST = url_for('spotify_api.make_playlist')

	oauth_access_token = g.access_token
	headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + oauth_access_token}

	# request.args should contain mood_name and idx (i.e. playlist idx)
	resp = requests.get(GET_PLAYLIST_FROM_MOOD, params=request.args, headers=headers)
	if not resp.ok:
		return resp.json()
	resp_json = resp.json()

	track_uris = []
	for track in resp_json['tracks']:
		track_uris.append(track['uri'])

	# mood_name already handled by get_playlist_by_mood
	if 'idx' not in request.args:
		abort(422, description="Unprocessable entity: missing playlist idx")

	resp = requests.post(MAKE_PLAYLIST, data={'playlist_name': mood_name + ' ' + request.args['idx'], \
		'track_uris': track_uris}, headers=headers)
	if not resp.ok:
		return resp.json()
	playlist_id = resp.json()['playlist_id']

	resp_json['playlist_id'] = playlist_id
	return jsonify(resp_json)
