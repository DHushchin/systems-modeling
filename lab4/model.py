from termcolor import colored
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
                if elem.tnext <= self.tnext:
                    self.tnext = elem.tnext
                    self.event = elem.id

            for elem in self.elements:
                elem.do_statistics(self.tnext - self.tcurr)

            self.tcurr = self.tnext

            for elem in self.elements:
                elem.tcurr = self.tcurr

            # print()
            for elem in self.elements:
                if elem.tnext == self.tcurr:
                    # print(colored(f"It's time for event in {elem.name}, time = {self.tcurr}", 'yellow'))
                    elem.out_act()
            # print()

            # for el in self.elements:
            #     el.print_info()

        #self.print_results()
            

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
                
                print(f"Mean length of queue = {round(mean, 2)}") 
                print(f"Failures = {round(elem.failures, 2)}")
                print(f"Failure probability = {round(failure_prob, 2)}")
                print(f"Average element process time {round(avg_process_time, 2)}")
                print(f"Average worker process time {round(avg_worker_process_time, 2)}")
        
        print(f"\nTotal failures = {total_failures}\n")
