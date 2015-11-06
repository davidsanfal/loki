import socket
import json
import psutil
import subprocess
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
    subp = subprocess.Popen(['./mjpg_streamer', '-i', './input_uvc.so -f 15 -r 640x480 -n', '-o' ,'./output_http.so -w ./www'],
                            cwd='/root/mjpg-streamer',
                            shell=False,
                            stdin=None,
                            stdout=None,
                            stderr=None,
                            close_fds=True)
    streaming = psutil.Process(subp.pid)
    while True:
        server.listen(1)
        robot = Pathfinder()
        robot.move(0, 0, 0)
        client, _ = server.accept()
        client.settimeout(2)
        print "MOVING ..."
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
        except KeyboardInterrupt:
            pass
        robot.move(0, 0, 0)
    streaming.kill()
    server.close()

if __name__ == '__main__':
    robot_server()
