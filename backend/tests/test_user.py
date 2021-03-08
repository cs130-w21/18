import json
import flask
import sys
import os
import pytest
from test_mood import test_create_mood, test_delete_mood, get_data
sys.path.insert(0, os.path.abspath('.'))
from backend.utils.jwt import JWT
from backend.utils.db import DB

# Description: tests getting all moods created by user
# Expected input: Authorization header with JWT
# Expected outcomes:
# - API call should succeed
# - response body should contain list of 1 mood,
# with params following MoodSchema specified in test_create_mood request body
# If any expected outcomes are not satisfied, then test fails.
# If all expected outcomes are satisified, then test succeeds.
def test_get_user_moods(client, app):
	with DB() as db:
		db.create_or_update_user('fake', 'fake token')

	test_delete_mood(client, app)
	test_create_mood(client, app)

	_, data, headers = get_data()
	USER_ENDPOINT = '/api/v1/user/moods'

	json_resp = client.get(USER_ENDPOINT, headers=headers).json
	assert(len(json_resp) == 2)
	created_moods = json_resp['created_moods']
	assert(len(created_moods) == 1)
	json_resp = created_moods[0]['params']
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

	resp = client.put(USER_ENDPOINT, data=json.dumps(data), headers=headers)
	assert(resp.status_code == 200)

# Description: tests adding external mood with invalid mood ID to user's collection
# Expected input: Authorization header with JWT, mood_id query string
# Expected outcomes:
# - API call should fail with response status of 422 (unprocessable entity) because of invalid mood_id
# If any expected outcomes are not satisfied, then test fails.
# If all expected outcomes are satisified, then test succeeds.
def test_add_external_mood_fail(client, app):
	_, data, headers = get_data()
	USER_ENDPOINT = '/api/v1/user/external_mood?mood_id=c'

	resp = client.put(USER_ENDPOINT, data=json.dumps(data), headers=headers)
	assert(resp.status_code == 422)

