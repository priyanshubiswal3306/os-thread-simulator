import random

class ProducerConsumer:
    def __init__(self, buffer_size=5):
        self.buffer = []
        self.buffer_size = buffer_size

    def produce(self):
        if len(self.buffer) < self.buffer_size:
            item = random.randint(1, 9)
            self.buffer.append(item)
            return f"Produced {item}"
        return "Buffer Full"

    def consume(self):
        if len(self.buffer) > 0:
            item = self.buffer.pop(0)
            return f"Consumed {item}"
        return "Buffer Empty"