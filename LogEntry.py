class LogEntry:
    def __init__(self, time, message):
        self.time: float = time
        self.message: str = message

    def __str__(self):
        return f"[Time={self.time:.2f}] {self.message}"