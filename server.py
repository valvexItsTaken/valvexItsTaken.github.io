import os
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8000

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.strip('/')
        if path == '':
            filename = 'index.html'
        else:
            filename = path

        try:
            # Check if the file exists and is not a directory
            if os.path.exists(filename) and os.path.isfile(filename):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')  # You can improve this later
                self.end_headers()
                with open(filename, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, f"File Not Found: {self.path}")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {e}")

def run(server_class=HTTPServer, handler_class=RequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {PORT}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
