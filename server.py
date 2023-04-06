import http.server
import socketserver

handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", 3000), handler) as httpd:
    print("Server listening to port 3000")
    httpd.serve_forever()