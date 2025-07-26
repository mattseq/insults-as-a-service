from collections import deque

class ChatMemory:
    def __init__(self, max_len=10):
        self.buffer = deque(maxlen=max_len)

    def add_message(self, author, content):
        self.buffer.append((author, content))

    def get_formatted_history(self):
        return "\n".join([f"{a}: {c}" for a, c in self.buffer])
