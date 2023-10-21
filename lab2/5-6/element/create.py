from .base import Element

class Create(Element):
    def __init__(self, name, mean_delay=1.0, distribution="exp"):
        super().__init__(name, mean_delay, distribution)
        self.tnext = 0.0

    def out_act(self):
        super().out_act()
        self.tnext = self.tcurr + self.get_delay()
        el = self.get_next_element()
        if el:
            el.in_act()
