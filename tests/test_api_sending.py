import requests
import json

import config

url = config.matrix_notifier_url
auth_secret = config.auth_secret
channel = config.test_channel


def test_sending_content():
    message = "Test message!"
    res = requests.post(url, headers={"Channel": channel, "Authorization": auth_secret}, data=message.encode("utf-8"))
    assert res.status_code == 200
    assert json.loads(res.text)['Content'] == message
    # assert message came over matrix


def test_sending_ids():
    message = "Test message!"
    res = requests.post(url, headers={"Channel": channel, "Authorization": auth_secret}, data=message.encode("utf-8"))
    id = json.loads(res.text)['Id']
    res = requests.post(url, headers={"Channel": channel, "Authorization": auth_secret}, data=message.encode("utf-8"))
    assert res.status_code == 200
    assert json.loads(res.text)['Id'] == (id + 1)
    # assert message came over matrix


def test_sending_content_utf8():
    message = "öäüßÖÄÜ€"
    res = requests.post(url, headers={"Channel": channel, "Authorization": auth_secret}, data=message.encode("utf-8"))
    assert json.loads(res.text)['Content'] == message
    # assert message came over matrix


def test_sending_title():
    message = "Hey, im actually accessed"
    title = "Test Title"
    res = requests.post(url, headers={"Channel": channel, "Authorization": auth_secret, "Title": title}, data=message.encode("utf-8"))
    assert res.status_code == 200
    assert json.loads(res.text)['Title'] == title
    # assert message came over matrix


def test_sending_tags():
    message = "Hey, im actually accessed"
    tags = "warning, skull"
    res = requests.post(url, headers={"Channel": channel, "Authorization": auth_secret, "Tags": tags}, data=message.encode("utf-8"))
    assert res.status_code == 200
    assert json.loads(res.text)['Tags'] == ["warning", "skull"]
    # assert message came over matrix


def test_sending_tags_spaces():
    message = "Hey, im actually accessed"
    tags = "warning,                                                skull"
    res = requests.post(url, headers={"Channel": channel, "Authorization": auth_secret, "Tags": tags}, data=message.encode("utf-8"))
    assert res.status_code == 200
    assert json.loads(res.text)['Tags'] == ["warning", "skull"]
    # assert message came over matrix


def test_sending_tags_withoutspaces():
    message = "Hey, im actually accessed"
    tags = "warning,skull"
    res = requests.post(url, headers={"Channel": channel, "Authorization": auth_secret, "Tags": tags}, data=message.encode("utf-8"))
    assert res.status_code == 200
    assert json.loads(res.text)['Tags'] == ["warning", "skull"]
    # assert message came over matrix


def test_sending_markdown():
    message = "> Hey, im actually accessed"
    markdown = "TrUe"
    res = requests.post(url, headers={"Channel": channel, "Authorization": auth_secret, "Markdown": markdown}, data=message.encode("utf-8"))
    assert res.status_code == 200
    assert json.loads(res.text)['Markdown'] == markdown.lower()
    # assert message came over matrix
