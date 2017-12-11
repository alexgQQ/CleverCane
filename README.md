# CleverCane
Senior Design Project Code Repo
University of Colorado in Denver
Authors: Alex Grand, Huong Nugyen, Robert Dunn, Katherine Falkenstine

This code is designed for the DragonBoard 410C platform but should be portable to most ARM based systems. Installation dependcies may vary if a 32-bit architecture is used or if anything under an ARM A-53 Cortex is used as the main CPU. 

This is a code repo for the CleverCane senior design project. The project is aimed at using computer vision, embedded engineering and neural networks to create a device to assist the visually impaired.
The goal in mind is to have an object detection system for head height objects not found by traditional assistance canes and a smart object detection system to navigate traffic intersection. 

The whole system uses multiprocessing to spawn processes for each subsystem. A main process will control data flow and general decision making while subprocesses run video streaming, object detection, sonar gathering and audio functionality. 

To install dependencies, run:
'''
./config/setup.sh install
'''

To check functionality, run:
'''
./config/setup.sh no-deps
'''

To start the whole system(after installing dependencies), run
'''
python run.py
'''

Each module file in the home directory can runon its own for further testing/debugging.
Stay tuned for more. 
