from event_process import EventProcess

class Model:
    def __init__(self, create_event, process_events):
        self.t_next = 0.0
        self.t_curr = self.t_next
        self.state = 0
        self.events = [create_event] + process_events

    def simulate(self, time_modeling):
        while self.t_curr < time_modeling:
            self.t_next = float('inf')
            next_event = None

            for event in self.events:
                if event.t_state < self.t_next:
                    self.t_next = event.t_state
                    next_event = event

            print("\nIt's time for event in " + next_event.name + ", time = " + str(self.t_next))

            for event in self.events:
                event.do_statistics(self.t_next - self.t_curr)

            self.t_curr = self.t_next

            for event in self.events:
                if event.t_state == self.t_curr:
                    event.out_act(self.t_curr)

            self.print_info()

        self.print_result()

    def print_info(self):
        for event in self.events:
            if event.state == 1:
                event.print_info()

    def print_result(self):
        print("\n-------------RESULTS-------------")
        for event in self.events:
            event.print_result()
            if isinstance(event, EventProcess):
                mean_queue = event.mean_queue / self.t_curr
                failure_prob = event.failure / (event.served + event.failure)
                print("mean length of queue = " + str(mean_queue))
                print("failure probability = " + str(failure_prob))
            print()
