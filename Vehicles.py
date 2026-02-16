from abc import ABC, abstractmethod
from typing import Optional

from Routes import Route


# ============================ #
# ===== Abstract Vehicle ===== #
# ============================ #
class Vehicle(ABC):
    #   =============
    # || Constructor ||
    #   =============
    def __init__(self, vehicle_id: str, route: Optional[Route] = None, ):
        self.vehicle_id = vehicle_id
        self.route = route

        self.current_stop_index = 0
        self.embarked_passengers = 0
        self.total_passengers_carried = 0
        self.total_travel_time = 0

    #   =================
    # || Abstract Methods ||
    #   =================
    @abstractmethod
    def dwell_time(self) -> int: pass
        # Time spent at a stop before departure

    @abstractmethod
    def speed(self) -> float: pass
        # Multiplier applied to travel time

    @abstractmethod
    def capacity(self): pass
        # Maximum passenger capacity

    #   ==================
    # || Concrete Methods ||
    #   ==================
    def current_stop(self):
        if self.route is None:
            raise ValueError("Vehicle has no assigned route.")
        return self.route.get_stop(self.current_stop_index)

    def has_next_stop(self) -> bool:
        if self.route is None:
            raise ValueError("Vehicle has no assigned route.")
        return  self.route.has_next_stop(self.current_stop_index)

    def at_last_stop(self) -> bool:
        if self.route is None:
            raise ValueError("Vehicle has no assigned route.")
        return self.route.is_last_stop(self.current_stop_index)

    def depart_stop(self):
        # Moves vehicle to its next stop and returns the adjusted travel time

        # Check for last stop
        if self.at_last_stop():
            raise IndexError("Vehicle has reached end of route.")
        #

        travel_time = self.route.get_travel_time(self.current_stop_index)

        adjusted_time = travel_time * self.speed()
        self.total_travel_time += adjusted_time
        self.current_stop_index += 1

        return adjusted_time

    #   ====================
    # || Passenger Handling ||
    #   ====================

    def embark_passengers(self, waiting_count: int) -> int:
        """
        Boards passengers up to vehicle capacity
        Returns the number who actually boarded
        """

        available_capacity = self.capacity() - self.embarked_passengers
        boarded = min(waiting_count, available_capacity)
        self.embarked_passengers += boarded
        self.total_passengers_carried += boarded

        return boarded

    def disembark_passengers(self, leaving_count: int) -> int:
        """
        Removes passengers from the vehicle
        Returns number who actually disembarked
        """

        leaving = min(leaving_count, self.embarked_passengers)
        self.embarked_passengers -= leaving
        return leaving

    def reset_route(self):
        self.current_stop_index = 0

# ======================== #
# ===== Standard Bus ===== #
# ======================== #

class Bus(Vehicle):
    pass