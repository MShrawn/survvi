# Name survvi_motion_analysis.py
# Author: MS. Kingon
# date: 29-01-2017

# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2


def motion_detected(bg_frame, gray):
	# detects motion against a provided background image.
	# resize the frame, convert it to grayscale, and blur it

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(bg_frame, gray)
	thresh = cv2.threshold(frameDelta, 30, 255, cv2.THRESH_BINARY)[1]
	# thresh = cv2.adaptiveThreshold(frameDelta,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2) 
	
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); 
	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < 3000:
			continue
 
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)
		return (1, gray);

	# otherwise we couldnt find movement in the frame, go to next
	return (-1, gray);

def gray_image(frame):
	# gray the provided image.
	frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
	return gray
