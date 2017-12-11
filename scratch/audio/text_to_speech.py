from gtts import gTTS
import os
import argparse
import sys


def runAudio(type, value):
    if type == "startup":
        text = "System starting up..."
    elif type == "setup":
        text = "Audio configured..."
    elif type == "sonar":
        text = "Object Overhead"
    elif type == "approach-traffic":
        if value == 0:
            text = "Approaching Traffic Intersection"
        elif value != 0:
            text = "Traffic Intersection ahead at " + str(args.dist) + " feet"

    tts = gTTS(text=text, lang='en')
    tts.save("/home/linaro/jobs/audio/buff.mp3")
    os.system("mpg321 /home/linaro/jobs/audio/buff.mp3")