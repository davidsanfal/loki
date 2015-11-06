import cv2
import urllib
import numpy as np
import socket
import pygame
import sys
import json
import time

JOYSTICK_MAX = -32768
JOYSTICK_MIN = 32767

TCP_IP = "172.16.17.26"
TCP_PORT = 5033


def translate(value):
    value = value - (JOYSTICK_MAX + JOYSTICK_MIN)/2 / (JOYSTICK_MIN - JOYSTICK_MAX) - 1
    return value

s = socket.socket()
s.connect((TCP_IP, TCP_PORT))
stream = urllib.urlopen('http://192.168.10.10:8080/?action=stream')
frame = ''

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
        # time.sleep(0.15)
        frame += stream.read(1024)
        a = frame.find('\xff\xd8')
        b = frame.find('\xff\xd9')
        if a != -1 and b != -1:
            jpg = frame[a:b+2]
            frame = frame[b+2:]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
            cv2.imshow('i', i)
            if cv2.waitKey(1) == 27:
                exit(0)
except KeyboardInterrupt:
    pygame.quit()
    s.send('quit')
    s.close()
    sys.exit()
pygame.quit()
