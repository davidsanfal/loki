import socket
import pygame


def client(ip="loki.local", port=80):

    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    s = socket.socket()
    s.connect((ip, port))
    while True:
        clock = pygame.time.Clock()
        for _ in pygame.event.get():
            pass
        clock.tick(50)
        y = float(joystick.get_axis(0))
        x = float(joystick.get_axis(1))
        w = float(joystick.get_axis(2))
        s.send("%.2f,%.2f,%.2f,\n" % (x, y, w))
    s.close()
    pygame.quit()

if __name__ == '__main__':
    client()
