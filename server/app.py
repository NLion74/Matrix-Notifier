from flask import Flask, request
import sqlite3
import os
import json

import config
import parser
import saver

app = Flask(__name__)


@app.route("/", methods=['POST'])
def post():
    body = request.get_data()
    headers = dict(request.headers)

    parameter = parser.headerparse(headers=headers)

    msg = parser.messageparse(parameter=parameter, body=body)

    saver.save_to_db(msg)
    saver.clean_db()

    return "Thingy Workingy", 200


@app.route("/", methods=['GET'])
def get():
    data_dir = config.datadir_server
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    con = sqlite3.connect(f"{data_dir}/messages.db")
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS messages (id INT PRIMARY KEY, title text, content text)''')

    cur.execute('''SELECT * FROM messages''')
    data = cur.fetchall()
    message_data_list = []
    for tuple in data:
        message_data = dict([('Id', tuple[0]), ('Channels', tuple[1]), ('Title', tuple[2]), ('Content', tuple[3])])
        message_data_list.append(message_data)

    content_data = json.dumps(message_data_list)

    con.commit()

    return content_data, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.port)