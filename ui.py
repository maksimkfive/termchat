from protocol import Message

class ChatUI:
    def __init__(self):
        self.running = True

    def handle_server(self, msg):
        if msg.type == "info":
            print(msg.payload.get("text", ""))
        elif msg.type == "message":
            nick = msg.payload.get("nick", "")
            text = msg.payload.get("text", "")
            print(f"[{nick}] {text}")
        elif msg.type == "users":
            lst = msg.payload.get("list", [])
            print("Users: " + ", ".join(lst))

    def run(self, client):
        while self.running:
            try:
                s = input("> ")
            except EOFError:
                break
            if s == "!quit":
                client.send(Message("quit"))
                break
            elif s == "!list":
                client.send(Message("users"))
            else:
                client.send(Message("message", text=s))
        client.sock.close()

    def stop(self):
        self.running = False
