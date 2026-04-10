import copy
from datetime import datetime
from typing import List

from Passengers import Passenger

class SimulationLog:
    """
    A collection of simulation data:
    - event log
    - vehicles objects
    - passengers objects
    """
    def __init__(self, log, vehicles, passengers):
        self.timestamp = datetime.now()
        self.event_log = copy.deepcopy(log)
        self.vehicles = copy.deepcopy(vehicles)
        self.completed_passengers: List[Passenger] = copy.deepcopy(passengers)

    # ============================= #
    # ===== Passenger Metrics ===== #
    # ============================= #
    def num_completed_trips(self):
        """
        :return: Count of passengers who reached their destination
        """
        return len(self.completed_passengers)

    def avg_travel_time(self):
        """
        :return: Average passenger travel time
        """
        total_time = 0.0
        for passenger in self.completed_passengers:
            total_time += passenger.travel_time()
        return total_time / self.num_completed_trips()

    def avg_trip_time(self):
        """
        :return: Average passenger trip time (includes wait at stop)
        """
        total_time = 0.0
        for passenger in self.completed_passengers:
            total_time += passenger.total_trip_time()
        return total_time / self.num_completed_trips()

    def avg_wait_time(self):
        """
        :return: Average passenger time waiting at stop before pickup
        """
        total_time = 0.0
        for passenger in self.completed_passengers:
            total_time += passenger.wait_time()
        return total_time / self.num_completed_trips()

    # ============================ #
    # ===== Vehicle Metrics ====== #
    # ============================ #
    def num_vehicles(self):
        """
        :return: Count of vehicles used in the simulation
        """
        return len(self.vehicles)

    def avg_service_time(self):
        """
        :return: Average vehicle service time
        """
        total_time = 0.0
        for vehicle in self.vehicles.values():
            total_time += vehicle.total_service_time()
        return total_time / self.num_vehicles()

    def avg_passengers_carried(self):
        """
        :return: Average passengers carried per vehicle
        """
        return self.total_passengers_carried() / self.num_vehicles()

    def total_passengers_carried(self):
        """
        :return: Count of passengers carried by all vehicles
        """
        total_passengers = 0
        for vehicle in self.vehicles.values():
            total_passengers += vehicle.total_passengers_carried
        return total_passengers

    # ==================== #
    # ===== Helpers ====== #
    # ==================== #
    def timestamp_string(self):
        """
        :return: Uniformly formatted timestamp string
        """
        return self.timestamp.strftime("%Y-%m-%d_%H-%M")