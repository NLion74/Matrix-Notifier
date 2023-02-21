import json
import logging
import os
from asyncio import sleep
import asyncio
import requests

import config
import sender
from file_actions import load_file, write_file

logger = logging.getLogger(__name__)


async def save_id(file_path, ids, id):
    ids = await append(ids, id)
    res = await write_file(file_path, json.dumps(ids))
    if res:
        return True
    else:
        return False


async def append(ids, id):
    ids.append(id)
    return ids


async def check(messages, client):
    try:
        data_dir = config.datadir_bot
        if not os.path.exists(data_dir):
            os.mkdir(f"{data_dir}/ids.json")

        # This is a mess, and I have to fix it.
        if os.path.exists(f"{data_dir}/ids.json"):
            ids = json.loads(await load_file(f"{data_dir}/ids.json"))
            if not ids:
                logger.critical("An error occurred while loading ids. Exiting...")
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
                if msg['Id'] in ids:
                    continue
                else:
                    tasks = [asyncio.create_task(sender.send(msg, client)), asyncio.create_task(save_id(f"{data_dir}/ids.json", ids, msg['Id']))]
                    res = await asyncio.gather(*tasks)
                    if False in res:
                        logger.error("Error with saving or sending ids. Exiting...")
                        quit(1)
        else:
            os.remove(f"{data_dir}/ids.json")

    except Exception as e:
        logger.error(e)
        pass

async def sync(url, client):
    logger.info("Resyncing with server")
    try:
        if str(config.authorization) == "true" or config.authorization == True:
            authorization = True
        else:
            authorization = False

        if authorization:
            res = requests.get(f"{url}?limit=100&auth={config.auth_secret}")
        else:
            res = requests.get(f"{url}?limit=100")
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
