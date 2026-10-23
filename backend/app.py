import os
import redis
from http.server import BaseHTTPRequestHandler, HTTPServer

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
           message = os.getenv("APP_MESSAGE", "Default backend message")
        
        elif self.path == "/api/visit":
            visits = redis_client.incr("visits")
            message = f"Website visits: {visits}"
        
        else:
            message = "Not found"

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(message)))
        self.end_headers()
        self.wfile.write(message.encode())

server = HTTPServer(("0.0.0.0", 8000), Handler)

print("Backend running on port 8000", flush=True)

server.serve_forever()