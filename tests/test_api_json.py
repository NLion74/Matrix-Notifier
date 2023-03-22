import requests
import json

import config

url = config.server_url
auth_secret = config.auth_secret
channel = config.channel


def test_json_content_withoutauth():
    message = "Test message!"
    payload = {
        "message": message,
        "channel": channel
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 401


def test_json_content_nomessage():
    payload = {
        "channel": channel
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 400


def test_json_content_wrongjson():
    payload = "Duhhhh"
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 400


def test_json_content():
    message = "Test message!"
    payload = {
        "message": message,
        "channel": channel,
        "auth": auth_secret
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Content'] == message


def test_json_ids():
    message = "Test message!"
    payload = {
        "message": message,
        "channel": channel,
        "auth": auth_secret
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    id = json.loads(res.text)['Id']
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Id'] == (id + 1)


def test_json_utf8():
    message = "öäüßÖÄÜ€"
    payload = {
        "message": message,
        "channel": channel,
        "auth": auth_secret
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Content'] == message


def test_json_title():
    message = "Hey, im actually accessed"
    title = "Test Title"
    payload = {
        "message": message,
        "title": title,
        "channel": channel,
        "auth": auth_secret
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Title'] == title


def test_json_tags():
    message = "Hey, im actually accessed"
    tags = "warning, skull"
    payload = {
        "message": message,
        "tags": tags,
        "channel": channel,
        "auth": auth_secret
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Tags'] == ["warning", "skull"]


def test_json_tags_spaces():
    message = "Hey, im actually accessed"
    tags = "warning,                                                skull"
    payload = {
        "message": message,
        "tags": tags,
        "channel": channel,
        "auth": auth_secret
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Tags'] == ["warning", "skull"]


def test_json_tags_withoutspaces():
    message = "Hey, im actually accessed"
    tags = "warning,skull"
    payload = {
        "message": message,
        "tags": tags,
        "channel": channel,
        "auth": auth_secret
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Tags'] == ["warning", "skull"]


def test_json_markdown():
    message = "> Hey, im actually accessed"
    markdown = "TrUe"
    payload = {
        "message": message,
        "markdown": markdown,
        "channel": channel,
        "auth": auth_secret
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Markdown'] == markdown.lower()


def test_json_channel_multipleduplicate():
    payload = {
        "message": "Test",
        "channel": f"{channel}, {channel}",
        "auth": auth_secret
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Channels'] == [channel]


def test_json_channel_multipleunique():
    payload = {
        "message": "Test",
        "channel": f"{channel}, !IvYrlASwHuqfFHxFIpL:matrix.org",
        "auth": auth_secret
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Channels'] == [channel, "!IvYrlASwHuqfFHxFIpL:matrix.org"]
