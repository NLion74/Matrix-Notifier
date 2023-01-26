import parser
import responder
import saver


def recv(conn):
    buffer = conn.recv(4096)
    rq = parser.httparse(buffer)
    parameter = parser.headerparse(rq)

    res = responder.respond(rq, conn)

    if not res:
        return False

    msg = parser.messageparse(rq, parameter)
    print(msg)

    saver.save_to_db(msg)
    saver.clean_db()


def start(s):
    print("Waiting for incoming Connections...")
    while True:
        conn, addr = s.accept()
        print(f"connected to: {addr[0]}")

        recv(conn)

        conn.close()
