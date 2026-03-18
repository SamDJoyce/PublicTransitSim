from abc import ABC, abstractmethod
from typing import Optional, List

from Passengers import Passenger
from Routes import Route, Stop
from VehicleStates import State


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
        self.embarked_passengers: Optional[List[Passenger]] = []
        self.current_passenger_count: int = 0
        self.total_passengers_carried = 0
        self.total_travel_time = 0
        self.service_start_time = 0
        self.service_end_time = 0
        self.state = State.INIT

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
    def capacity(self) -> int: pass
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

    #   ====================
    # || Passenger Handling ||
    #   ====================

    def has_space(self) -> bool:
        return (self.capacity() - self.current_passenger_count) > 0

    def embark_passengers(self, queue: List[Passenger], simulator) -> List[Passenger]:
        """
        Boards passengers up to vehicle capacity.
        Returns the remaining passengers if any.
        """
        current_time = simulator.current_time
        remaining: List[Passenger] = []
        for passenger in queue:
            if self.has_space():
                passenger.embark(current_time)
                self.embarked_passengers.append(passenger)
                self.current_passenger_count += 1
                self.total_passengers_carried += 1
                # Log the event
                simulator.log_event(
                    f"Passenger #{passenger.passenger_id} has boarded vehicle {self.vehicle_id}."
                )
            else:
                remaining.append(passenger)
        if len(remaining) > 0:
            simulator.log_event(
                f"Vehicle {self.vehicle_id} is full. {len(remaining)} passengers could not board."
            )
        return remaining

    def disembark_passengers(self, simulator) -> List[Passenger]:
        """
        Removes passengers from the vehicle
        Returns a list of Passengers who have completed their trip
        """
        current_time = simulator.current_time
        remaining: List[Passenger] = []
        disembarking:List[Passenger] = []
        for passenger in self.embarked_passengers:
            if passenger.at_destination(self.current_stop()):
                passenger.disembark(current_time)
                disembarking.append(passenger)
                # Log the event
                simulator.log_event(
                    f"Passenger #{passenger.passenger_id} has reached their destination: {self.current_stop().name}."
                )
            else:
                remaining.append(passenger)
        self.embarked_passengers = remaining
        return disembarking

    def reset_route(self):
        self.current_stop_index = 0

    def deassign(self):
        self.route = None
        self.current_stop_index = 0

# ======================== #
# ===== Standard Bus ===== #
# ======================== #

class Bus(Vehicle):
    def __init__(self, vehicle_id: str, route: Optional[Route] = None, ):
        super().__init__(vehicle_id, route)
        self._dwell_time = 1
        self._speed      = 1.0
        self._capacity   = 60

    def dwell_time(self) -> int:
        return self._dwell_time

    def speed(self) -> float:
        return self._speed

    def capacity(self) -> int:
        return self._capacity