import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

if len(sys.argv) == 1:
    PINS = [4]
else:
    PINS = [int(pin) for pin in sys.argv[1:]]

for pin in PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, not GPIO.input(pin))