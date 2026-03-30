import time

class Simulator:
    def __init__(self, scheduler, update_callback):
        self.scheduler = scheduler
        self.update_callback = update_callback
        self.running = False
        self.paused = False
        self.speed = 1.0

    def start(self):
        self.running = True
        while self.running:
            if self.paused:
                time.sleep(0.1)
                continue

            thread = self.scheduler.schedule()
            self.update_callback(thread)
            time.sleep(self.speed)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.running = False