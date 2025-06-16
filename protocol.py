import json

MAX_LEN = 1024

class ProtocolError(Exception): pass

class Message:
    def __init__(self, type_, **kwargs):
        self.type = type_
        self.payload = kwargs

    def encode(self):
        obj = {"type": self.type, **self.payload}
        line = json.dumps(obj, ensure_ascii=False)
        if len(line) > MAX_LEN:
            raise ProtocolError("msg too long")
        return (line + "\n").encode()

    @staticmethod
    def decode(line_bytes):
        line = line_bytes.decode(errors="ignore").rstrip("\n")
        if len(line_bytes) > MAX_LEN:
            raise ProtocolError("msg too long")
        obj = json.loads(line)
        t = obj.pop("type", None)
        if not t:
            raise ProtocolError("no type")
        return Message(t, **obj)
