import requests

import config

url = config.server_url

def test_webpage_opening():
    res = requests.get(url)
    assert res.status_code == 200
