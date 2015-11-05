import socket
import pygame
import sys
import json
import time

JOYSTICK_MAX = -32768
JOYSTICK_MIN = 32767


def translate(value):
    value = value - (JOYSTICK_MAX + JOYSTICK_MIN)/2 / (JOYSTICK_MIN - JOYSTICK_MAX) - 1
    return value

s = socket.socket()
s.connect(("localhost", 5033))
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
        w = translate(-joystick.get_axis(2)) / 3
        clock.tick(50)
        s.send(json.dumps({'x': x, 'y': y, 'w': w}))
        time.sleep(0.15)
except KeyboardInterrupt:
    pygame.quit()
    s.send('quit')
    s.close()
    sys.exit()
pygame.quit()
