import time
import random
from pointer import Pointer
from camera import Camera

p = Pointer()
c = Camera(lowlight=1).start()

for pan in range (1600, 1700, 20):
    for tilt in range (1900, 2000, 20):
        p.position(pan, tilt)
        time.sleep(0.2)
        c.detect_pointer()

c.stop()
p.cleanup()
