import os
import sys
import subprocess as sp
import pickle
import tensorflow as tf
import cv2

from multiprocessing import Process, Queue
from objectDetection import *
from sonar import *
from audio import *
from videoProcessing import *
from colors import _H_DETECT, _H_MAIN, _H_AUDIO, _H_SONAR

savedFileTag = 0

#rotate image imutils.rotate_bound(img, angle)

class timer:
    def __init__(self, ID):
        self.timeStart = 0
        self.timeStop = 0
        self.ID = ID

    def start(self):
        self.timeStart = time.time()

    def stop(self):
        self.timeStop = time.time()

    def report(self):
        print("TIMER [" + self.ID + "] REPORTS: " + str(self.timeStop-self.timeStart) + "seconds")

def annotateImage(image, text):
    height, width, channel = image.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image,text, (20,height-20), font, 2, (0, 255, 0), 5, cv2.LINE_AA)
    return image

def saveImage(image):
    base = "/home/linaro/jobs/saved_images/"
    tag = "savedImage-" + str(savedFileTag)
    cv2.imwrite(base+tag, image)
    savedFileTag += 1

def runAudio(alertType, distance):
    audioProcess = Process(target=runText, args=(alertType, distance,))
    audioProcess.start()
    audioProcess.join()

def visualizeImage(image, )

#videoQueue = Queue()
#videoProcess = Process(target=streamVideo, args=(videoQueue,))

#detectQueue = Queue()
#detectProcess = Process(target=runDetect, args=(videoQueue, detectQueue, False,))

print _H_MAIN + "Creating Detection Processes"
video = cv2.VideoCapture(0)
detectQueue = Queue()
visualizeQueue = Queue()
detectProcess = Process(target=singleStream, args=(video, detectQueue, True, visualizeQueue,))

print _H_MAIN + "Creating Sonar Processes"
sonarPort = "/dev/ttyUSB0"
sonarQueue = Queue()
sonarProcess = Process(target=streamSonar, args=(sonarPort, sonarQueue, 0,))

print _H_MAIN + "Starting Processes"
detectProcess.start()
sonarProcess.start()

SHOW_DETECTION = True

while True:
    loopTimer = timer("LOOP")
    loopTimer.start()

#    detData = detectQueue.get(True)
#    detPair = detData[0]
#    detNum = detData[1]
#    foundItems = processDetect(detPair[0], detPair[1])

    detNum = detectQueue.get(True)
    detBoxes = detectQueue.get(True)
    detClasses = detectQueue.get(True)
    detScores = detectQueue.get(True)

    if SHOW_DETECTION:
        detImg = visualizeQueue.get(True)
        visImg = visualizeDetection(detImg, detBoxes, detScores, detClasses, detNum)

#        cv2.namedWindow("Main")
#        cv2.imshow("Main", visImg)

#        if cv2.waitKey(1) & 0xFF == ord('q'):
#                SHOW_DETECTION = False
#                cv2.destroyAllWindows()


    foundItems = processDetect(detClasses, detScores)


    sonarData = sonarQueue.get(True)

    search = [ "person",
            "tv"]

#    search = ["stop_sign",
#            "stop_light",
#            "green_light",
#            "pedestrian_crossing",
#            "pedestrian_stop"]

    detected = {}
    for item in search:
        detected[item] = foundItems.count(item)
        print _H_DETECT + "Found " + str(detected[item]) + " " + str(item)

    print _H_SONAR + str(sonarData)

    annotationTag = "Sonar: " + str(sonarData) + " -- Trigger: approach-stop-sign"

    if detected[search[0]] > 0:
        runAudio("approach-stop-sign", 0)
        if SHOW_DETECTION:
            saveImage(annotateImage(visImg, annotationTag))
    if detected[search[1]] > 1 or detected[search[2]] > 1:
        runAudio("approach-traffic", 0)
        if SHOW_DETECTION:
            saveImage(annotateImage(visImg, annotationTag))
    if sonarData < 100:
        runAudio("sonar", 0)

    loopTimer.stop()
    loopTimer.report()