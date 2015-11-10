import socket
import json
import pygame


def joystick_client(close_event=None, shot_event=None,
                    ip="172.16.17.26", port=5033):
    
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    s = socket.socket()
    s.connect((ip, port))
    while True:
        clock = pygame.time.Clock()
        if close_event and close_event.is_set():
            break
        for _ in pygame.event.get():
            pass
        clock.tick(50)
        if joystick.get_button(0):
            if shot_event:
                shot_event.set()
        y = float(-joystick.get_axis(0))
        x = float(-joystick.get_axis(1))
        w = float(-joystick.get_axis(2)) / 3
        s.send(json.dumps({'x': x,
                           'y': y,
                           'w': w}))
    s.send('quit')
    s.close()
    pygame.quit()
