import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

PORT = 8000


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse URL and remove query parameters
        parsed_path = urlparse(self.path)
        clean_path = parsed_path.path.strip('/')

        # Default file
        filename = 'index.html' if clean_path == '' else clean_path

        try:
            # Check if the file exists and is not a directory
            if os.path.exists(filename) and os.path.isfile(filename):
                self.send_response(200)

                # Very basic content-type detection (optional improvement)
                if filename.endswith(".html"):
                    self.send_header('Content-type', 'text/html')
                elif filename.endswith(".css"):
                    self.send_header('Content-type', 'text/css')
                elif filename.endswith(".js"):
                    self.send_header('Content-type', 'application/javascript')
                else:
                    self.send_header('Content-type', 'application/octet-stream')

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
