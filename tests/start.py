from ctypes import c_int

import pytest
import sqlite3
from time import sleep
import logging

import config

logger = logging.getLogger(__name__)


def get_latest_id(cur: sqlite3.Cursor, tablename):
    cur.execute(f'''SELECT id FROM {tablename} ORDER BY ID DESC LIMIT 1''')
    id = cur.fetchall()
    if id == []:
        id = 0
    else:
        id = id[0][0]
    return id


def main():
    res = pytest.main(["."])
    logger.info("Done with testing, now waiting for bot to finish sending all messages.")

    sleep(1)

    try:
        con_server = sqlite3.connect(f"{config.database_dir}/messages.db")
        con_bot = sqlite3.connect(f"{config.database_dir}/ids.db")
        cur_server = con_server.cursor()
        cur_bot = con_bot.cursor()

        cur_server.execute(
            '''CREATE TABLE IF NOT EXISTS messages (id INT PRIMARY KEY, channels text, title text, content text, tags text, markdown text)''')
        cur_bot.execute(
            '''CREATE TABLE IF NOT EXISTS ids (id INT PRIMARY KEY)''')

        while True:
            id_server = get_latest_id(cur_server, "messages")
            id_bot = get_latest_id(cur_bot, "ids")

            if id_server <= id_bot:
                logger.info("Bot done sending all messages. Exiting...")
                quit(int(res))

            sleep(5)
    except Exception as e:
        logger.critical("Exception occurred")
        logger.critical(e)
        quit(1)


if __name__ == "__main__":
    main()
