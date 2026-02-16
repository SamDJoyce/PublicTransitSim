from abc import ABC, abstractmethod

class Event(ABC):
    def __init__(self, time: int):
        self.time = time

    @abstractmethod
    def process(self, simulator):
        ...

    def __lt__(self, other):
        return self.time < other.time

