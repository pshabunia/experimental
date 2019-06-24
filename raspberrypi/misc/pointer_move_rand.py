import time
import random
from pointer import Pointer

print("Starting")
def randpan():
    return random.randrange(1400, 1600)

def randtilt():
    return random.randrange(1800, 2000)

def randsleep():
    time.sleep(random.uniform(0.5, 3))

pointer = Pointer()
try:
    while True:
        pointer.position(randpan(), randtilt())
        randsleep()
except KeyboardInterrupt:
    pass # it's ok
finally:
    print("Clean up and exit.")
    pointer.cleanup()

print("Done")
