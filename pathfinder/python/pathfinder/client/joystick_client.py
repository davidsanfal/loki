import socket
import pygame
import sys
import json

JOYSTICK_MAX = -32768
JOYSTICK_MIN = 32767

TCP_IP = "172.16.17.26"
TCP_PORT = 5033


def translate(value):
    value = value - (JOYSTICK_MAX + JOYSTICK_MIN)/2 / (JOYSTICK_MIN - JOYSTICK_MAX) - 1
    return value


def joystick(thread_event=None):

    s = socket.socket()
    s.connect((TCP_IP, TCP_PORT))
    pygame.init()
    clock = pygame.time.Clock()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    while True:
        if thread_event and thread_event.is_set():
            break
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                break
        y = translate(-joystick.get_axis(0))
        x = translate(-joystick.get_axis(1))
        w = translate(-joystick.get_axis(2)) / 3
        clock.tick(50)
        s.send(json.dumps({'x': x, 'y': y, 'w': w}))
    pygame.quit()
    s.send('quit')
    s.close()
    sys.exit()