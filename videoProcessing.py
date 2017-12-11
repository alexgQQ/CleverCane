import cv2
import os
import sys

from multiprocessing import Process, Queue

def prepareImage(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
    return image

def streamVideo(outputQueue):
    video = cv2.VideoCapture(0)
    succ, frame = video.read()

    while succ:
        frame = prepareImage(frame)
        outputQueue.put(frame)

    video.release()

if __name__ == "__main__":
    q = Queue()
    p = Process(target=streamVideo, args=(q,))

    p.start()
    while True:
        received = q.get(True)
        print "\n Received:"
        print len(received)
        print type(received)
    p.join()
