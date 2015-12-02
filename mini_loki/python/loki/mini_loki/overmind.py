import socket
from mini_loki.client import client
import json
from _collections import defaultdict
from time import sleep

robots = defaultdict()
close_all = False


def server(ip="172.16.17.52", port=5044):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(1)
    client, _ = server.accept()
    client.settimeout(2)
    robot_dns = None
    try:
        msg = client.recv(1024)
        print msg
        robot_dns = "loki_%s" % len(robots)
        robots[robot_dns] = json.loads(msg)
        print robots
        client.send("%s\n" % robot_dns)
    except socket.timeout:
        pass
    except socket.error:
        pass
    except KeyboardInterrupt:
        close_all = True
    server.close()
    return robot_dns

if __name__ == '__main__':
    while not close_all:
        robot_dns = server()
        sleep(1)
        if robot_dns:
            client("%s.local" % robot_dns)
