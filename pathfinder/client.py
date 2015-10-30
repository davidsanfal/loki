import socket
import pygame
import sys
import json


def translate(value):
    value = value - (-32768 + 32767)/2 / (32767 + 32768) - 1
    return value

s = socket.socket()
s.connect(("172.16.17.26", 8090))
try:
    pygame.init()
    clock = pygame.time.Clock()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                pygame.quit()
                s.send('quit')
                s.close()
                sys.exit()
        y = translate(-joystick.get_axis(0))
        x = translate(-joystick.get_axis(1))
        w = translate(-joystick.get_axis(2)) / 2
        clock.tick(50)
        s.send(json.dumps({'x': x, 'y': y, 'w': w}))
except KeyboardInterrupt:
    pygame.quit()
    s.send('quit')
    s.close()
    sys.exit()
pygame.quit()
