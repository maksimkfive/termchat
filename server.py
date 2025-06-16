#!/usr/bin/env python3
import socket, threading
from protocol import Message, ProtocolError

class ChatServer:
    def __init__(self, port):
        self.host = "0.0.0.0"
        self.port = port
        self.clients = {}   # conn -> nick
        self.lock = threading.Lock()

    def broadcast(self, msg, exclude=None):
        data = msg.encode()
        with self.lock:
            for conn in list(self.clients):
                if conn is not exclude:
                    try: conn.sendall(data)
                    except: pass

    def handle(self, conn, addr):
        try:
            # join
            raw = conn.recv(2048)
            msg = Message.decode(raw)
            if msg.type != "join":
                conn.close(); return
            nick = msg.payload.get("nick","?")[:32]
            with self.lock: self.clients[conn] = nick
            self.broadcast(Message("info", text=f"{nick} joined"))
            # loop
            while True:
                raw = conn.recv(2048)
                if not raw: break
                try:
                    msg = Message.decode(raw)
                except ProtocolError:
                    continue
                if msg.type == "message":
                    text = msg.payload.get("text","")[:256]
                    # очистка ANSI тут, если надо
                    self.broadcast(Message("message", nick=nick, text=text), exclude=conn)
                elif msg.type == "quit":
                    break
                elif msg.type == "users":
                    with self.lock:
                        lst = list(self.clients.values())
                    conn.sendall(Message("users", list=lst).encode())
        finally:
            with self.lock: self.clients.pop(conn, None)
            self.broadcast(Message("info", text=f"{nick} left"))
            conn.close()

    def run(self):
        sock = socket.socket()
        sock.bind((self.host, self.port))
        sock.listen(5)
        print(f"Server on {self.host}:{self.port}")
        while True:
            conn, addr = sock.accept()
            threading.Thread(target=self.handle, args=(conn,addr), daemon=True).start()

if __name__=="__main__":
    import sys
    p = int(sys.argv[1]) if len(sys.argv)>1 else 6000
    ChatServer(p).run()
