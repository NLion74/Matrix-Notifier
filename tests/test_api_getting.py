import requests
import json

import config

url = config.matrix_notifier_url
auth_secret = config.auth_secret
channel = config.test_channel


def test_api_access():
    res = requests.get(f"{url}/messages?auth={auth_secret}")
    assert res.status_code == 200


def test_getting_limit_negativenumber():
    res = requests.get(f"{url}/messages?auth={auth_secret}&limit=-1")
    assert res.status_code == 200
    assert type(json.loads(res.text)) == type([])
    assert type(json.loads(res.text)[0]) == type({})
    assert type(json.loads(res.text)[0]['Id']) == type(1)


def test_getting_limit_zero():
    res = requests.get(f"{url}/messages?auth={auth_secret}&limit=0")
    assert res.status_code == 200
    assert type(json.loads(res.text)) == type([])
    assert len(json.loads(res.text)) == 0


def test_getting_limit_one():
    res = requests.get(f"{url}/messages?auth={auth_secret}&limit=1")
    assert res.status_code == 200
    assert type(json.loads(res.text)) == type([])
    assert len(json.loads(res.text)) == 1

def test_getting_limit_words():
    res = requests.get(f"{url}/messages?auth={auth_secret}&limit=word")
    assert res.status_code == 500
