from flask import Flask, request, render_template
import sqlite3
import os
import json
import logging
from time import time

import config
import parser
import authenticator
import saver
from exit_handler import Exit

logger = logging.getLogger()

if config.coverage:
    from coverage import Coverage
    coveragedatafile = ".coverage-server-" + str(int(time()))
    cov = Coverage(data_file=f"{config.datadir_server}/coverage/{coveragedatafile}")
    cov.erase()
    cov.start()
else:
    cov = ""

exit_handler = Exit(cov)

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
        return "Wrong markdown format", 400

    auth_res = authenticator.auth(parameter.auth_pass)

    if not auth_res:
        return "Unauthorized", 401

    msg = parser.messageparse(parameter=parameter, body=body)

    id = saver.save_to_db(msg)

    msg_json = json.dumps(dict([('Id', id), ('Channels', msg.channels),
                                ('Title', msg.title), ('Content', msg.content),
                                ('Tags', msg.tags), ('Markdown', msg.markdown)]))

    return msg_json, 200


@app.route("/webhook", methods=['GET', 'POST'])
def webhook_messages():
    queries = dict(request.args)

    parameter, message = parser.queryparse(queries=queries)

    if parameter == "wrong_markdown":
        return "Wrong query format", 400

    auth_res = authenticator.auth(parameter.auth_pass)

    if not auth_res:
        return "Unauthorized", 401

    msg = parser.webhookmessageparse(parameter=parameter, content=message)

    id = saver.save_to_db(msg)

    msg_json = json.dumps(dict([('Id', id), ('Channels', msg.channels),
                                ('Title', msg.title), ('Content', msg.content),
                                ('Tags', msg.tags), ('Markdown', msg.markdown)]))

    return msg_json, 200


@app.route("/json", methods=['GET', 'POST'])
def json_messages():
    body = request.get_data()

    parameter, message = parser.jsonparse(body=body)

    if parameter == "invalid json":
        return "Invalid json", 400
    elif parameter == "message required":
        return "Message required", 400

    auth_res = authenticator.auth(parameter.auth_pass)

    if not auth_res:
        return "Unauthorized", 401

    msg = parser.webhookmessageparse(parameter=parameter, content=message)

    id = saver.save_to_db(msg)

    msg_json = json.dumps(dict([('Id', id), ('Channels', msg.channels),
                                ('Title', msg.title), ('Content', msg.content),
                                ('Tags', msg.tags), ('Markdown', msg.markdown)]))

    return msg_json, 200


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

    cur.execute(
        'SELECT * FROM (SELECT * FROM messages ORDER BY id DESC LIMIT :limit) sub ORDER BY id ASC', {"limit": parameter.limit})

    data = cur.fetchall()
    message_data_list = []
    for tuple in data:
        message_data = dict([('Id', tuple[0]), ('Channels', json.loads(tuple[1])),
                            ('Title', tuple[2]), ('Content', tuple[3]),
                            ('Tags', json.loads(tuple[4])),('Markdown', tuple[5])])
        message_data_list.append(message_data)

    content_data = json.dumps(message_data_list)

    con.commit()

    return content_data, 200


@app.route("/messages/<message_id>", methods=['GET'])
def get_message_byid(message_id):
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

    ids = parser.id_parse(message_id)

    message_data_list = []
    for id in ids:
        cur.execute(
            'SELECT * FROM messages WHERE id = :id', {"id": id})
        data = cur.fetchall()

        if not data == []:
            for tuple in data:
                message_data = dict([('Id', tuple[0]), ('Channels', json.loads(tuple[1])),
                                     ('Title', tuple[2]), ('Content', tuple[3]),
                                     ('Tags', json.loads(tuple[4])), ('Markdown', tuple[5])])
                message_data_list.append(message_data)

    if not message_data_list == []:
        content_data = json.dumps(message_data_list)

        con.commit()
        return content_data, 200
    else:
        con.commit()
        return "Id not found", 404


@app.route("/", methods=['GET'])
def get_page():
    return render_template('index.html', token=(config.authorization == True))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.port)
