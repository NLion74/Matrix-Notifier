from flask import Flask, request, render_template
import sqlite3
import os
import json
import logging

import config
import parser
import authenticator
import saver

logger = logging.getLogger()

app = Flask(__name__,
            static_folder='web/static',
            static_url_path='/static',
            template_folder='web/templates')


@app.route("/", methods=['POST'])
def post_messages():
    body = request.get_data()
    headers = dict(request.headers)

    parameter = parser.headerparse(headers=headers)

    if parameter == "wrong_markdown":
        return "Wrong markdown format", 403

    auth_res = authenticator.auth(parameter.auth_pass)

    if not auth_res:
        return "Unauthorized", 401

    msg = parser.messageparse(parameter=parameter, body=body)

    saver.save_to_db(msg)

    return "Message successfully saved to database", 200


@app.route("/messages", methods=['GET'])
def get_messages():
    queries = dict(request.args)

    parameter, message = parser.queryparse(queries=queries)

    auth_res = authenticator.auth(parameter.auth_pass)

    if not auth_res:
        return "Unauthorized", 401

    data_dir = config.datadir_server
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    con = sqlite3.connect(f"{data_dir}/messages.db")
    cur = con.cursor()

    cur.execute(
        '''CREATE TABLE IF NOT EXISTS messages (id INT PRIMARY KEY, channels text, title text, content text, tags text, markdown text)''')

    cur.execute(f'''SELECT * FROM (SELECT * FROM messages ORDER BY id DESC LIMIT {parameter.limit}) sub ORDER BY id ASC''')
    data = cur.fetchall()
    message_data_list = []
    for tuple in data:
        message_data = dict([('Id', tuple[0]), ('Channels', tuple[1]),
                            ('Title', tuple[2]), ('Content', tuple[3]),
                            ('Tags', tuple[4]),('Markdown', tuple[5])])
        message_data_list.append(message_data)

    content_data = json.dumps(message_data_list)

    con.commit()

    return content_data, 200


@app.route("/webhook", methods=['GET', 'POST'])
def webhook_messages():
    queries = dict(request.args)

    parameter, message = parser.queryparse(queries=queries)

    if parameter == "wrong_markdown":
        return "Wrong query format", 403

    auth_res = authenticator.auth(parameter.auth_pass)

    if not auth_res:
        return "Unauthorized", 401

    msg = parser.webhookmessageparse(parameter=parameter, content=message)

    saver.save_to_db(msg)

    return "Message successfully saved to database", 200


@app.route("/", methods=['GET'])
def get_page():
    return render_template('index.html', token=(config.authorization == True))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.port)
