class Semaphore:
    def __init__(self, value):
        self.value = value

    def wait(self):
        if self.value > 0:
            self.value -= 1
            return True
        return False

    def signal(self):
        self.value += 1