from gtts import gTTS
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("dist")
parser.add_argument("type")

args = parser.parse_args()

if args.type == "sonar":
    text = "Object Overhead"
elif args.type == "approach":
    text = "Approaching Traffic Intersection"
else:
    text = "Traffic Intersection ahead at " + str(args.dist) + " feet"

tts = gTTS(text=text, lang='en')
tts.save("buff.mp3")

os.system("mpg321 buff.mp3")
