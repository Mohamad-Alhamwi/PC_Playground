import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

PORT = 8888

class RedirectHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        # Extract the 'url' parameter
        if 'url' in query_params:
            redirect_url = query_params['url'][0]
            self.send_response(301)  # 301 Moved Permanently
            self.send_header('Location', redirect_url)
            self.end_headers()
        else:
            self.send_response(400)  # 400 Bad Request
            self.end_headers()
            self.wfile.write(b'Missing "url" parameter')

with socketserver.TCPServer(("", PORT), RedirectHandler) as httpd:
    print(f"Serving on port {PORT}, redirecting to provided URLs")
    httpd.serve_forever()
