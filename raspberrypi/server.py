import time
import random
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
from pointer import Pointer

HOSTNAME = 'raspberrypi.local'
PORT = 1337
POINTER = Pointer()

class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path.startswith('/position'):
            self.position()
        elif self.path.startswith('/reset'):
            self.reset()
            
    def end_headers(self):
        # CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(RequestHandler, self).end_headers()
    
    def position(self):
        query_params = parse_qs(urlparse(self.path).query)
        x = query_params['x']
        y = query_params['y']
        (pan, tilt) = self.translate(x, y)
        POINTER.position(pan, tilt)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Ok')

    def translate(self, x, y):
        return (random.randrange(1400, 1600), random.randrange(1800, 2100))
    
    def reset(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Ready')
       
if __name__ == '__main__':
    httpd = HTTPServer((HOSTNAME, PORT), RequestHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOSTNAME, PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    POINTER.cleanup()
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOSTNAME, PORT))