from typing import Dict, Deque,List, Optional
from collections import deque

from Passengers import Passenger


# ====================== #
# ===== Stop Class ===== #
# ====================== #
class Stop:
    """
    Represents a stop where passengers queue.
    Manages waiting passenger queue and boarding.
    """
    #   =============
    # || Constructor ||
    #   =============
    def __init__(self, name: str):
        self.name = name
        self._waiting_passengers: Deque[Passenger] = deque()

        # Metrics
        self.total_arrivals = 0
        self.total_boarded = 0

    #   ======================
    # || Passenger Management ||
    #   ======================
    def add_passenger(self, passenger: Passenger):
        """
        Adds a passenger to the queue.
        """
        self._waiting_passengers.append(passenger)
        self.total_arrivals += 1
    def queue_length(self) -> int:
        return len(self._waiting_passengers)

    def has_waiting_passengers(self) -> bool:
        return len(self._waiting_passengers) > 0

    #   ==========
    # || Boarding ||
    #   ==========
    def embark_passengers(self, vehicle, current_time: int) -> List[Passenger]:
        """
        Embarks waiting passengers onto vehicle.
        Returns list of embarked passengers.
        """
        boarded_passengers = []

        while (
            self.has_waiting_passengers()
            and vehicle.embarked_passengers < vehicle.capacity()
        ):
            passenger = self._waiting_passengers.popleft()
            passenger.embark(current_time)
            vehicle.embarked_passengers += 1
            vehicle.total_arrivals += 1
            boarded_passengers.append(passenger)
            self.total_boarded += 1
        return boarded_passengers

    # Ensure Stops can be compared
    def __str__(self):
        return f"Stop({self.name})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Stop):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

# ======================= #
# ===== Route Class ===== #
# ======================= #
class Route:
    #   =============
    # || Constructor ||
    #   =============
    def __init__(self, route_id: int, segments: Dict[Stop, Optional[int]]):

        # Check to ensure there are at least 2 stops
        if len(segments) < 2 :
            raise ValueError("Route must have at least 2 stops")
        stops = list(segments.keys())

        # Check to ensure there is a final stop (no travel time)
        if segments[stops[-1]] is not None:
            raise ValueError("Final stop must have travel time = None")

        self.route_id = route_id
        self._segments = dict(segments)
        self._stops: List[Stop] = stops

    #   =================
    # || Getters/Setters ||
    #   =================

    def stops(self) -> List[Stop]:
        return self._stops

    def get_stop(self, index: int) -> Stop:
        return self._stops[index]

    def number_of_stops(self) -> int:
        return len(self._stops)

    def is_last_stop(self, index: int) -> bool:
        return index == len(self._stops) - 1

    def has_next_stop(self, index: int) -> bool:
        return index < len(self._stops) - 1

    def get_travel_time(self, index: int) -> int:
        """
        Returns the travel time from stop[index]
        to stop[index+1]
        """
        stop_name = self._stops[index]
        travel_time = self._segments[stop_name]

        if travel_time is None:
            raise ValueError("This is the final stop. No travel time")
        return travel_time

    def get_total_route_duration(self):
        duration = 0
        for stop, travel_time in self._segments.items():
            if travel_time is not None:
                duration += travel_time
        return duration

    def get_next_stop(self, index: int) -> Stop:
        if self.is_last_stop(index):
            raise ValueError("This is the final stop.")
        return self._stops[index + 1]