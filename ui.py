import tkinter as tk
from thread_model import Thread
from scheduler import RoundRobinScheduler
from simulator import Simulator

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Thread Simulator")

        self.scheduler = RoundRobinScheduler(quantum=2)

        self.canvas = tk.Canvas(root, width=600, height=300, bg="white")
        self.canvas.pack()

        self.start_btn = tk.Button(root, text="Start", command=self.start_sim)
        self.start_btn.pack()

        self.threads = []

        self.simulator = Simulator(self.scheduler, self.update_ui)

        self.create_threads()

    def create_threads(self):
        for i in range(5):
            t = Thread(f"T{i+1}", burst_time=5+i)
            self.scheduler.add_thread(t)
            self.threads.append(t)

    def draw_threads(self):
        self.canvas.delete("all")

        x = 50
        for t in self.threads:
            color = {
                "READY": "yellow",
                "RUNNING": "green",
                "TERMINATED": "gray"
            }.get(t.state, "red")

            self.canvas.create_rectangle(x, 100, x+80, 150, fill=color)
            self.canvas.create_text(x+40, 125, text=t.tid)

            x += 100

    def update_ui(self, thread):
        self.draw_threads()
        self.root.update()

    def start_sim(self):
        self.simulator.start()