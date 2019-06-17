import time
import random
import pigpio

XX_MIN=1400
XX_MAX=1600
YY_MIN=1800
YY_MAX=2000

def xpos():
    return random.randrange(XX_MIN, XX_MAX)

def ypos():
    return random.randrange(YY_MIN, YY_MAX)

pi = pigpio.pi()

if not pi.connected:
   exit()

XX_PIN=23
YY_PIN=24

while True:
    try:
        pi.set_servo_pulsewidth(XX_PIN, xpos())
        pi.set_servo_pulsewidth(YY_PIN, ypos())
        time.sleep(random.uniform(0.7, 3))

    except KeyboardInterrupt:
        break

print "Clean up and terminate."

pi.set_servo_pulsewidth(XX_PIN, 0)
pi.set_servo_pulsewidth(YY_PIN, 0)
pi.stop()