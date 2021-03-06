import socketserver

from core import Request
from request_handler import handle_request


class BaseTCPHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        print(f"Address: {self.client_address}")

        data = self.request.recv(4096).strip()  # strip() - Delete spaces
        request = Request(data)
        response = handle_request(request)
        self.request.send(response)


socketserver.ThreadingTCPServer.allow_reuse_address = True

if __name__ == "__main__":
    with socketserver.ThreadingTCPServer(("", 8300), BaseTCPHandler) as server:
        print("Server started")
        server.serve_forever()
    print("Server stopped")
