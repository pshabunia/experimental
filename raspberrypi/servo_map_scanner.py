import sys
import time
import pickle
from collections import deque
from pointer import Pointer
from ipcamera2 import CCamera

STEP = 10
DELAY = 0.1
FILE = 'servo_map.data'
RES = (736, 480)

p = Pointer()
c = CCamera(resolution=RES)
q = deque()
visited = set()
datamap = {}

pan = sys.argv[1] if len(sys.argv)>1 else 1700
tilt = sys.argv[2] if len(sys.argv)>2 else 1700
p.position(pan, tilt)

time.sleep(3) # warmup
if c.detect_pointer():
	q.append((pan, tilt))
else:
	raise Exception("Cannot detect laser pointer at initial pan={} tilt={}".format(pan, tilt))

print("starting from {}".format((pan, tilt)))
while q:
	print("enqued: {}, visited: {}, collected: {}".format(len(q), len(visited), len(datamap)))
	(pan, tilt) = q.pop()
	if (pan, tilt) in visited:
		continue

	visited.add((pan, tilt))
	p.position(pan, tilt)
	time.sleep(DELAY)
	xy = c.detect_pointer()

	if not xy:
		continue

	(x, y) = xy
	datamap[(x, y)] = (pan, tilt)
	for pp in [pan - STEP, pan + STEP]:
		for tt in [tilt - STEP, tilt + STEP]:
			if (pp, tt) not in visited:
				print("enqueue ", (pp, tt))
				q.append((pp, tt))
			else:
				print("ignore ", (pp, tt))

print("Done scanning. Collected entries: ", len(datamap))
print("Saving to ", FILE)
with open(FILE, 'wb') as file:
	pickle.dump(datamap, file)

print("Done")
c.cleanup()
p.cleanup()
