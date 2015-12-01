import socket
from mini_loki.client import client
import json


def server(ip="172.16.17.26", port=5044):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(1)
    client, _ = server.accept()
    client.settimeout(2)
    try:
        msg = client.recv(1024)
        print msg
        client.send("loki0\n")
    except socket.timeout:
        pass
    except socket.error:
        pass
    except KeyboardInterrupt:
        pass
    server.close()

if __name__ == '__main__':
    server()
    client("loki0.local")
