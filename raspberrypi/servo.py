import time
import pigpio


class Servo:
    def __init__(self, panpin=23, tiltpin=24):
        self.ppin = panpin
        self.tpin = tiltpin
        print("Servo: starting on pins [pan={}, tilt={}]"
              .format(panpin, tiltpin))
        self.pi = pigpio.pi()
        if not self.pi.connected:
           exit("Cannot connect to pi")
    
    def pan(self, pan):
        self.pi.set_servo_pulsewidth(self.ppin, pan)

    def tilt(self, tilt):
        self.pi.set_servo_pulsewidth(self.tpin, tilt)
        
    def position(self, pan, tilt):
        print("Servo: [pan={}, tilt={}]".format(pan, tilt))
        self.pan(pan)
        self.tilt(tilt)
        
    def cleanup(self):
        print("Servo: cleanup GPIO")
        self.pan(0)
        self.tilt(0)
        self.pi.stop()
