class ThreadModel:
    def __init__(self, model_type):
        self.model_type = model_type

    def map_threads(self, threads):
        mapping = []

        if self.model_type == "Many-to-One":
            for t in threads:
                mapping.append((t.tid, "CPU-1"))

        elif self.model_type == "One-to-One":
            for i, t in enumerate(threads):
                mapping.append((t.tid, f"CPU-{i+1}"))

        elif self.model_type == "Many-to-Many":
            for i, t in enumerate(threads):
                cpu_id = (i % 2) + 1
                mapping.append((t.tid, f"CPU-{cpu_id}"))

        return mapping