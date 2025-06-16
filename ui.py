import curses
from protocol import Message

class ChatUI:
    def __init__(self):
        self.stdscr = None
        self.lines = []
        self.status = ""

    def handle_server(self, msg):
        if msg.type in ("info", "message"):
            if msg.type == "info":
                text = msg.payload.get("text", "")
            else:
                text = f"[{msg.payload.get('nick', '')}] {msg.payload.get('text', '')}"
            self.lines.append(text)
            self.redraw()
        elif msg.type == "users":
            self.status = "Users: " + ", ".join(msg.payload.get("list", []))
            self.redraw()

    def run(self, client):
        curses.wrapper(self._curses_loop, client)

    def _curses_loop(self, stdscr, client):
        self.stdscr = stdscr
        curses.curs_set(1)
        h, w = stdscr.getmaxyx()
        win_msgs = curses.newwin(h-2, w, 0, 0)
        win_status = curses.newwin(1, w, h-2, 0)
        win_input = curses.newwin(1, w-1, h-1, 0)

        while True:
            # render messages
            win_msgs.clear()
            win_msgs.box()
            start = max(0, len(self.lines) - (h-2))
            for idx, line in enumerate(self.lines[start:]):
                win_msgs.addstr(idx+1, 1, line[:w-2])
            win_msgs.refresh()

            # render status bar
            win_status.clear()
            win_status.addstr(0, 0, self.status[:w-1])
            win_status.chgat(0, 0, curses.A_REVERSE)
            win_status.refresh()

            # input
            win_input.clear()
            win_input.addstr(0, 0, "> ")
            win_input.refresh()
            try:
                s = win_input.getstr().decode()
            except Exception:
                break

            if s == "!quit":
                client.send(Message("quit"))
                break
            elif s == "list":
                client.send(Message("users"))
            else:
                client.send(Message("message", text=s))

        client.sock.close()

    def redraw(self):
        # placeholder: will refresh UI on next loop iteration
        pass
