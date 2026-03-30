import time

class Simulator:
    def __init__(self, scheduler, update_callback):
        self.scheduler = scheduler
        self.running = False
        self.update_callback = update_callback

    def start(self):
        self.running = True
        while self.running:
            thread = self.scheduler.schedule()
            self.update_callback(thread)
            time.sleep(1)