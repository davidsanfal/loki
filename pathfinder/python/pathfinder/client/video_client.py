import cv2
import urllib
import numpy as np
import os
import Image
import zbar

video_out = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                         'output',
                         'pathfinder.avi')


def video(close_event=None, shot_event=None,
          ip="172.16.17.26"):
    stream = urllib.urlopen('http://%s:8080/?action=stream' % ip)
    frame = ''
    cv2.namedWindow('LOKI Pathfinder', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('LOKI Pathfinder', 640, 480)
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    video = cv2.VideoWriter(video_out, fourcc, 15, (640, 480))

    scanner = zbar.ImageScanner()
    scanner.parse_config('enable')
    qr_url = []
    while True:
        if close_event and close_event.is_set():
            break
        frame += stream.read(1024)
        a = frame.find('\xff\xd8')
        b = frame.find('\xff\xd9')
        if a != -1 and b != -1:
            jpg = frame[a:b+2]
            frame = frame[b+2:]
            img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
            video.write(img)
            cv2.imshow('LOKI Pathfinder', img)
            if cv2.waitKey(1) == 27:
                pass
            if shot_event and shot_event.is_set():
                shot_event.clear()
                qr_scanner(img, scanner, qr_url)
            else:
                qr_url = []

    video.release()
    # face_recognice()
    cv2.destroyAllWindows()


def qr_scanner(img, scanner, qr_url):
    img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    pil = Image.fromarray(img).convert('L')
    width, height = pil.size
    raw = pil.tostring()
    image = zbar.Image(width, height, 'Y800', raw)
    scanner.scan(image)
    for symbol in image:
        url = symbol.data
        if url not in qr_url:
            os.system("sensible-browser %s" % url)
            qr_url.append(url)


def face_recognice():
    face_out = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'output',
                            'face.avi')
    cascPath = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'haarcascade_frontalface_default.xml')
    faceCascade = cv2.CascadeClassifier(cascPath)
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    video = cv2.VideoWriter(face_out, fourcc, 15, (640, 480))
    cap = cv2.VideoCapture(video_out)
    while cap.isOpened():
        _, frame = cap.read()
        if frame is None:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        video.write(frame)
    video.release()
    cap.release()
    print "face_recognice Ended"
