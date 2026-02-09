from http.server import BaseHTTPRequestHandler, HTTPServer
import json

HOST = "localhost"
PORT = 8000

books = [
    {"id": 1, "name": "Uncle Tom's Cabin", "price": 9.50},
    {"id": 2, "name": "Meditations", "price": 15.75}
]

class APIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            self._set_headers()
            response = {"status": "ok"}
            self.wfile.write(json.dumps(response).encode())

        elif self.path == "/books":
            self._set_headers()
            self.wfile.write(json.dumps(books).encode())

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

def run_server():
    server = HTTPServer((HOST, PORT), APIHandler)
    print(f"Server running at http://{HOST}:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()