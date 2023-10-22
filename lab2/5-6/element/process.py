from .base import Element


class Worker:
    def __init__(self, index):
        self.index = index
        self.status = "free"
        self.tnext = float('inf')


class Process(Element):
    def __init__(self, name, mean_delay=1.0, max_queue=float('inf'), max_workers=1, distribution="exp"):
        super().__init__(name, mean_delay, distribution)
        self.queue = 0
        self.failures = 0
        self.total_process_time = 0
        self.mean_queue = 0.0
        self.max_queue = max_queue
        self.max_workers = max_workers
        self.workers = [Worker(i) for i in range(self.max_workers)]


    def in_act(self):
        free_worker = self.get_free_worker()

        if free_worker:
            free_worker.status = "busy"
            delay = self.get_delay()
            free_worker.tnext = self.tcurr + delay
            self.total_process_time += delay
            self.tnext = free_worker.tnext
        elif self.queue < self.max_queue:
            self.queue += 1
        else:
            self.failures += 1


    def out_act(self):
        super().out_act()
        busy_worker = self.get_busy_worker()

        assert busy_worker is not None
        
        busy_worker.tnext = float('inf')
        worker_tnext_values = [w.tnext for w in self.workers]
        self.tnext = min(worker_tnext_values)
        busy_worker.status = "free"

        if self.queue > 0:
            self.queue -= 1
            busy_worker.status = "busy"
            delay = self.get_delay()
            busy_worker.tnext = self.tcurr + delay
            self.total_process_time += delay
            self.tnext = min([w.tnext for w in self.workers])

        next_element = self.get_next_element()

        if next_element:
            next_element.in_act()


    def get_state(self):
        return self.get_busy_worker().index if self.get_busy_worker() else 0


    def get_free_worker(self):
        return next((w for w in self.workers if w.status == "free"), None)


    def get_busy_worker(self):
        busy_workers = [w for w in self.workers if w.status == "busy"]
        min_tnext = min(w.tnext for w in busy_workers) if busy_workers else None
        return next((w for w in self.workers if w.tnext == min_tnext), None)


    def do_statistics(self, delta):
        self.mean_queue += self.queue * delta
