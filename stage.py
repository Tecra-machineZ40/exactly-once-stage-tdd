import threading


class StageRunner:
    def __init__(self):
        self.completed = False
        self.receipts = []
        self._lock = threading.Lock()

    def complete_work(self, before_commit_hook=None):
        if before_commit_hook:
            before_commit_hook()
        with self._lock:
            if not self.completed:
                self.completed = True
                self.receipts.append("done")

    def timeout(self):
        with self._lock:
            if not self.completed:
                self.completed = True
                self.receipts.append("timeout")
