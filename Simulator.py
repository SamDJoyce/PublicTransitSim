import heapq
from typing import List

from Events import Event
from Passengers import Passenger


class Simulator:
    def __init__(self):
        self.current_time = 0
        self.event_queue = []
        self.completed_passengers: List[Passenger] = []

    def schedule_event(self, event: Event):
        heapq.heappush(self.event_queue, event)

    def run(self):
        while self.event_queue:
            event = heapq.heappop(self.event_queue)
            self.current_time = event.time
            event.process(self)
