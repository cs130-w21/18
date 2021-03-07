import json
import flask
import JWT
import pytest
from .test_mood import test_create_mood, get_data

# Description: tests endpoint protection when JWT is missing header
# Expected input: mood name query string, NO Authorization header
# Expected outcomes:
# - API call should fail
# If any expected outcomes are not satisfied, then test fails.
# If all expected outcomes are satisified, then test succeeds.
def test_jwt_missing_header(client, app):
	MOOD_ENDPOINT, _, _ = get_data()
	json_resp = client.get(MOOD_ENDPOINT).json()
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
      'expires_at': '-1',
      'user_id': 'fake'
  }
  FAKE_BEARER = JWT.encode(payload)
  headers = {'Authorization': f"Bearer {FAKE_BEARER}"}

  MOOD_ENDPOINT, _, _ = get_data()
  json_resp = client.get(MOOD_ENDPOINT, headers=json.dumps(headers)).json()
	assert('error' in json_resp)