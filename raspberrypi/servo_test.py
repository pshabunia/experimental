import time
import math
import random
from servo import Servo

servo = Servo()
try:
    while True:
        for x in range (0, 360, random.randrange(5, 20)):
            rad = math.radians(x)
            if random.random() > 0.95:
                rad = math.radians(x-40)
            servo.position(1600 + math.sin(rad)*300, 1900 + math.cos(rad)*200)
            time.sleep(random.uniform(0.1, 0.8))
except KeyboardInterrupt:
    pass
finally:
    servo.cleanup()