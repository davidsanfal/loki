import socket
import json


def organizer_server(ip="172.16.17.57", port=5044, robots=None, close_event=None):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.settimeout(2)
    while True:
        try:
            server.listen(1)
            client, _ = server.accept()
            client.settimeout(2)
            try:
                msg = client.recv(1024)
                robot_dns = "loki_%s" % len(robots)
                info = json.loads(msg)
                robots[robot_dns] = info
                client.send("%s\n" % robot_dns)
            except socket.timeout:
                pass
            except socket.error:
                pass
            if close_event.is_set():
                break
        except socket.timeout:
            pass
        if close_event.is_set():
            break
    server.close()
