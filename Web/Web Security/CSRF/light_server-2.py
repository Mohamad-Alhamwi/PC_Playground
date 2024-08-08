import http.server
import socketserver
from urllib.parse import urlparse, parse_qs, quote

PORT = 8888

class RedirectHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        # Extract the 'url' parameter
        if 'url' in query_params:
            redirect_url = query_params['url'][0]
        
            # HTML form for POST request
            html_form = f"""
            <html>
            <body>
                <form id="redirectForm" action="{redirect_url}" method="POST">
                </form>
                <script type="text/javascript">
                    document.getElementById('redirectForm').submit();
                </script>
            </body>
            </html>
            """
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_form.encode('utf-8'))

        else:
            self.send_response(400)  # 400 Bad Request
            self.end_headers()
            self.wfile.write(b'Missing "url" parameter')

with socketserver.TCPServer(("", PORT), RedirectHandler) as httpd:
    print(f"Serving on port {PORT}, redirecting to provided URLs using POST requests")
    httpd.serve_forever()
