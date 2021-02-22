import requests
import json

def test_hello_world():
    resp = requests.get("http://localhost:8000/")
    assert(resp.text == "Hello World!")

def do_no_test_mood_api():
    url = 'http://localhost:8000/api/v1/mood/fakeUser/mood?name=helloworld'
    data = {
        "seed_artists": ["hello", "world", "python"],
        "seed_genres": ["hello", "world", "python"],
        "seed_tracks": ["hello"]
    }
    resp = requests.put(url, data=json.dumps(data))
    json_resp = resp.json()
    assert("seed_artists" in json_resp)
    data = {
        "seed_artists": ["hello", "world", "python"],
        "seed_genres": ["hello", "world", "python"],
        "seed_tracks": ["hello"],
        "danceability": ["12", "37", "18"],
        "valence": ["1.2", "3.7", "1.8"]
    }
    resp = requests.put(url, data=json.dumps(data))
    json_resp = resp.json()
    assert("danceability" in json_resp)
    resp = requests.get(url)
    json_resp = resp.json()
    assert("danceability" in json_resp)
    assert("seed_artists" in json_resp)
    resp = requests.delete(url)
    resp = requests.get(url)
    assert(resp.status_code == 404)

