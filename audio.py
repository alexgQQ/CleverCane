from gtts import gTTS
import os
import argparse
import sys
from colors import _H_AUDIO


def runText(type, value):
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
    elif type == "approach-stop-sign":
        if value == 0:
            text = "Stop Sign ahead"
        elif value != 0:
            text = "Stop Sign ahead at " + str(args.dist) + " feet"

    tts = gTTS(text=text, lang='en')
    tts.save("/home/linaro/jobs/buff.mp3")
    os.system("mpg321 /home/linaro/jobs/buff.mp3")

if __name__ == "__main__":

    from multiprocessing import Process, Queue

    print _H_AUDIO + "Running Audio Test"
    print _H_AUDIO + "Testing Pulse Audio..."
    cmd = ["amixer -c 0 cset iface=MIXER,name='RX3 MIX1 INP1' 'RX1'",
            "amixer -c 0 cset iface=MIXER,name='SPK DAC Switch' 1",
            "aplay -c 1 -D plughw:0,1 'piano.wav'"]
    for call in cmd:
        os.system(call)

    print _H_AUDIO + "Testing Text to Speech Engine..."
    runText("setup", 0)

    print _H_AUDIO + "Testing Audio Process Spawn..."
    p = Process(target=runText, args=("setup", 0,))
    p.start()
    p.join()

    print _H_AUDIO + "Audio Test Complete"