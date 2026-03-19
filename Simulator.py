import heapq
from typing import List

from Events import Event
from Passengers import Passenger
from Routes import Route
from Vehicles import Vehicle


class Simulator:
    """
    Runs the simulation by managing events and tracking time.
    Also collects logs and metrics from each simulation.
    """
    def __init__(self):
        self.vehicles     = {}
        self.route_queue  = []
        self.current_time: float = 0.0
        self.event_queue  = []
        self.completed_passengers: List[Passenger] = []
        self.log = []


    def get_next_route(self):
        if self.has_next_route():
            return heapq.heappop(self.route_queue)
        else:
            return None

    def has_next_route(self) -> bool:
        return len(self.route_queue) > 0

    def get_time_to_next_route(self):
        # TODO This should be dynamic
        #  current value is a placeholder
        return 10.0

    def schedule_event(self, event: Event):
        heapq.heappush(self.event_queue, event)

    def log_event(self, message: str):
        log_entry = f"[Time={self.current_time:.2f}] {message}"
        self.log.append(log_entry)
        print(log_entry)

    def clear_logs(self):
        self.completed_passengers = []
        self.log = []
        self.current_time = 0.0

    def run(self):
        self.clear_logs()
        self.log_event("Starting simulation.")
        while self.event_queue:
            event = heapq.heappop(self.event_queue)
            self.current_time = event.time
            event.process(self)
        self.log_event("Simulation complete.")