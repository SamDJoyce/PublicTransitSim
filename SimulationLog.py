import copy
from typing import List

from Passengers import Passenger

class SimulationLog:
    def __init__(self, log, vehicles, passengers):
        self.log = copy.deepcopy(log)
        self.vehicles = copy.deepcopy(vehicles)
        self.completed_passengers: List[Passenger] = copy.deepcopy(passengers)

    # ============================= #
    # ===== Passenger Metrics ===== #
    # ============================= #
    def num_completed_trips(self):
        return len(self.completed_passengers)

    def avg_travel_time(self):
        total_time = 0.0
        for passenger in self.completed_passengers:
            total_time += passenger.travel_time()
        return total_time / self.num_completed_trips()

    def avg_trip_time(self):
        total_time = 0.0
        for passenger in self.completed_passengers:
            total_time += passenger.total_trip_time()
        return total_time / self.num_completed_trips()

    def avg_wait_time(self):
        total_time = 0.0
        for passenger in self.completed_passengers:
            total_time += passenger.wait_time()
        return total_time / self.num_completed_trips()

    # ============================ #
    # ===== Vehicle Metrics ====== #
    # ============================ #
    def num_vehicles(self):
        return len(self.vehicles)

    def avg_service_time(self):
        total_time = 0.0
        for vehicle in self.vehicles.values():
            total_time += vehicle.total_service_time()
        return total_time / self.num_vehicles()

    def avg_passengers_carried(self):
        return self.total_passengers_carried() / self.num_vehicles()

    def total_passengers_carried(self):
        total_passengers = 0
        for vehicle in self.vehicles.values():
            total_passengers += vehicle.total_passengers_carried
        return total_passengers