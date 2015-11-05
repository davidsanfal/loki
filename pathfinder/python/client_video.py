#!/usr/bin/python
import socket
import cv2
import numpy

TCP_IP = 'localhost'
TCP_PORT = 5034


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))
while True:
    length = recvall(sock, 16)
    stringData = recvall(sock, int(length))
    data = numpy.fromstring(stringData, dtype='uint8')
    decimg = cv2.imdecode(data, 1)
    cv2.imshow('SERVER', decimg)
    cv2.waitKey(10)
sock.close()
cv2.destroyAllWindows()
