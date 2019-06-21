import time
from timeit import default_timer as timer
import numpy as np
import cv2
import imutils
from imutils.video.pivideostream import PiVideoStream

class Camera:
    def __init__(self, resolution=(1280, 720), framerate=12, lowlight=0):
        self.stream = PiVideoStream(resolution, framerate)
        self.hsv_low = (0, 100, 100)
        self.hsv_high = (20, 255, 255)
        if lowlight:
            self.hsv_low = (160, 100, 100)
            self.hsv_high = (180, 255, 255)

    def start(self):
        print("Camera: starting")
        self.stream.start()
        time.sleep(3.0)
        return self
    def read(self):
        return self.stream.read() 
    def stop(self):
        print("Camera: stopping")
        self.stream.stop()
        
    def detect_pointer(self):
        start = timer()
        
        frame = self.stream.read()
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "red"
        mask = cv2.inRange(hsv, self.hsv_low, self.hsv_high)
        # debug
        # cv2.imwrite('_threshold.png', mask)

        # optionally, perform a series of dilations and erosions
        # to remove any small blobs left in the mask
        # most suitable for bright light conditions
        # mask = cv2.erode(mask, None, iterations=2)
        # mask = cv2.dilate(mask, None, iterations=2)

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
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            print("[{}] detected pointer at {} with radius {}"
                  .format(timer() - start, center, radius))
        else:
            print("[{}] no pointer detected".format(timer() - start))
        return center