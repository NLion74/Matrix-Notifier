import requests
import json

import config

url = config.matrix_notifier_url
auth_secret = config.auth_secret
channel = config.test_channel

def test_webhook_content():
    message = "Test message!"
    res = requests.get(f"{url}/webhook?auth={auth_secret}%channel={channel}&message={message.replace(' ', '+')}")
    assert res.status_code == 200
    assert json.loads(res.text)['Content'] == message


def test_webhook_ids():
    message = "Test message!"
    res = requests.get(f"{url}/webhook?auth={auth_secret}%channel={channel}&message={message.replace(' ', '+')}")
    id = json.loads(res.text)['Id']
    res = requests.post(url, headers={"Channel": channel, "Authorization": auth_secret}, data=message.encode("utf-8"))
    assert res.status_code == 200
    assert json.loads(res.text)['Id'] == (id + 1)


def test_webhook_utf8():
    message = "öäüßÖÄÜ€"
    res = requests.get(f"{url}/webhook?auth={auth_secret}%channel={channel}&message={message.replace(' ', '+')}")
    assert res.status_code == 200
    assert json.loads(res.text)['Content'] == message


def test_webhook_title():
    message = "Hey, im actually accessed"
    title = "Test Title"
    res = requests.get(f"{url}/webhook?auth={auth_secret}%channel={channel}&message={message.replace(' ', '+')}&title={title.replace(' ', '+')}")
    assert res.status_code == 200
    assert json.loads(res.text)['Title'] == title


def test_webhook_tags():
    message = "Hey, im actually accessed"
    tags = "warning, skull"
    res = requests.get(f"{url}/webhook?auth={auth_secret}%channel={channel}&message={message.replace(' ', '+')}&tags={tags.replace(' ', '+')}")
    assert res.status_code == 200
    assert json.loads(res.text)['Tags'] == ["warning", "skull"]
    # assert message came over matrix


def test_webhook_tags_spaces():
    message = "Hey, im actually accessed"
    tags = "warning,                                                skull"
    res = requests.get(f"{url}/webhook?auth={auth_secret}%channel={channel}&message={message.replace(' ', '+')}&tags={tags.replace(' ', '+')}")
    assert res.status_code == 200
    assert json.loads(res.text)['Tags'] == ["warning", "skull"]
    # assert message came over matrix


def test_webhook_tags_withoutspaces():
    message = "Hey, im actually accessed"
    tags = "warning,skull"
    res = requests.get(f"{url}/webhook?auth={auth_secret}%channel={channel}&message={message.replace(' ', '+')}&tags={tags.replace(' ', '+')}")
    assert res.status_code == 200
    assert json.loads(res.text)['Tags'] == ["warning", "skull"]
    # assert message came over matrix


def test_webhook_markdown():
    message = "> Hey, im actually accessed"
    markdown = "TrUe"
    res = requests.get(f"{url}/webhook?auth={auth_secret}%channel={channel}&message={message.replace(' ', '+')}&markdown={markdown}")
    assert res.status_code == 200
    assert json.loads(res.text)['Markdown'] == markdown.lower()
    # assert message came over matrix
