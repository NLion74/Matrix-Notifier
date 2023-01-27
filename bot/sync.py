import json
import requests
import os
from asyncio import sleep

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


async def sync(scheme, url, client):
    print("Resyncing")
    try:
        res = requests.get(f"{scheme}{url}")
        messagesb = res.content.decode('utf-8')
        messages = json.loads(messagesb)
        await check(messages, client)
    except requests.exceptions.RequestException:
        print("The server seems to be down. Retrying in 20 seconds")
        await sleep(15)
        return False
