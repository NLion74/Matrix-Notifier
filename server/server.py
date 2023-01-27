import threading

import parser
import responder
import saver


def recv(conn, addr):
    print(f"connected to: {addr[0]}")
    buffer = conn.recv(4096)
    rq = parser.httparse(buffer)
    parameter = parser.headerparse(rq)

    res = responder.respond(rq, conn)

    if not res:
        conn.close()
        return False

    msg = parser.messageparse(rq, parameter)

    saver.save_to_db(msg)
    saver.clean_db()

    conn.close()


def start(s):
    print("Waiting for incoming Connections...")
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=recv, args=(conn, addr))
        thread.start()

        print(f"Active Connections: {threading.active_count() - 1}")
