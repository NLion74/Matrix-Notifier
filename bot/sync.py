import json
import requests
import os
from asyncio import sleep

import sender
import config


async def check(messages, client):
    data_dir = config.datadir_bot
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    if os.path.exists(f"{data_dir}/ids.json"):
        with open(f"{data_dir}/ids.json", "r") as f:
            ids = json.load(f)
            f.close()
    else:
        ids = []

    for msg in messages:
        id = msg['Id']
        if id in ids:
            continue
        else:
            ids.append(id)
            await sender.send(msg, client)
            with open(f"{data_dir}/ids.json", "w") as f:
                json.dump(ids, f)


async def sync( url, client):
    print("Resyncing")
    try:
        res = requests.get(f"{url}")
        messagesb = res.content.decode('utf-8')
        messages = json.loads(messagesb)
        await check(messages, client)
    except requests.exceptions.RequestException:
        print("The server seems to be down. Retrying in 20 seconds")
        await sleep(15)
        return False
