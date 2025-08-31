# client/socket_handler.py
import socket
import json

class SocketClient:
    def __init__(self, host='127.0.0.1', port=9009):
        self.host = host
        self.port = port
        self.sock = None
        self.buf = ""

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send(self, obj):
        data = (json.dumps(obj) + "\n").encode('utf-8')
        self.sock.sendall(data)

    def recv(self):
        while "\n" not in self.buf:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise ConnectionError("Server closed")
            self.buf += chunk.decode('utf-8')
        line, self.buf = self.buf.split("\n", 1)
        return json.loads(line)

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
