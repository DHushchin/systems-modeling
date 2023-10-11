from event import Event

class EventCreate(Event):
    def out_act(self, t_curr):
        super().out_act(t_curr)
        self.t_state = t_curr + self.get_delay()
        self.next.in_act(t_curr)

    def do_statistics(self, delta):
        self.mean_queue += self.queue * delta