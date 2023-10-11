from event import Event


class EventProcess(Event):
    def in_act(self, t_curr):
        if self.state == 0:
            self.state = 1
            self.t_state = t_curr + self.get_delay()
        else:
            if self.queue < self.max_queue:
                self.queue += 1
            else:
                self.failure += 1

    def out_act(self, t_curr):
        super().out_act(t_curr)
        self.t_state = float('inf')
        self.state = 0
        if self.queue > 0:
            self.queue -= 1
            self.state = 1
            self.t_state = t_curr + self.get_delay()
        if self.next is not None:
            self.next.in_act(t_curr)

    def do_statistics(self, delta):
        self.mean_queue += self.queue * delta

    def print_result(self):
        super().print_result()
        print("failure = " + str(self.failure))