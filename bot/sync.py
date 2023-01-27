import json
import requests
import os

import sender


async def check(messages, client):
    if not os.path.exists("./saved"):
        os.mkdir("./saved")

    if os.path.exists("./saved/ids.json"):
        with open("./saved/ids.json", "r") as f:
            ids = json.load(f)
            f.close()
    else:
        ids = []

    for msg in messages:
        id = msg[0]
        if id in ids:
            continue
        else:
            ids.append(id)
            await sender.send(msg, client)

    with open("./saved/ids.json", "w") as f:
        json.dump(ids, f)
        f.close()


async def sync(scheme, url, client):
    try:
        res = requests.get(f"{scheme}{url}")
        messagesb = res.content.decode('utf-8')
        messages = json.loads(messagesb)
        await check(messages, client)
    except ConnectionError:
        print("The Server seems to be down")
        raise ConnectionError
    except Exception:
        raise Exception
