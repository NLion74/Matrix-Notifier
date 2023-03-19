import sqlite3
import os
import json
from datetime import datetime

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

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS messages (id INT PRIMARY KEY, date text, channels text, title text, content text, tags text, markdown text)''')
    id = get_next_id(cur)

    channels = json.dumps(msg.channels)
    tags = json.dumps(msg.tags)

    message_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute(
        'INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?)', (id, message_time, channels, msg.title, msg.content, tags, msg.markdown))

    con.commit()
    return id, message_time


def clean_db():
    message_preserve_time = config.message_preserve_time

    data_dir = config.datadir_server
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    con = sqlite3.connect(f"{data_dir}/messages.db")
    cur = con.cursor()

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS messages (id INT PRIMARY KEY, date text, channels text, title text, content text, tags text, markdown text)''')

    cur.execute(
        f'DELETE FROM messages WHERE date < datetime("now", "localtime", "-{message_preserve_time} hours")')

    con.commit()
