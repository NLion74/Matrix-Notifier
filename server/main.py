import socket
import server


def main():
    host = '127.0.0.1'
    port = '5505'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, int(port)))
    except socket.error as exception:
        print(str(exception))

    s.listen(20)

    server.start(s)


if __name__ == "__main__":
    main()
