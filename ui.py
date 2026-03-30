import tkinter as tk
from thread_model import Thread
from scheduler import RoundRobinScheduler
from simulator import Simulator
import threading
from models import ThreadModel

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Thread Simulator")

        self.scheduler = RoundRobinScheduler(quantum=2)

        self.canvas = tk.Canvas(root, width=800, height=400, bg="white")
        self.canvas.pack()

        self.start_btn = tk.Button(root, text="Start", command=self.start_sim)
        self.start_btn.pack(pady=10)
        # 🔽 Multithreading Model Selector
        self.model_var = tk.StringVar(value="Many-to-One")

        model_menu = tk.OptionMenu(
            root,
            self.model_var,
            "Many-to-One",
            "One-to-One",
            "Many-to-Many"
        )
        model_menu.pack(pady=5)

        self.threads = []
        self.finished_threads = []
        self.current_thread = None

        self.simulator = Simulator(self.scheduler, self.update_ui)

        self.create_threads()
        self.draw_threads()

    # 🔹 Create initial threads
    def create_threads(self):
        for i in range(5):
            t = Thread(f"T{i+1}", burst_time=5+i)
            self.scheduler.add_thread(t)
            self.threads.append(t)

    # 🔹 Static labels
    def draw_layout(self):
        self.canvas.create_text(150, 50, text="Ready Queue", font=("Arial", 14))
        self.canvas.create_text(400, 50, text="CPU", font=("Arial", 14))
        self.canvas.create_text(650, 50, text="Finished", font=("Arial", 14))
        self.canvas.create_text(400, 220, text="Thread Mapping", font=("Arial", 14))

    # 🔹 Main drawing function
    def draw_threads(self):
        self.canvas.delete("all")
        self.draw_layout()

        # ✅ Color mapping
        color_map = {
            "READY": "yellow",
            "RUNNING": "green",
            "TERMINATED": "gray"
        }

        # 🔹 Ready Queue
        x = 50
        for t in self.scheduler.queue:
            color = color_map.get(t.state, "red")
            self.canvas.create_rectangle(x, 100, x+80, 150, fill=color)
            self.canvas.create_text(x+40, 120, text=t.tid)
            self.canvas.create_text(x+40, 140, text=f"{t.remaining_time}")
            x += 100

        # 🔹 CPU
        if self.current_thread:
            color = color_map.get(self.current_thread.state, "red")
            self.canvas.create_rectangle(350, 100, 450, 150, fill=color)
            self.canvas.create_text(400, 120, text=self.current_thread.tid)
            self.canvas.create_text(400, 140, text=f"{self.current_thread.remaining_time}")

        # 🔹 Finished Threads
        x = 550
        for t in self.finished_threads:
            color = color_map.get(t.state, "red")
            self.canvas.create_rectangle(x, 100, x+80, 150, fill=color)
            self.canvas.create_text(x+40, 120, text=t.tid)
            x += 100

        self.draw_mapping()

    def draw_mapping(self):
        model = ThreadModel(self.model_var.get())
        mapping = model.map_threads(self.threads)

        y = 250
        for tid, cpu in mapping:
            text = f"{tid} → {cpu}"
            self.canvas.create_text(400, y, text=text, font=("Arial", 12))
            y += 25

    # 🔹 Update UI after each step
    def update_ui(self, thread):
        if thread:
            self.current_thread = thread

            if thread.state == "TERMINATED":
                self.finished_threads.append(thread)
                self.current_thread = None

        self.draw_threads()

    # 🔹 Start simulation in separate thread
    def start_sim(self):
        threading.Thread(target=self.simulator.start, daemon=True).start()

    