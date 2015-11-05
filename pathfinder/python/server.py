import threading
from pathfinder_services import robot_server, video_server


class MiThread(threading.Thread):
    def __init__(self, service, event=None):
        threading.Thread.__init__(self)
        self.event = event
        self.service = service

    def run(self):
        self.service(self.event)

close_server = threading.Event()
try:
    robot = MiThread(robot_server, close_server)
    video = MiThread(video_server, close_server)

    robot.start()
    video.start()
    robot.join()
    video.join()
except KeyboardInterrupt:
    close_server.set()
