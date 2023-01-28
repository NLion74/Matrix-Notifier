import sqlite3
import os


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
    docker = os.environ.get('docker', False)
    if docker:
        if not os.path.exists("/data"):
            os.mkdir("/data")
        con = sqlite3.connect("/data/messages.db")
    else:
        if not os.path.exists("./database"):
            os.mkdir("./database")
        con = sqlite3.connect("./database/messages.db")
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS messages (id INT PRIMARY KEY, title text, content text)''')
    id = get_next_id(cur)
    cur.execute(f'''INSERT OR IGNORE INTO messages VALUES ('{id}', '{msg.title}', '{msg.content}')''')

    con.commit()


def clean_db():
    docker = os.environ.get('docker', False)
    if docker:
        limit = os.environ.get('sqlimit', False)
        con = sqlite3.connect("/data/messages.db")
    else:
        limit = 25
        con = sqlite3.connect("./database/messages.db")
    cur = con.cursor()

    cur.execute(f'''DELETE FROM messages WHERE id NOT IN (SELECT id FROM (SELECT id FROM messages ORDER BY id DESC LIMIT {limit}))''')

    con.commit()
