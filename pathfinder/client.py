import socket
import pygame
import sys
import json


keys = {'a': False,
        's': False,
        'd': False,
        'w': False,
        'q': False,
        'e': False}

s = socket.socket()
s.connect(("172.16.17.26", 8090))
pygame.init()
WIDTH = 440
HEIGHT = 440
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)


while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.constants.QUIT:
            pygame.quit()
            s.send('quit')
            s.close()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            if key in keys.keys():
                keys[key] = 1
            s.send(json.dumps(keys))
        elif event.type == pygame.KEYUP:
            key = pygame.key.name(event.key)
            if key in keys.keys():
                keys[key] = 0
            s.send(json.dumps(keys))
