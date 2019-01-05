# Python-face-recognition-door-opener-rasperry-pi
Python face recognition door opener with simple GUI interface built with Raspberry Pi 3, PiCamera and servo.

This project is made to learn myself and others about, face recognition, GPIO controlling
from the raspberry pi.

Hardware needed:
-Raspberry Pi (Monitor,keyboard and mouse)
-Raspberry Pi Camera Module.(I used a cheap one from aliexpress)
-Servo aviable to rotate 180 degrees.

To build the unlocker to f.eks. put on your door you would need an 3d-printer or skills to 
design and build a housing from scratch to mount on the doorlock.

Software needed:
-OpenCv3, link to install the OpenCv i used in the project:
	-https://www.life2coding.com/install-opencv-3-4-0-python-3-raspberry-pi-3/
	-Program must be run in virtual enviroment.
	-To run program see file, run.txt
-Packages:
	-face_recognition
	-argparse
	-pickle
	-RPi.GPIO
	-time
	-pickle
	-dlib
        -tkinter
        -RPi.GPIO

The setup i used to connect the servo: (see pictures)
	-When holding the GPIO pins towards yourself.
	-RED cable on the most right, lower corner.
	-BLACK on the fifth upper pin from right to left.
	-YELLOW/WHITE the pin just left to the BLACK cable.

NB: Before you can use this program you need to make an encodings.pickle file. 
	1.) Put 20+ pictures of yourself in a folder named your name into dataset.
	2.) Encode the faces by running in the virural enviroment and using the following command.
		python /home/pi/Desktop/face-recognition-door-opener-raspberry-pi/encode_faces.py 
			--dataset /home/pi/Desktop/face-recognition-door-opener-raspberry-pi/dataset
			-- encodings /home/pi/Desktop/face-recognition-door-opener-raspberry-pi/encodings.pickle
	    NB:This command can only be used if the files are put on the rasbian desktop!

To learn about face recognition i used the courses by Adrian at PyImageSearch
