import time
import picamera
import numpy as np
import cv2

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 24
    time.sleep(0.1)
    image = np.empty((1280 * 720 * 3,), dtype=np.uint8)
    camera.capture(image, 'bgr')
    image = image.reshape((1280, 720, 3))