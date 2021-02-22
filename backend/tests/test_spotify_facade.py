import requests
import json

def do_not_int_test_spotify_api():
    mood_url = 'http://localhost:8000/api/v1/mood/mood?name=testrecommendations'
    spotify_playlist_url = 'http://localhost:8000/api/v1/spotify/playlist-from-mood?mood_name=testrecommendations'

    data = {
        "danceability": ["0.12", "0.37", "0.18"],
        "valence": ["0.12", "0.37", "0.18"]
    }
    resp = requests.put(mood_url, data=json.dumps(data))
    json_resp = resp.json()
    assert("danceability" in json_resp)

    resp = requests.put(spotify_playlist_url, data=json.dumps(data))
    json_resp = resp.json()
    assert("tracks" in json_resp)

    resp = requests.delete(url)


