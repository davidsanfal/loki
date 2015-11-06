import time
import threading
from pathfinder.client.joystick_client import joystick
from pathfinder.client.video_client import video


class MiThread(threading.Thread):
    def __init__(self, service, event=None):
        threading.Thread.__init__(self)
        self.event = event
        self.service = service

    def run(self):
        self.service(self.event)


def client():

    close_server = threading.Event()
    robot_thread = MiThread(joystick, close_server)
    video_thread = MiThread(video, close_server)
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
    client()
