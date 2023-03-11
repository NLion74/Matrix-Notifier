import json
import logging
import os
from asyncio import sleep
import asyncio
import requests
import sqlite3

import config
import sender

logger = logging.getLogger(__name__)


async def save_id(con, cur, id):
    try:
        cur.execute(
            '''INSERT OR IGNORE INTO ids VALUES (:id)''', {"id": id})
        con.commit()
    except Exception as e:
        logger.error(e)
        return False


async def check(messages, client):
    try:
        data_dir = config.datadir_bot
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

        con = sqlite3.connect(f"{data_dir}/ids.db")
        cur = con.cursor()

        cur.execute(
            '''CREATE TABLE IF NOT EXISTS ids (id INT PRIMARY KEY)''')

        cur.execute(f'''SELECT * FROM (SELECT * FROM ids ORDER BY id DESC LIMIT 250) sub ORDER BY id ASC''')
        data = cur.fetchall()
        ids = []
        for tuple in data:
            ids_raw = tuple[0]
            ids.append(ids_raw)

        if not ids:
            prev_id = -1
        else:
            prev_id = int(ids[(len(ids) - 1)])

        if not messages:
            curr_id = -1
        else:
            curr_id = messages[(len(messages) - 1)]['Id']

        if curr_id >= prev_id or prev_id == -1:
            for msg in messages:
                if msg['Id'] in ids:
                    continue
                else:
                    tasks = [asyncio.create_task(sender.send(msg, client)), asyncio.create_task(save_id(con, cur, msg['Id']))]
                    res = await asyncio.gather(*tasks)
                    if False in res:
                        logger.error("Error with saving or sending ids.")
                        return False
        else:
            con.execute('''DROP TABLE IF EXISTS ids''')

    except Exception as e:
        logger.error(e)
        pass
    finally:
        con.commit()


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
