import numpy as np
import cv2
import imutils
from imutils.video import VideoStream
from picamera import PiCamera
from timeit import default_timer as timer


class _PiCamera:
	"""Decorator for PiCamera inerface. Allows uniform calls to VideoStream
		and PiCamera using read() and cleanup()
	"""
	def __init__(self, resolution=(720, 480)):
		self.camera = PiCamera()
		self.camera.resolution = resolution
		self.w, self.h = resolution
	def read(self):
		frame = np.empty((self.h * self.w * 3,), dtype=np.uint8)
		self.camera.capture(frame, 'bgr')
		frame = frame.reshape((self.h, self.w, 3))
		return frame
	def stop(self):
		self.camera.close()

class CCamera:
	def __init__(self, stream="", resolution=(720, 480), framerate=30):
		# e.g. "http://192.168.0.29:1338/video",
		if stream:
			print("CCamera: start stream capture from ", stream)
			self.capture = VideoStream(stream)
			self.capture.start()
		else:
			print("CCamera: capture from attached RPi Camera")
			self.capture = _PiCamera(resolution)

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
		print("CCamera: stop stream capture")
		self.capture.stop()
