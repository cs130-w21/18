import requests
from enum import Enum
from flask import Blueprint, request, abort, jsonify, Response, g
from .auth import extract_credentials
from .mood_generator import MoodGenerator, GetMoodFromDBWithIDStrategy
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

class Spotify:
    
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {access_token}"
                }

    def get_top_tracks(self):
        tracks_resp = requests.get(
                Constants.SPOTIFY_TOP_ARTISTS_AND_TRACKS.value.format('tracks'), 
                params={'limit': Constants.LIMIT.value}, 
                headers=self.headers
                )
        if not tracks_resp.ok:
            print("Unable to get user's top tracks")
            print(tracks_resp.json())
            return None
        tracks = tracks_resp.json()['items']
        return [track['id'] for track in tracks]

    def get_top_artists_and_genres(self):
        artists_resp = requests.get(
                Constants.SPOTIFY_TOP_ARTISTS_AND_TRACKS.value.format('artists'), 
                params={'limit': Constants.LIMIT.value}, 
                headers=self.headers
                )
        if not artists_resp.ok:
            print("Unable to get user's top artists and genres")
            print(artists_resp.json())
            return None, None
        top_artists = artists_resp.json()['items']
        seed_artists = []
        top_genres = set()
        for artist in top_artists:
            seed_artists.append(artist['id'])
            top_genres.update(artist['genres'])
        return seed_artists, top_genres

    def get_recommendations(self, get_args):
        rec_resp = requests.get(
                Constants.SPOTIFY_RECOMMENDATIONS.value, 
                params=get_args, 
                headers=self.headers)
        if not rec_resp.ok:
            print("Unable to get recommendations from Spotify")
            print(rec_resp.json())
            return None
        return rec_resp.json()['tracks']


    def make_playlist(self, user_id, playlist_name):
        post_data = {
                'name': playlist_name,
                'public': 'false'
                }
        playlist_resp = requests.post(
                Constants.SPOTIFY_MAKE_PLAYLIST.value.format(user_id), 
                json=post_data, 
                headers=self.headers
                )
        if not playlist_resp.ok:
            print(f"Unable to create playlist with name {playlist_name}")
            print(playlist_resp.json())
            return None
        return playlist_resp.json()['id']

    def add_tracks_to_playlist(self, tracks, playlist_id):
        post_data = {
                'uris': tracks,
                }
        playlist_resp = requests.post(
                Constants.SPOTIFY_ADD_TO_PLAYLIST.value.format(playlist_id), 
                json=post_data, 
                headers=self.headers
                )
        if not playlist_resp.ok:
            print(f"Unable to add tracks to playlist {playlist_id}")
            print(playlist_resp.json())
            return False
        return True

        
spotify_api = Blueprint('spotify_api', __name__)
spotify_api.before_request(extract_credentials)

# Reference: https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-recommendations
@spotify_api.route("/playlist-from-mood", methods=['GET'])
def get_playlist_from_mood():
    if not request.args:
        abort(400, description="Malformed syntax")

    if request.args.get('mood_id') is None: # ?mood_id = mood id string
        abort(422, description="Unprocessable entity: missing mood id")

    mood_id = request.args.get('mood_id')

    try:
        mood_id = int(mood_id)
    except:
        abort(422, description="Unprocessable entity: invalid mood id")

    generator = MoodGenerator(None, None, None, mood_id, GetMoodFromDBWithIDStrategy)
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
        else:   # seed parameters
            get_args[k] = v

    oauth_access_token = g.access_token

    if 'seed_artists' not in get_args or 'seed_genres' not in get_args:
        # Reference: https://developer.spotify.com/console/get-current-user-top-artists-and-tracks/
        seed_artists, top_genres = Spotify(oauth_access_token).get_top_artists_and_genres()
        if seed_artists is None:
            abort(500, "Error in retrieving user's top artists")

        if 'seed_artists' not in get_args:
            get_args['seed_artists'] = seed_artists
        if 'seed_genres' not in get_args:
            get_args['top_genres'] = list(top_genres)

    if 'seed_tracks' not in get_args:
        # Reference: https://developer.spotify.com/console/get-current-user-top-artists-and-tracks/
        top_tracks = Spotify(oauth_access_token).get_top_tracks()
        if top_tracks is None:
            abort(500, "Error in retrieving user's top tracks")
        get_args['seed_tracks'] = top_tracks

    recommendations = Spotify(oauth_access_token).get_recommendations(get_args)
    if recommendations is None:
        abort(500, "Error in retrieving recommendations from Spotify")
    return jsonify({'tracks': recommendations})

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
    if not request.data:
        abort(400, description="Malformed syntax")

    data = json.loads(request.data.decode("utf8"))
    if 'playlist_name' not in data:
        abort(422, description="Unprocessable entity: missing playlist name")
    if 'track_uris' not in data:
        abort(422, description="Unprocessable entity: missing track URIs")

    oauth_access_token = g.access_token

    playlist_id = Spotify(oauth_access_token).make_playlist(g.user_id, data['playlist_name'])
    
    if playlist_id is None:
        abort(500, "Error in making playlist")

    tracks_added = Spotify(oauth_access_token).add_tracks_to_playlist(data['track_uris'], playlist_id)
    if not tracks_added:
        abort(500, "Error in adding to playlist")

    return jsonify({'playlist_id': playlist_id})
