class RoundRobinScheduler:
    def __init__(self, quantum):
        self.quantum = quantum
        self.queue = []

    def add_thread(self, thread):
        self.queue.append(thread)

    def schedule(self):
        if not self.queue:
            return None

        current = self.queue.pop(0)
        current.state = "RUNNING"

        finished = current.run(self.quantum)

        if not finished:
            current.state = "READY"
            self.queue.append(current)

        return current