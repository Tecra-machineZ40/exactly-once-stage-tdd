class StageRunner:
    def __init__(self):
        self.completed = False
        self.receipts = []

    def complete_work(self, before_commit_hook=None):
        if not self.completed:
            if before_commit_hook:
                before_commit_hook()
            self.completed = True
            self.receipts.append("done")

    def timeout(self):
        if not self.completed:
            self.completed = True
            self.receipts.append("timeout")
