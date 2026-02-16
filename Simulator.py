import heapq

from Events import Event


class Simulator:
    def __init__(self):
        self.current_time = 0
        self.event_q = []

    def schedule_event(self, event: Event):
        heapq.heappush(self.event_q, event)

    def run(self):
        while self.event_q:
            event = heapq.heappop(self.event_q)
            self.current_time = event.time
            event.process(self)
