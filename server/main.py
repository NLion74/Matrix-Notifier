import socket
import os

import server


def main():
    host = '0.0.0.0'
    port = '5505'

    docker = os.environ.get('docker', False)
    if docker:
        port = os.environ.get('port', False)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, int(port)))
    except socket.error as exception:
        print(str(exception))

    s.listen(20)

    server.start(s, host, port)


if __name__ == "__main__":
    main()
