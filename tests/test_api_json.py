import requests
import json

import config

url = config.matrix_notifier_url
auth_secret = config.auth_secret
channel = config.test_channel


def test_json_content():
    message = "Test message!"
    payload = {
        "message": message
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Content'] == message


def test_json_ids():
    message = "Test message!"
    payload = {
        "message": message
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    id = json.loads(res.text)['Id']
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Id'] == (id + 1)


def test_json_utf8():
    message = "öäüßÖÄÜ€"
    payload = {
        "message": message
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Content'] == message


def test_json_title():
    message = "Hey, im actually accessed"
    title = "Test Title"
    payload = {
        "message": message,
        "title": title
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Title'] == title


def test_json_tags():
    message = "Hey, im actually accessed"
    tags = "warning, skull"
    payload = {
        "message": message,
        "tags": tags
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Tags'] == ["warning", "skull"]
    # assert message came over matrix


def test_json_tags_spaces():
    message = "Hey, im actually accessed"
    tags = "warning,                                                skull"
    payload = {
        "message": message,
        "tags": tags
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Tags'] == ["warning", "skull"]
    # assert message came over matrix


def test_json_tags_withoutspaces():
    message = "Hey, im actually accessed"
    tags = "warning,skull"
    payload = {
        "message": message,
        "tags": tags
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Tags'] == ["warning", "skull"]
    # assert message came over matrix


def test_json_markdown():
    message = "> Hey, im actually accessed"
    markdown = "TrUe"
    payload = {
        "message": message,
        "markdown": markdown
    }
    res = requests.post(f"{url}/json", data=json.dumps(payload))
    assert res.status_code == 200
    assert json.loads(res.text)['Markdown'] == markdown.lower()
    # assert message came over matrix
