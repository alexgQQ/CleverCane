import os
import sys

class bcol:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

HEAD = "[" + bcol.OKBLUE + "OPENCV" + bcol.ENDC + "]"

def err_check(str, err):
    OK = "[" + bcol.OKGREEN + "OK" + bcol.ENDC + "]"
    ERR = "[" + bcol.FAIL + "ERROR" + bcol.ENDC + "]"

    if err == False:
        print HEAD + str + OK
    elif err == True:
        print HEAD + str + ERR
    return 0

try:
    import cv2
    version = cv2.__version__
    err_check(" OpenCV importing ", False)
    err_check(" OpenCV Version " + version + " ", False)
except:
    err_check(" OpenCV importing ", True)
#    sys.exit(-1)

try:
	cv2.VideoCapture(0)
	err_check(" Video Stream ", False)
except:
	err_check(" Video Stream ", True)