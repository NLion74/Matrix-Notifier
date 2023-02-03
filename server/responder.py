import sqlite3
import os
import json

import config


def respond(rq, conn):
    if rq.method == "POST":
        if rq.body == "":
            status_line = "HTTP/1.1 200 OK"
            content = "Cannot deliever empty message\n"
            content_length = len(content)
            content_type = "text/plain"
            response = f"{status_line}\\r\\nContent-Length: {content_length}\r\nContent-Type: {content_type}\r\n\r\n{content}\r\n"
            conn.sendall(bytes(response, 'utf-8'))
            return False
        else:
            status_line = "HTTP/1.1 200 OK"
            content = "Successfully delievered message\n"
            content_length = len(content)
            content_type = "text/plain"
            response = f"{status_line}\\r\\nContent-Length: {content_length}\r\nContent-Type: {content_type}\r\n\r\n{content}\r\n"
            conn.sendall(bytes(response, 'utf-8'))
            return True
    if rq.method == "GET":
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
            message_data = dict([('Id', tuple[0]), ('Channel', tuple[1]), ('Title', tuple[2]), ('Content', tuple[3])])
            message_data_list.append(message_data)

        content_data = json.dumps(message_data_list)

        con.commit()

        status_line = "HTTP/1.1 200 OK"
        content = content_data
        content_length = len(content)
        content_type = "text/plain"
        response = f"{status_line}\\r\\nContent-Length: {content_length}\r\nContent-Type: {content_type}\r\n\r\n{content}\r\n"
        conn.sendall(bytes(response, 'utf-8'))
        return False
    else:
        status_line = "HTTP/1.1 405 Method Not Allowed"
        content = "Method Not Allowed"
        content_length = len(content)
        content_type = "text/plain"
        response = f"{status_line}\\r\\nContent-Length: {content_length}\r\nContent-Type: {content_type}\r\n\r\n{content}\r\n"
        conn.sendall(bytes(response, 'utf-8'))
        return False
