from _collections import defaultdict
import time
import threading
from mini_loki.swarm_organizer import organizer_server
from mini_loki.client import client


robots = defaultdict()
close_all = False


class MiThread(threading.Thread):
    def __init__(self, service,
                 close_event=None,
                 ip="172.16.17.136",
                 port=5044):
        threading.Thread.__init__(self)
        self.close_event = close_event
        self.service = service
        self.ip = ip
        self.port = port

    def run(self):
        self.service(self.ip, self.port, robots, self.close_event)


def overmind(ip):
    close_all = threading.Event()
    organizer_thread = MiThread(organizer_server, close_all, ip)
    client_thread = MiThread(client, close_all, "loki_0.local", 80)
    organizer_thread.start()
    client_thread.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        close_all.set()
        organizer_thread.join()
        client_thread.join()


if __name__ == '__main__':
    overmind("172.16.17.57")
    print robots
