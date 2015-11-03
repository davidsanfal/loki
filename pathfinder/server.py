import socket
import json
from pathfinder import Pathfinder

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("192.168.10.10", 8090))
server.listen(1)
robot = Pathfinder()
robot.move(0, 0, 0)
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
robot.move(0, 0, 0)
server.close()
