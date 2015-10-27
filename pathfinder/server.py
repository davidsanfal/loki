import socket
import json
from pathfinder import Pathfinder
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("172.16.17.26", 8090))
server.listen(1)
robot = Pathfinder()
client, addr = server.accept()
client.settimeout(5)
while True:
    msg = client.recv(1024)
    if msg == "quit":
        break
    else:
        try:
            msg = json.loads(msg)
            robot.move(msg['x'], msg['y'], msg['w'],)
        except ValueError:
            pass

server.close()
