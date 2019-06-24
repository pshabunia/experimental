import numpy as np
import cv2
import imutils
from imutils.video import VideoStream
from timeit import default_timer as timer

class IpCamera:
	def __init__(self, stream="http://192.168.0.29:1338/video", resolution=(720, 480), framerate=30):
		self.capture = VideoStream(stream)
		print("IpCamera: start stream capture from ", stream)
		self.capture.start()

	def read(self):
		return self.capture.read()
	   
	def detect_pointer(self):
		start = timer()
		
		frame = self.read()
		# cv2.imwrite('_read.png', frame)
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
		# cv2.imwrite('_blur.png', hsv)

		# construct a mask for the color "red"
		mask = cv2.inRange(hsv, (160, 50, 50), (180, 255, 255))
		# cv2.imwrite('_threshold.png', mask)

		# find contours in the mask and initialize the current
		# (x, y) center of the pointer
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		center = None

		# only proceed if at least one contour was found
		if len(cnts) > 0:
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			if M["m00"] > 0:
				center= (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
				print("[{}] detected pointer at {} with radius {}"
					.format(timer() - start, center, radius))
				return center
		print("[{}] no pointer detected".format(timer() - start))

	def cleanup(self):
		print("IpCamera: stop stream capture")
		self.capture.stop()
