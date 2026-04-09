# test_helpers.py

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
        self.current_time = 10
        self.logs = []

    def log_event(self, msg):
        self.logs.append(msg)