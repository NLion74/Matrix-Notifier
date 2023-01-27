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
    if not os.path.exists("./database"):
        os.mkdir("./database")
    con = sqlite3.connect("./database/messages.db")
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS messages (id INT PRIMARY KEY, title text, content text)''')
    id = get_next_id(cur)

    cur.execute(f'''INSERT OR IGNORE INTO messages VALUES ('{id}', '{msg.title}', '{msg.content}')''')

    con.commit()


def clean_db():
    con = sqlite3.connect("./database/messages.db")
    cur = con.cursor()

    cur.execute('''DELETE FROM messages WHERE id NOT IN (SELECT id FROM (SELECT id FROM messages ORDER BY id DESC LIMIT 25))''')

    con.commit()
