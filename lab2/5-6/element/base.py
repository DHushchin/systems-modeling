import random
from .generator import Generator
from termcolor import colored


class Element:
    next_id = 0

    def __init__(self, name, mean_delay, distribution):
        self.tnext = float('inf')
        self.mean_delay = mean_delay
        self.distribution = distribution
        self.tcurr = self.tnext
        self.state = 0
        self.processed = 0
        self.next_elements = []
        self.id = Element.next_id
        Element.next_id += 1
        self.name = name if name else f"element_{self.id}"


    def get_delay(self):
        delay = self.mean_delay
        
        if self.distribution == "exp":
            delay = Generator.exp(self.mean_delay)
        elif self.distribution == "norm":
            delay = Generator.norm(self.mean_delay, 1)
        elif self.distribution == "unif":
            delay = Generator.unif(0, 2 * self.mean_delay)
        elif self.distribution == "empiric":
            delay = Generator.empiric([1, 2, 3], [0.2, 0.5, 0.3])
        else:
            raise Exception("Unknown distribution")

        return delay


    def get_next_element(self):
        if not self.next_elements:
            return None

        return random.choice(self.next_elements)


    def out_act(self):
        self.processed += 1


    def print_result(self):
        print()
        print(colored(self.name, "green"))
        print(f"Processed = {self.processed}")


    def print_info(self):
        print(f"{self.name} | state={self.state} | processed={self.processed} | tnext={self.tnext}")


    def do_statistics(self, delta):
        pass