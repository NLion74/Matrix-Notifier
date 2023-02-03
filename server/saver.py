import sqlite3
import os
import json

import config


def get_current_id(cur):
    cur.execute('''SELECT id FROM messages ORDER BY ID DESC LIMIT 1''')
    id = cur.fetchall()
    id = id[0][0]
    return id


def get_next_id(cur):
    cur.execute('''SELECT id FROM messages ORDER BY ID DESC LIMIT 1''')
    id = cur.fetchall()
    if not id:
        id = 0
    else:
        id = id[0][0]
    id += 1
    return id


def save_to_db(msg):
    data_dir = config.datadir_server
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    con = sqlite3.connect(f"{data_dir}/messages.db")
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS messages (id INT PRIMARY KEY, channel text, title text, content text)''')
    id = get_next_id(cur)

    channel = json.dumps(msg.channel)

    cur.execute(f'''INSERT OR IGNORE INTO messages VALUES ('{id}', '{channel}', '{msg.title}', '{msg.content}')''')

    con.commit()


def clean_db():
    data_dir = config.datadir_server

    con = sqlite3.connect(f"{data_dir}/messages.db")
    cur = con.cursor()

    limit = config.limit
    cur.execute(f'''DELETE FROM messages WHERE id NOT IN (SELECT id FROM (SELECT id FROM messages ORDER BY id DESC LIMIT {limit}))''')

    con.commit()
