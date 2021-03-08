import pytest
import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from main import app as main_app

@pytest.fixture
def app():
	return main_app

@pytest.fixture
def client():
	return main_app.test_client()
