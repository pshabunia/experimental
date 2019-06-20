import RPi.GPIO as GPIO

class Laser:
    def __init__(self, pin=4):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        print("Opening GPIO output on pin ", pin)
        GPIO.setup(self.pin, GPIO.OUT)
    
    def on(self):
        print("Laser: turn ON")
        GPIO.output(self.pin, 1)
            
    def off(self):
        print("Laser: turn OFF")
        GPIO.output(self.pin, 0)

    def cleanup(self):
        print("Laser: cleanup GPIO")
        GPIO.cleanup()
