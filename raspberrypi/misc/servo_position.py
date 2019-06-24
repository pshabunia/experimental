import sys
from servo import Servo

pan = sys.argv[1] if len(sys.argv)>1 else 1600
tilt = sys.argv[2] if len(sys.argv)>2 else 1800
servo = Servo()
servo.position(pant, tilt)

