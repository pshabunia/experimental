from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep
from pointer import Pointer
from servo_map import ServoMap

HOSTNAME = '192.168.0.11'
PORT = 1337

POINTER = Pointer()
SERVO_MAP = ServoMap()

class RequestHandler(BaseHTTPRequestHandler):
	
	def do_GET(self):
		if (self.path == '/'):
			self.play()
		elif self.path.startswith('/position'):
			self.position()
		else:
			self.not_found()


	# TODO remove		
	def end_headers(self):
		# CORS
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', 'GET')
		self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
		return super(RequestHandler, self).end_headers()

	def play(self):
		f = open(curdir + sep + 'www' + sep + 'index.html')
		self.send_response(200)
		self.send_header('Content-Type', 'text/html')
		self.end_headers()
		self.wfile.write(bytearray(f.read(), 'utf-8'))
		f.close()

	def position(self):
		query_params = parse_qs(urlparse(self.path).query)
		x = int(query_params['x'][0])
		y = int(query_params['y'][0])
		(pan, tilt) = SERVO_MAP.query(x, y)
		POINTER.position(pan, tilt)
		self.send_response(200)
		self.end_headers()
		self.wfile.write(b'Ok')

	def not_found(self):
		self.send_error(404, 'Robots not found')

if __name__ == '__main__':
	httpd = HTTPServer((HOSTNAME, PORT), RequestHandler)
	print('Server Starts - {}:{}'.format(HOSTNAME, PORT))
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	POINTER.cleanup()
	httpd.server_close()
	print('Server Stops - {}:{}'.format(HOSTNAME, PORT))
