# Name: Survvi.py
# Author: MS. Kingon
# Date: 29-01-2017
# Description: A survaliance App for any desktop or other divice running OpenCV 3.0.0 with Python 2.7+
# Key-Features: monitors a set feild and will inform the user of movment. 
#		- Should ultimatly email/text the master with a img.
#			- will need api access for sms/watsapp
#			- should ignore leaving room?
#			- needs to be carefull with door movment (ie door opens but no one comes in/goes out)
#		- Use feature recognition to determine what entered the room (human/cat/dog/car/ball/tennis-racket/jet etc)
#			- should ignore small objects cats/dogs etc
#			- 
#		- Use facial recocnition to determine whom entered the and greet them.
#		- add database dependancy so facial recognition can learn and train itself with people coming and going. 
#			- Asking master for clarification whom people are that its spotted (at end of day)


# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2
import time
import sys
import os
# add personal modules for survvi to python path
sys.path.append(os.path.abspath('/home/shane/Documents/ImageProcc/survvi/scripts/survvi_modules'))

# import personal modules
from survvi_motion_analysis import *

# construct the argument parse and parse the arguments to controll behaviour of survvi on launch.
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--display", type=int, default=1,
	help="Whether or not frames should be displayed")
ap.add_argument("-nm", "--notify-master", type=bool, default=False,
	help="Should survvi notify master of intruders?")
args = vars(ap.parse_args())


# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] Survvi is sampling THREADED frames from webcam...")

# threaded version:
vs = WebcamVideoStream(src=0).start()


# non-threaded version
# camera = cv2.VideoCapture(0)

fps = FPS().start()
strt_timer = time.time();
disp_state = 2;	# display_state 0:	Stop displaying images
		# display_state 1:	display images
		# display_state 2:	Idle


# loop over frames...this time using the threaded stream
# wait 5 seconds to fetch initial frame
while ((time.time() - strt_timer) <= 2):
	bg_frame = gray_image(vs.read());

# reset timer:
strt_timer = -1.0;
while (1==1):
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	
	frame = vs.read();

	gray_frame = gray_image(frame);
	
 	(motion, gray_frame) = motion_detected(bg_frame, gray_frame);

	# handle 2s timer for display.
	if (strt_timer >= 0.0) and ((time.time() - strt_timer) <= 2.0):
		# still on timer
		# print(time.time()-strt_timer);
		# print ();
		if (motion > 0):
			# we also detect motion so reset timer:
			strt_timer = time.time();
	else:
		if (motion < 0):
			# update background image with latest static image
			if(disp_state != 2):
				disp_state = 0;				# stop displaying frame
		else:
			# else set disp timer to 10s 
			strt_timer = time.time();
        	       	print("[WARNING] Survvi has detected motion from webcam... ");
			disp_state = 1;	# start displaying frame
	
	# check to see if motion  should be displayed to our screen
	if (args["display"] > 0) and (disp_state == 1):
		cv2.imshow("Camera Feed", frame)
		cv2.imshow("Survvi Feed", gray_frame);
		key = cv2.waitKey(1) & 0xFF
	elif (disp_state == 0): 
		# clear screen now that we no longer show images
	 	print("[INFO] Survvi detects no motion from webcam... ");
		cv2.destroyAllWindows();
 		disp_state = 2;
	elif (disp_state == 2):
		pass;
		key = cv2.waitKey(1) & 0xFF;

	# bg_frame = gray_frame;
	# update the FPS counter
	fps.update()
 
# stop the timer and display FPS information
fps.stop()
print("[INFO] Survvi up-time: {:.2f}".format(fps.elapsed()))
print("[INFO] Survvi approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
# camera.stop();
