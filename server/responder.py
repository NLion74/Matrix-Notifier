import sqlite3
import os
import json


def respond(rq, conn):
    if rq.method == "POST":
        if rq.body == "":
            status_line = "HTTP/1.1 200 OK"
            content = "Cannot deliever empty message"
            content_length = len(content)
            content_type = "text/plain"
            response = f"{status_line}\\r\\nContent-Length: {content_length}\r\nContent-Type: {content_type}\r\n\r\n{content}"
            conn.sendall(bytes(response, 'utf-8'))
            return False
        else:
            status_line = "HTTP/1.1 200 OK"
            content = "Successfully delievered message"
            content_length = len(content)
            content_type = "text/plain"
            response = f"{status_line}\\r\\nContent-Length: {content_length}\r\nContent-Type: {content_type}\r\n\r\n{content}"
            conn.sendall(bytes(response, 'utf-8'))
            return True
    if rq.method == "GET":
        if not os.path.exists("./database"):
            os.mkdir("./database")
        con = sqlite3.connect("./database/messages.db")
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS messages (id INT PRIMARY KEY, title text, content text)''')

        cur.execute('''SELECT * FROM messages''')
        data = cur.fetchall()
        content_data = json.dumps(data)

        con.commit()

        status_line = "HTTP/1.1 200 OK"
        content = content_data
        content_length = len(content)
        content_type = "text/plain"
        response = f"{status_line}\\r\\nContent-Length: {content_length}\r\nContent-Type: {content_type}\r\n\r\n{content}"
        conn.sendall(bytes(response, 'utf-8'))
        return False
    else:
        status_line = "HTTP/1.1 405 Method Not Allowed"
        content = "Method Not Allowed"
        content_length = len(content)
        content_type = "text/plain"
        response = f"{status_line}\\r\\nContent-Length: {content_length}\r\nContent-Type: {content_type}\r\n\r\n{content}"
        conn.sendall(bytes(response, 'utf-8'))
        return False
