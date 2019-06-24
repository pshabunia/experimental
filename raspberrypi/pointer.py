import time
import random
import sys
from laser import Laser
from servo import Servo

class Pointer:
    def __init__(self):
        self.laser = Laser()
        self.servo = Servo()
        self.laser.on()
        
    def position(self, pan, tilt):
        self.servo.position(pan, tilt)
        
    def cleanup(self):
        print("Pointer: clean laser and servo")
        self.laser.cleanup()
        self.servo.cleanup()

