import socket
import json
from pathfinder import Pathfinder

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("172.16.17.26", 8090))
server.listen(1)
robot = Pathfinder()
robot.move(0, 0, 0)
client, addr = server.accept()
client.settimeout(2)
try:
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
except socket.timeout:
    print("timeout error")
    robot.move(0, 0, 0)
except socket.error:
    print("socket error occured: ")
    robot.move(0, 0, 0)
robot.move(0, 0, 0)
server.close()
