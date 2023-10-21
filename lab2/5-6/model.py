from element import Process

class Model:
    def __init__(self, elements):
        self.elements = elements
        self.tnext = 0
        self.event = 0
        self.total_time = 0
        self.tcurr = self.tnext


    def simulate(self, time):
        self.total_time = time

        while self.tcurr < self.total_time:
            self.tnext = float('inf')

            for elem in self.elements:
                if elem.tnext < self.tnext:
                    self.tnext = elem.tnext
                    self.event = elem.id

            print(f"\nIt's time for event in {self.elements[self.event].name}, time = {self.tnext}")

            for elem in self.elements:
                elem.do_statistics(self.tnext - self.tcurr)

            self.tcurr = self.tnext

            for elem in self.elements:
                elem.tcurr = self.tcurr

            self.elements[self.event].out_act() # ?

            for elem in self.elements:
                if elem.tnext == self.tcurr:
                    elem.out_act()

            for el in self.elements:
                el.print_info()

        self.print_results()
            

    def print_results(self):
        print("\n----------------------------RESULTS----------------------------")
        total_failures = 0

        for elem in self.elements:
            elem.print_result()

            if isinstance(elem, Process):
                mean = elem.mean_queue / self.tcurr
                total_failures += elem.failures
                failure_prob = elem.failures / (elem.processed + elem.failures) \
                               if (elem.processed + elem.failures) > 0 else 0
                avg_process_time = elem.total_process_time / self.total_time
                avg_worker_process_time = avg_process_time / len(elem.workers)
                
                print(f"Mean length of queue = {mean}") 
                print(f"Failures = {elem.failures}")
                print(f"Failure probability = {failure_prob}")
                print(f"Mean process time {avg_process_time}")
                print(f"Average worker process time {avg_worker_process_time}\n\n")
        
        print(f"Total failures = {total_failures}")
