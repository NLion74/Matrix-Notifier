import json
import requests
import os
import logging
from asyncio import sleep

import sender
import config

logger = logging.getLogger(__name__)


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


async def sync(url, client):
    logger.info("Resyncing with server")
    try:
        if str(config.authorization) == "true" or config.authorization == True:
            authorization = True
        else:
            authorization = False

        if authorization:
            res = requests.get(
                url, headers={"Authorization": config.auth_secret})
        else:
            res = requests.get(url)
            if res.status_code == 401:
                logger.error(
                    "Authorization seems to be enabled but not in the bot config")
                return False

        messages = json.loads(res.content)
        await check(messages, client)
    except requests.exceptions.RequestException:
        logger.error("The server seems to be down.")
        return False


async def sync_forever(url, client):
    while True:
        await sync(url, client)
        await sleep(0.25)
