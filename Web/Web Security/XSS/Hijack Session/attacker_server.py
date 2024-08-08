import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

PORT = 8888

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if parsed_path.path == '/log':
            # Extract the 'cookie' parameter
            cookie = query_params.get('cookie', [''])[0]
            print(f"Received cookie: {cookie}")
            
            # Send response
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Cookie logged\n')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found\n')

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
