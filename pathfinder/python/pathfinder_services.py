import socket
import json
try:
    from pathfinder import Pathfinder
except:
    print "Pathfinder Fake!"

    class Pathfinder(object):
        def move(self, x, y, w):
            print x, y, w
import cv2
import numpy

# TCP_IP = "172.16.17.26"
TCP_IP = "localhost"
TCP_ROBOT_PORT = 5033
TCP_VIDEO_PORT = 5034


def robot_server(event=None):
    print "robot_server launched"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((TCP_IP, TCP_ROBOT_PORT))
    while True:
        server.settimeout(0.1)
        try:
            server.listen(1)
            robot = Pathfinder()
            robot.move(0, 0, 0)
            client, _ = server.accept()
            client.settimeout(2)
            try:
                while True:
                    print event.is_set()
                    msg = client.recv(1024)
                    if event and event.is_set():
                        break
                    if msg == "quit":
                        event.set()
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
        except socket.timeout:
            print "PUES NADA, A ESPERAR"
        if event and event.is_set():
            break
    server.close()


def video_server(event=None):
    print "video_server launched"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((TCP_IP, TCP_VIDEO_PORT))
    while True:
        server.listen(1)
        client, _ = server.accept()
        try:
            capture = cv2.VideoCapture(1)
            while True:
                if event and event.is_set():
                    break
                _, frame = capture.read()
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                _, imgencode = cv2.imencode('.jpg', frame, encode_param)
                data = numpy.array(imgencode)
                stringData = data.tostring()
                client.send(str(len(stringData)).ljust(16))
                client.send(stringData)
        except socket.error:
            print "video_server, socket.error"
        client.close()
        if event and event.is_set():
            break
    server.close()
