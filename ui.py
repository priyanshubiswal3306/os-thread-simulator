import tkinter as tk
import threading
import random

from thread_model import Thread
from scheduler import RoundRobinScheduler
from simulator import Simulator
from models import ThreadModel
from semaphore import Semaphore
from producer_consumer import ProducerConsumer


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Thread Simulator")

        # 🎨 Theme
        self.colors = {
            "bg": "#1e1e2f",
            "card": "#2a2a40",
            "accent": "#4cc9f0",
            "ready": "#f1c40f",
            "running": "#2ecc71",
            "done": "#7f8c8d",
            "text": "#ffffff",
            "subtext": "#bbbbbb"
        }

        self.canvas = tk.Canvas(root, width=900, height=600, bg=self.colors["bg"], highlightthickness=0)
        self.canvas.pack()

        # 🎛 Controls
        controls = tk.Frame(root, bg=self.colors["bg"])
        controls.pack(pady=5)

        tk.Button(controls, text="Start", command=self.start_sim).grid(row=0, column=0, padx=5)
        tk.Button(controls, text="Pause", command=self.pause_sim).grid(row=0, column=1, padx=5)
        tk.Button(controls, text="Reset", command=self.reset_sim).grid(row=0, column=2, padx=5)

        self.speed_var = tk.DoubleVar(value=1.0)
        tk.Scale(
            controls,
            from_=0.2,
            to=2.0,
            resolution=0.1,
            orient="horizontal",
            label="Speed",
            variable=self.speed_var,
            command=self.update_speed
        ).grid(row=0, column=3, padx=10)

        # Dropdown
        self.model_var = tk.StringVar(value="Many-to-One")
        tk.OptionMenu(root, self.model_var, "Many-to-One", "One-to-One", "Many-to-Many").pack(pady=5)

        # Core
        self.scheduler = RoundRobinScheduler(quantum=2)
        self.simulator = Simulator(self.scheduler, self.update_ui)

        # Data
        self.threads = []
        self.finished_threads = []
        self.current_thread = None
        self.gantt = []

        # Sync
        self.semaphore = Semaphore(3)
        self.pc = ProducerConsumer(buffer_size=5)
        self.pc_log = ""

        self.create_threads()
        self.draw_all()

    def create_threads(self):
        for i in range(5):
            t = Thread(f"T{i+1}", 5+i)
            self.scheduler.add_thread(t)
            self.threads.append(t)

    def draw_all(self):
        self.canvas.delete("all")
        self.draw_layout()
        self.draw_threads()
        self.draw_mapping()
        self.draw_producer_consumer()
        self.draw_gantt()

    def draw_layout(self):
        c = self.colors

        self.canvas.create_text(150, 30, text="Ready Queue", fill=c["text"], font=("Segoe UI", 14, "bold"))
        self.canvas.create_text(450, 30, text="CPU", fill=c["text"], font=("Segoe UI", 14, "bold"))
        self.canvas.create_text(750, 30, text="Finished", fill=c["text"], font=("Segoe UI", 14, "bold"))

        self.canvas.create_rectangle(20, 60, 280, 200, fill=c["card"], outline="")
        self.canvas.create_rectangle(350, 60, 550, 200, fill=c["card"], outline="")
        self.canvas.create_rectangle(620, 60, 880, 200, fill=c["card"], outline="")

        self.canvas.create_line(50, 220, 850, 220, fill=c["accent"], width=2)

        self.canvas.create_text(450, 250, text="Thread Mapping", fill=c["accent"], font=("Segoe UI", 14, "bold"))

        self.canvas.create_text(150, 380, text="Producer", fill=c["subtext"])
        self.canvas.create_text(450, 380, text="Buffer", fill=c["subtext"])
        self.canvas.create_text(750, 380, text="Consumer", fill=c["subtext"])

    def draw_threads(self):
        c = self.colors
        color_map = {
            "READY": c["ready"],
            "RUNNING": c["running"],
            "TERMINATED": c["done"]
        }

        start_x = 40
        start_y = 90

        x = start_x
        y = start_y

        max_per_row = 3   # number of threads per row
        count = 0

        for t in self.scheduler.queue:
            color = color_map.get(t.state)

            self.canvas.create_rectangle(x, y, x+60, y+50, fill=color, outline="")
            self.canvas.create_text(x+30, y+20, text=t.tid, fill="black")

            count += 1

            if count % max_per_row == 0:
                # Move to next row
                x = start_x
                y += 60
            else:
                x += 70

        if self.current_thread:
            for step in range(5):
                self.canvas.delete("cpu_anim")
                x = 350 + step * 15

                self.canvas.create_rectangle(x, 100, x+60, 140, fill=c["running"], tags="cpu_anim")
                self.canvas.create_text(x+30, 120, text=self.current_thread.tid, tags="cpu_anim")

                self.canvas.update()
                self.canvas.after(20)

        x = 640
        for t in self.finished_threads:
            self.canvas.create_rectangle(x, 100, x+60, 140, fill=c["done"], outline="")
            self.canvas.create_text(x+30, 120, text=t.tid)
            x += 70

    def draw_mapping(self):
        model = ThreadModel(self.model_var.get())
        mapping = model.map_threads(self.threads)

        y = 270
        for tid, cpu in mapping:
            self.canvas.create_text(450, y, text=f"{tid} → {cpu}", fill=self.colors["text"])
            y += 18

    def draw_producer_consumer(self):
        x = 350
        y = 410

        for i in range(self.pc.buffer_size):
            color = self.colors["running"] if i < len(self.pc.buffer) else self.colors["card"]
            self.canvas.create_rectangle(x, y, x+45, y+45, fill=color, outline=self.colors["accent"])
            x += 50

        self.canvas.create_text(450, 470, text=self.pc_log, fill=self.colors["text"])
        self.canvas.create_text(450, 500, text=f"Semaphore: {self.semaphore.value}", fill=self.colors["subtext"])

    def draw_gantt(self):
        x = 50
        y = 550

        for t in self.gantt[-20:]:
            self.canvas.create_rectangle(x, y, x+30, y+30, fill=self.colors["accent"])
            self.canvas.create_text(x+15, y+15, text=t)
            x += 35

    def update_ui(self, thread):
        if thread:
            self.current_thread = thread
            self.gantt.append(thread.tid)

            if thread.state == "TERMINATED":
                self.finished_threads.append(thread)
                self.current_thread = None

        action = random.choice(["produce", "consume"])

        if action == "produce":
            if self.semaphore.wait():
                self.pc_log = self.pc.produce()
                self.semaphore.signal()
        else:
            if self.semaphore.wait():
                self.pc_log = self.pc.consume()
                self.semaphore.signal()

        self.draw_all()

    def start_sim(self):
        threading.Thread(target=self.simulator.start, daemon=True).start()

    def pause_sim(self):
        self.simulator.pause()

    def reset_sim(self):
        self.simulator.stop()
        self.scheduler.queue.clear()
        self.finished_threads.clear()
        self.current_thread = None
        self.gantt.clear()
        self.create_threads()
        self.draw_all()

    def update_speed(self, val):
        self.simulator.speed = float(val)