# test_helpers.py
from Events import Event
from Routes import Route
from Stops import Stop


class MockPassenger:
    def __init__(self, passenger_id, destination=None):
        self.passenger_id = passenger_id
        self.destination = destination
        self.embarked_time = None
        self.disembarked_time = None

    def embark(self, time):
        self.embarked_time = time

    def disembark(self, time):
        self.disembarked_time = time

    def at_destination(self, stop):
        return stop == self.destination


class MockStop:
    def __init__(self, name):
        self.name = name


class MockRoute:
    def __init__(self, stops):
        self.stops = stops

    def get_stop(self, index):
        return self.stops[index]

    def has_next_stop(self, index):
        return index < len(self.stops) - 1

    def is_last_stop(self, index):
        return index == len(self.stops) - 1


class MockSimulator:
    def __init__(self):
        self.current_time = 0
        self.events = []
        self.logs = []
        self.completed_passengers = []
        self.routes = []
        self.route_index = 0

    def schedule_event(self, event):
        self.events.append(event)

    def log_event(self, msg):
        self.logs.append(msg)

    def get_next_route(self):
        if self.route_index < len(self.routes):
            r = self.routes[self.route_index]
            self.route_index += 1
            return r
        return None

    def has_next_route(self):
        return self.route_index < len(self.routes)

    def get_time_to_next_route(self):
        return 5  # constant for testing

class MockEvent(Event):
    def __init__(self, time, vehicle =None):
        super().__init__(time, vehicle)

    def process(self, simulator):
        simulator.log_event(f"Processed event at {self.time}")

class ChainedEvent(MockEvent):
    def process(self, simulator):
        super().process(simulator)
        if self.time == 5:
            simulator.schedule_event(MockEvent(10))

def create_test_route():
    a = Stop("A")
    b = Stop("B")
    c = Stop("C")
    segments = {
        a: 5,
        b: 10,
        c: None  # final stop
    }
    return Route(1, segments)