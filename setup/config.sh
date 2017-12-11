#!/bin/bash

BLUE='\033[1;34m'
NC='\033[0m'
HEAD="[${BLUE}SOURCES${NC}]"
HOME="/home/linaro/jobs"
SRC="${HOME}/sources"
AUDIO="${HOME}/audio"
TTS="${AUDIO}/text-to-speech.py"
TF_API_LOC="${SRC}/models/research"
TF_BASE_LOC="${SRC}/tf-whl-install"

TF_MODELS_REPO="https://github.com/tensorflow/models.git"

function err_check {
	RED='\033[0;31m'
	GREEN='\033[0;32m'
	ER="[${RED}ERROR${NC}]"
	OK="[${GREEN}OK${NC}]"
	if [ $? -ne 0 ] 
	then
		echo -e  "$HEAD - $* check - $ER"
	fi
	echo -e  "$HEAD - $* check - $OK"
}

function tf_check {
	HEAD="[${BLUE}TENSORFLOW${NC}]"
	echo -e  "$HEAD - Checking Tensorflow..."
	python test-tf.py $TF_API_LOC
}

function tf_base_install {
	HEAD="[${BLUE}TENSORFLOW INSTALLING${NC}]"
	cd $TF_BASE_LOC
	sudo pip install tensorflow-1.4.0-cp27-none-any.whl ; err_check "TF Base Install"
	sudo pip install numpy > /dev/null ; err_check 'numpy'
	tf_check
	return 0
}

function tf_api_install {
	HEAD="[${BLUE}TENSORFLOW API INSTALLING${NC}]"
	cd $TF_API_LOC
	protoc object_detection/protos/*.proto --python_out=. ; err_check "Google Protobuf Config"
	export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim ; err_check "Slim Enviroment Config"
#	echo -e  "export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim" >> ~/.bashrc ; err_check "Slim Enviroment Config"
	return 0
}

function dep_install {
	echo -e  "$HEAD - Checking Sources..."
	sudo apt-get -qq -y update; err_check 'system update'

	sudo apt-get -qq -y install python-pip ; err_check 'python-pip'
	sudo apt-get -qq -y install python-dev ; err_check 'python-dev'
	sudo apt-get -qq -y install python-pil ; err_check "python-pil"
	sudo apt-get -qq -y install python-lxml ; err_check "python-lxml"
	sudo apt-get -qq -y install python-matplotlib ; err_check "python-matplotlib"
	sudo apt-get -qq -y install python-opencv ; err_check "python-opencv"
	sudo apt-get -qq -y install python-tk ; err_check "python-tk"
	sudo apt-get -qq -y install swig ; err_check "swig"
	sudo apt-get -qq -y install protobuf-compiler ; err_check 'protobuf-compiler'

	sudo pip install setuptools > /dev/null ; err_check 'setuptools'
	sudo pip install wheel > /dev/null ; err_check 'wheel'
	sudo pip install numpy > /dev/null ; err_check 'numpy'
	sudo pip install jupyter > /dev/null ; err_check 'jupyter'

	sudo apt-get -qq -y install mpg123 ; err_check 'mpg123'
	sudo apt-get -qq -y install mpg321 ; err_check 'mpg321'

	sudo pip install gTTS > /dev/null ; err_check 'gTTS'

	sudo pip install imutils > /dev/null ; err_check 'gTTS'
}

function audio_config {
	HEAD="[${BLUE}AUDIO${NC}]"
	echo -e  "$HEAD - Starting Config..."
	amixer -c 0 cset iface=MIXER,name='RX3 MIX1 INP1' 'RX1'; err_check 'amixer0'
	amixer -c 0 cset iface=MIXER,name='SPK DAC Switch' 1; err_check 'amixer1'
	aplay -c 1 -D plughw:0,1 "${AUDIO}/piano.wav"; err_check 'aplay piano'
	python "$AUDIO/test.py"
}

function cv_check {
	HEAD="[${BLUE}OPENCV${NC}]"
	echo -e  "$HEAD - Checking OpenCV..."
	python test-opencv.py
}

if [ "$1" == "install" ] 
then
	dep_install
	tf_base_install
	tf_api_install
	exit 0
fi

if [ "$1" == "config" ] 
then
	dep_install
	audio_config
	cv_check
	tf_check
	exit 0
fi

if [ "$1" == "no-deps" ]
then
	audio_config
	cv_check
	tf_check
	exit 0
fi