import json
import flask
import JWT
import pytest
from .test_mood import test_create_mood, get_data

# Description: tests getting all moods created by user
# Expected input: Authorization header with JWT
# Expected outcomes:
# - API call should succeed
# - response body should contain list of 1 mood,
# with params following MoodSchema specified in test_create_mood request body
# If any expected outcomes are not satisfied, then test fails.
# If all expected outcomes are satisified, then test succeeds.
def test_get_user_moods(client, app):
	test_create_mood(client, app)

	_, data, headers = get_data()
	USER_ENDPOINT = '/api/v1/user/moods'

	json_resp = client.get(USER_ENDPOINT, headers=json.dumps(headers)).json()
  assert(len(json_resp) == 1)
  json_resp = json_resp[0]
  mood = dict((k, json_resp[k]) for k in json_resp if k != 'mood_id')
  assert(mood == data)

  test_delete_mood(client, app)

# Description: tests adding external mood to user's collection of moods
# Expected input: Authorization header with JWT, mood_id query string
# Expected outcomes:
# - API call should succeed
# If any expected outcomes are not satisfied, then test fails.
# If all expected outcomes are satisified, then test succeeds.
def test_add_external_mood(client, app):
	_, data, headers = get_data()
	USER_ENDPOINT = '/api/v1/user/external_mood?mood_id=1'

	resp = client.put(USER_ENDPOINT, data=json.dumps(data), headers=json.dumps(headers))
	assert(resp.status == 200)

# Description: tests adding external mood with invalid mood ID to user's collection
# Expected input: Authorization header with JWT, mood_id query string
# Expected outcomes:
# - API call should fail with response status of 422 (unprocessable entity) because of invalid mood_id
# If any expected outcomes are not satisfied, then test fails.
# If all expected outcomes are satisified, then test succeeds.
def test_add_external_mood_fail(client, app):
	_, data, headers = get_data()
	USER_ENDPOINT = '/api/v1/user/external_mood?mood_id=c'

	resp = client.put(USER_ENDPOINT, data=json.dumps(data), headers=json.dumps(headers))
	assert(resp.status == 422)

