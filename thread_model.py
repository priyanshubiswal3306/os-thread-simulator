class Thread:
    def __init__(self, tid, burst_time):
        self.tid = tid
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.state = "READY"

    def run(self, time_slice):
        if self.remaining_time > time_slice:
            self.remaining_time -= time_slice
            return False  # not finished
        else:
            self.remaining_time = 0
            self.state = "TERMINATED"
            return True  # finished

    def __str__(self):
        return f"{self.tid} ({self.state})"