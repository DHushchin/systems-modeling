from generator import Generator


class Event:
    def __init__(self, delay, name, max_queue=0):
        self.delay = delay
        self.max_queue = max_queue
        self.name = name
        self.t_state = 0
        self.state = 0
        self.next = None
        self.queue = 0
        self.failure = 0
        self.served = 0
        self.mean_queue = 0

    def in_act(self, t_curr):
        pass

    def out_act(self, t_curr):
        self.served += 1

    def print_info(self):
        print("Event = " + self.name + " t_next = " + str(self.t_state) + " queue: " + str(self.queue) + " state = " + str(self.state))

    def print_statistics(self, time_modeling):
        print("Event = " + self.name + " served = " + str(self.served) + " failure = " + str(self.failure))

    def print_result(self):
        print(self.name + " served = " + str(self.served))

    def do_statistics(self, delta):
        pass

    def set_next_element(self, next_element):
        self.next = next_element

    def get_delay(self):
        return Generator.exp(self.delay)