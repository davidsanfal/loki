import socket
import json
try:
    from pathfinder.robot.pathfinder import Pathfinder
except:
    print "Pathfinder Fake!"

    class Pathfinder(object):
        def move(self, x, y, w):
            print x, y, w

TCP_IP = "172.16.17.26"
TCP_ROBOT_PORT = 5033


def robot_server():
    print "robot_server launched"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((TCP_IP, TCP_ROBOT_PORT))
    while True:
        server.listen(1)
        robot = Pathfinder()
        robot.move(0, 0, 0)
        client, _ = server.accept()
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
            print "robot_server, socket.timeout"
        except socket.error:
            print "robot_server, socket.error"
        robot.move(0, 0, 0)
        client.close()
    server.close()

if __name__ == '__main__':
    robot_server()
