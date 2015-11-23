import time
import threading
from pathfinder.client.joystick_client import joystick_client
from pathfinder.client.video_client import video
import sys


class MiThread(threading.Thread):
    def __init__(self, service,
                 close_event=None,
                 shot_event=None,
                 ip="172.16.17.136"):
        threading.Thread.__init__(self)
        self.close_event = close_event
        self.shot_event = shot_event
        self.service = service
        self.ip = ip

    def run(self):
        self.service(self.close_event, self.shot_event, self.ip)


def client(ip):
    close_server = threading.Event()
    shot_event = threading.Event()
    robot_thread = MiThread(joystick_client, close_server, shot_event, ip)
    video_thread = MiThread(video, close_server, shot_event, ip)
    robot_thread.start()
    video_thread.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        close_server.set()
        robot_thread.join()
        video_thread.join()

if __name__ == '__main__':
    ip = '172.16.17.136'
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    client(ip)
