import numpy as np
import cv2 as cv
import imutils
from imutils.video import VideoStream

stream = 'http://192.168.0.29:1338/video'
res = (720, 480)
fps = 30

capture = VideoStream(src=stream, resolution=res, framerate=fps)
capture.start()

frame = capture.read()
cv.imwrite('data/_frame.png', frame)

frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

for b in range(5, 14, 2):
	frame_hsv = cv.GaussianBlur(frame_hsv, (b, b), 0)
	for h in range(160, 176, 5):
		for sv in range(50, 101, 10):
			frame_threshed = cv.inRange(frame_hsv, (h, sv, sv), (h + 10, 255, 255))
			cv.imwrite('data/_frame_threshed_b{}_h{}_sv{}.png'.format(b, h, sv), frame_threshed)


capture.stop()
