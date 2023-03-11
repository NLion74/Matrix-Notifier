import requests
import json

import config

url = config.server_url
auth_secret = config.auth_secret
channel = config.channel


def test_api_access():
    res = requests.get(f"{url}/messages?auth={auth_secret}")
    assert res.status_code == 200


def test_api_access_withoutauth():
    res = requests.get(f"{url}/messages")
    assert res.status_code == 401


# make sure message is in db cause its needed
def test_api_sendmessage():
    message = "Initialization!"
    res = requests.post(url, headers={"Authorization": auth_secret}, data=message.encode("utf-8"))
    assert res.status_code == 200
    res = requests.post(url, headers={"Authorization": auth_secret}, data=message.encode("utf-8"))
    assert res.status_code == 200
    res = requests.post(url, headers={"Authorization": auth_secret}, data=message.encode("utf-8"))
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


def test_getting_referencingbyid():
    res = requests.get(f"{url}/messages/1?auth={auth_secret}")
    assert res.status_code == 200
    assert type(json.loads(res.text)) == type([])
    assert len(json.loads(res.text)) == 1


def test_getting_referencingbyid_commas():
    res = requests.get(f"{url}/messages/1,3?auth={auth_secret}")
    assert res.status_code == 200
    assert type(json.loads(res.text)) == type([])
    assert len(json.loads(res.text)) == 2
    assert json.loads(res.text)[0]['Id'] == 1
    assert json.loads(res.text)[1]['Id'] == 3
