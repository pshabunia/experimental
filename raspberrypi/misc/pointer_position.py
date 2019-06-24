from pointer import Pointer

pan = sys.argv[1] if len(sys.argv)>1 else 1600
tilt = sys.argv[2] if len(sys.argv)>2 else 1800
p = Pointer()
p.position(pan, tilt)
