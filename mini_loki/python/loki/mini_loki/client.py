import socket
import pygame
import time


def client(ip="loki_0.local", port=80, robots=None, close_event=None):

    while len(robots) < 1:
        if close_event.is_set():
            return
        time.sleep(0.1)
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    s = socket.socket()
    time.sleep(1)
    s.connect((ip, port))
    try:
        while True:
            clock = pygame.time.Clock()
            for _ in pygame.event.get():
                pass
            clock.tick(50)
            y = float(joystick.get_axis(0))
            x = float(joystick.get_axis(1))
            w = float(joystick.get_axis(2))
            if joystick.get_button(6) and not joystick.get_button(7):
                x, y, w = 0.00, -1.00, 0.50
            if joystick.get_button(7) and not joystick.get_button(6):
                x, y, w = 0.00, 1.00, -0.50
            s.send("%.2f,%.2f,%.2f,\n" % (x, y, w))
            if close_event.is_set():
                break
    except socket.error:
        pass
    s.close()
    pygame.quit()

if __name__ == '__main__':
    client()
