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

    # Fix if ids is zero index out of range
    if not ids:
        prev_id = -1
    else:
        prev_id = ids[(len(ids) - 1)]

    if not messages:
        curr_id = -1
    else:
        curr_id = messages[(len(messages) - 1)]['Id']

    if curr_id >= prev_id or prev_id == -1:
        for msg in messages:
            id = msg['Id']
            if id in ids:
                continue
            else:
                ids.append(id)
                await sender.send(msg, client)
                with open(f"{data_dir}/ids.json", "w") as f:
                    json.dump(ids, f)
    else:
        os.remove(f"{data_dir}/ids.json")


async def sync( url, client):
    print("Resyncing")
    try:
        res = requests.get(url)
        messages = json.loads(res.content)

        await check(messages, client)
    except requests.exceptions.RequestException:
        print("The server seems to be down. Retrying in 20 seconds")
        await sleep(15)
        return False
