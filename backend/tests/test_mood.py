import json
import flask
import JWT
import pytest

def get_data():
    payload = {
        'access_token': 'fake',
        'expires_at': '1000',
        'user_id': 'fake'
    }
    FAKE_BEARER = JWT.encode(payload)
    MOOD_ENDPOINT = '/api/v1/mood/mood?name=test'

    data = {
        "seed_artists": ["hello", "world", "python"],
        "seed_genres": ["hello", "world", "python"],
        "seed_tracks": ["hello"],
        "danceability": ["12", "37", "18"],
        "valence": ["1.2", "3.7", "1.8"],
        "energy": ["0.12", "0.37", "0.18"]
    }
    headers = {'Authorization': f"Bearer {FAKE_BEARER}"}
    return MOOD_ENDPOINT, data, headers

# Description: tests mood creation
# Expected input: request body following MoodSchema, Authorization header with JWT, mood name query string
# Expected outcomes:
# - API call should succeed
# - response body should contain mood_id
# - response body should contain params following MoodSchema specified in request body
# If any expected outcomes are not satisfied, then test fails.
# If all expected outcomes are satisified, then test succeeds.
def test_create_mood(client, app):
    MOOD_ENDPOINT, data, headers = get_data()

    json_resp = client.put(MOOD_ENDPOINT, data=json.dumps(data), headers=json.dumps(headers)).json()
    assert("mood_id" in json_resp)

    mood_params = dict((k, json_resp[k]) for k in json_resp if k != 'mood_id')
    assert(mood_params == data)

# Description: tests mood creation with invalid mood schema
# Expected input: request body NOT following MoodSchema, Authorization header with JWT, mood name query string
# Expected outcomes:
# - API call should NOT succeed
# - response status should be 422 (unprocessable entity)
# If any expected outcomes are not satisfied, then test fails.
# If all expected outcomes are satisified, then test succeeds.
def test_create_mood_fail(client, app):
    MOOD_ENDPOINT, data, headers = get_data()

    resp = client.put(MOOD_ENDPOINT, data=json.dumps({}), headers=json.dumps(headers))
    assert(resp.status_code == 422)

# Description: tests mood update
# Expected input: request body following MoodSchema (different from request body for test_create_mood), 
# Authorization header with JWT, mood name query string
# Expected outcomes:
# - API call should succeed
# - response body should contain mood_id
# - response body should contain params following MoodSchema specified in request body
# If any expected outcomes are not satisfied, then test fails.
# If all expected outcomes are satisified, then test succeeds.
@pytest.mark.dependency(depends=['test_create_mood'])
def test_update_mood(client, app):
    MOOD_ENDPOINT, data, headers = get_data()
    data['danceability'] = ["0.12", "0.37", "0.18"]

    json_resp = client.put(MOOD_ENDPOINT, data=json.dumps(data), headers=json.dumps(headers)).json()
    assert("mood_id" in json_resp)

    mood_params = dict((k, json_resp[k]) for k in json_resp if k != 'mood_id')
    assert(mood_params == data)

# Description: tests getting mood created by user
# Expected input: mood name query string
# Expected outcomes:
# - API call should succeed
# - response body should contain mood_id
# - response body should contain params following MoodSchema specified in test_update_mood request body
# If any expected outcomes are not satisfied, then test fails.
# If all expected outcomes are satisified, then test succeeds.
@pytest.mark.dependency(depends=['test_update_mood'])
def test_get_mood(client, app):
    MOOD_ENDPOINT, data, headers = get_data()
    data['danceability'] = ["0.12", "0.37", "0.18"]

    json_resp = client.get(MOOD_ENDPOINT, headers=json.dumps(headers)).json()
    assert("mood_id" in json_resp)

    mood_params = dict((k, json_resp[k]) for k in json_resp if k != 'mood_id')
    assert(mood_params == data)

# Description: tests delete mood and get mood failure
# Expected input: mood name query string
# Expected outcomes:
# - delete API call should succeed
# - delete response body should contain mood_id
# - delete response body should contain params following MoodSchema specified in test_update_mood request body
# - get API call should fail
# - get response status should be 404 (mood not found)
# If any expected outcomes are not satisfied, then test fails.
# If all expected outcomes are satisified, then test succeeds.
@pytest.mark.dependency(depends=['test_get_mood'])
def test_delete_mood(client, app):
    MOOD_ENDPOINT, data, headers = get_data()
    data['danceability'] = ["0.12", "0.37", "0.18"]

    json_resp = client.delete(MOOD_ENDPOINT, headers=json.dumps(headers)).json()
    assert("mood_id" in json_resp)

    mood_params = dict((k, json_resp[k]) for k in json_resp if k != 'mood_id')
    assert(mood_params == data)

    resp = client.get(MOOD_ENDPOINT, headers=json.dumps(headers))
    assert(resp.status_code == 404)

# Description: tests getting moods for user's Explore page (i.e. moods from other users)
# Expected input: Authorization header with JWT (for different user than one in test_create_mood)
# Expected outcomes:
# - API call should succeed
# - response body should contain list of 1 mood,
# with params following MoodSchema specified in test_create_mood request body
# If any expected outcomes are not satisfied, then test fails.
# If all expected outcomes are satisified, then test succeeds.
@pytest.mark.dependency(depends=['test_delete_mood'])
def test_get_explore_moods(client, app):
    test_create_mood(client, app)

    payload = {
        'access_token': 'fake',
        'expires_at': '1000',
        'user_id': 'fake2'
    }
    FAKE_BEARER = JWT.encode(payload)
    MOOD_ENDPOINT = '/api/v1/mood/recent-moods?name=test'

    _, data, _ = get_data()
    headers = {'Authorization': f"Bearer {FAKE_BEARER}"}

    json_resp = client.get(MOOD_ENDPOINT, headers=json.dumps(headers)).json()
    assert(len(json_resp) == 1)
    json_resp = json_resp[0]
    mood = dict((k, json_resp[k]) for k in json_resp if k != 'mood_id')
    assert(mood == data)

    test_delete_mood(client, app)
