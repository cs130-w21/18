import sys
import json
import flask
import sys
import os
import pytest
from test_mood import test_create_mood, get_data

sys.path.insert(0, os.path.abspath('.'))
from backend.utils.jwt import JWT
from backend.auth import create_jwt

# Description: tests endpoint protection when JWT is missing header
# Expected input: mood name query string, NO Authorization header
# Expected outcomes:
# - API call should fail
# If any expected outcomes are not satisfied, then test fails.
# If all expected outcomes are satisified, then test succeeds.
def test_jwt_missing_header(client, app):
	MOOD_ENDPOINT, _, _ = get_data()
	resp = client.get(MOOD_ENDPOINT)
	json_resp = resp.json
	assert('error' in json_resp)

# Description: tests endpoint protection when JWT has invalid expiration time
# Expected input: mood name query string, Authorization header with invalid expiration time
# Expected outcomes:
# - API call should fail
# If any expected outcomes are not satisfied, then test fails.
# If all expected outcomes are satisified, then test succeeds.
def test_jwt_expired_token(client, app):
	payload = {
		'access_token': 'fake',
		'expires_at': 1,
		'user_id': 'fake'
		}
	FAKE_BEARER = create_jwt('fake', 'fake', -1)
	headers = {'Authorization': f"Bearer {FAKE_BEARER}"}
	MOOD_ENDPOINT, _, _ = get_data()
	resp = client.get(MOOD_ENDPOINT, headers=headers)
	json_resp = resp.json
	assert('error' in json_resp)
