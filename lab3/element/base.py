import random
from termcolor import colored

from element.generator import Generator

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

        # NEW
        self.probabilities = None
        self.blocked = None
        self.priorities = None


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

    # NEW
    def set_next_elements(self, next_elements, probabilities=None, priorities=None, blocked=None):
        self.next_elements = next_elements
        self.probabilities = probabilities
        self.blocked = blocked
        self.priorities = priorities


    def get_next_element(self):
        if not self.next_elements:
            return None
        
        # NEW
        if self.probabilities:
            while True:
                element = random.choices(self.next_elements, weights=self.probabilities)[0]
                if self.blocked is None or not self.blocked[self.next_elements.index(element)]:
                    return element

        if self.priorities:
            sorted_elements = [x for _, x in sorted(zip(self.priorities, self.next_elements), reverse=True, key=lambda x: x[0])]
            for element in sorted_elements:
                if self.blocked is None or not self.blocked[self.next_elements.index(element)]:
                    return element
            return None
        
        if self.blocked is not None:
            while True:
                element = random.choice(self.next_elements)
                if not self.blocked[self.next_elements.index(element)]:
                    return element

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
