import os
import socket

import server
import config


def main():
    host = "0.0.0.0"
    port = config.port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, int(port)))
    except socket.error as exception:
        print(str(exception))

    s.listen(20)

    server.start(s, host, port)


if __name__ == "__main__":
    main()
