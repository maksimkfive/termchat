#!/usr/bin/env python3
import socket, threading, sys
from protocol import Message

class ChatClient:
    def __init__(self, host, port, nick, ui):
        self.sock = socket.socket()
        self.sock.connect((host, port))
        self.nick = nick
        self.ui = ui

    def send(self, msg):
        self.sock.sendall(msg.encode())

    def recv_loop(self):
        try:
            while True:
                raw = self.sock.recv(2048)
                if not raw: break
                for line in raw.split(b"\n"):
                    if not line: continue
                    msg = Message.decode(line+b"\n")
                    self.ui.handle_server(msg)
        finally:
            self.ui.stop()

    def start(self):
        self.send(Message("join", nick=self.nick))
        threading.Thread(target=self.recv_loop, daemon=True).start()
        self.ui.run(self)

if __name__=="__main__":
    import ui, sys
    h,p = sys.argv[1], int(sys.argv[2])
    nick = input("Name: ")
    ChatClient(h,p,nick, ui.ChatUI()).start()
