import json
import requests
import os
from asyncio import sleep

import sender


async def check(messages, client):
    docker = os.environ.get('docker', False)
    if docker:
        if not os.path.exists("/data"):
            os.mkdir("/data")

        if os.path.exists("/data/ids.json"):
            with open("/data/ids.json", "r") as f:
                ids = json.load(f)
                f.close()
        else:
            ids = []
    else:
        if not os.path.exists("./saved"):
            os.mkdir("./saved")

        if os.path.exists("./saved/ids.json"):
            with open("./saved/ids.json", "r") as f:
                ids = json.load(f)
                f.close()
        else:
            ids = []
    print("checking")
    for msg in messages:
        id = msg[0]
        if id in ids:
            continue
        else:
            ids.append(id)
            await sender.send(msg, client)
            if docker:
                with open("/data/ids.json", "w") as f:
                    json.dump(ids, f)
            else:
                with open("./saved/ids.json", "w") as f:
                    json.dump(ids, f)


async def sync( url, client):
    print("Resyncing")
    try:
        res = requests.get(f"{url}")
        messagesb = res.content.decode('utf-8')
        messages = json.loads(messagesb)
        print("checking")
        await check(messages, client)
    except requests.exceptions.RequestException:
        print("The server seems to be down. Retrying in 20 seconds")
        await sleep(15)
        return False
