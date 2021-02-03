import requests

def test_get_fortune():
    resp = requests.get("http://localhost:8000/")
    assert(resp.text == "O, Fortuna")
