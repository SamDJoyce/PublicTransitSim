import heapq
import random

import yaml

from Passengers import Passenger
from Routes import Route, Stop
from Vehicles import Bus, DoubleDeckerBus, Articulated


class Loader:
    """
    Loads configuration data from a YAML file.
    """
    def __init__(self, filepath: str):
        with open(filepath, "r") as file:
            self.data = yaml.safe_load(file)
        self.routes = []
        self.vehicles = {}
        self.passenger_counter = 1
        self._load_routes()
        self._load_vehicles()

    # ========================= #
    # ===== Route Loading ===== #
    # ========================= #

    def _load_routes(self):
        """
        Loads routes data from the designated YAML file.
        """
        # Load all routes listed
        for route_data in self.data["routes"]:
            route_id = route_data["id"]
            segments = {}
            stops = []
            stops_config = []
            # Load each stop for the current route
            for stop_data in route_data["stops"]:
                # Get stop description
                stop = Stop(stop_data["name"])
                travel_time = stop_data["travel_time"]
                # Assemble the stop
                segments[stop] = travel_time
                stops.append(stop)
                # Get and store stop population stats
                min_pass = stop_data.get("min_pass", 0)
                max_pass = stop_data.get("max_pass", 0)
                stops_config.append((stop, min_pass, max_pass))
            # Assemble route
            route = Route(route_id, segments)
            # Add route to route list
            self.routes.append(route)
            print("Route #" + str(route_id) + " loaded.")
            # Generate passengers for route
            self._generate_passengers(stops, stops_config)

    # =========================== #
    # ===== Vehicle Loading ===== #
    # =========================== #

    def _load_vehicles(self):
        """
        Loads vehicles data from the designated YAML file.
        """
        for vehicle_data in self.data["vehicles"]:
            vehicle_id = vehicle_data["id"]
            vehicle_type = vehicle_data["type"]


            if vehicle_type == "bus":
                vehicle = Bus(vehicle_id)
                print("Bus #" + str(vehicle_id) + " loaded.")
            elif vehicle_type == "Double-Decker Bus":
                vehicle = DoubleDeckerBus(vehicle_id)
                print("Double-Decker Bus #" + str(vehicle_id) + " loaded.")
            elif vehicle_type == "Articulated Bus":
                vehicle = Articulated(vehicle_id)
                print("Articulated Bus #" + str(vehicle_id) + " loaded.")
            else:
                raise ValueError(f"Unknown vehicle type: {vehicle_type}")

            self.vehicles[vehicle_id] = vehicle

    # =============================== #
    # ===== Generate Passengers ===== #
    # =============================== #

    def _generate_passengers(self, stops, stops_config):
        """
        Generate passengers for each stop from the YAML file data.

        :param stops:           collection of stops
        :param stops_config:    the maximum and minimum number of passengers
                                for each stop
        """
        print("Generating passengers.")
        for i, (origin_stop, min_pass, max_pass) in enumerate(stops_config):

            # Vehicle does not pick up from last stop
            # so do not generate passengers.
            if i == len(stops) - 1:
                continue
            # Otherwise determine the number of passengers
            num_passengers = random.randint(min_pass, max_pass)
            # Create the details for each passenger
            for each in range(num_passengers):
                # Select destination stop
                destination_stop = random.choice(stops[i + 1:])
                # Create Passenger object
                passenger = Passenger(
                    passenger_id = self.passenger_counter,
                    origin_stop = origin_stop,
                    destination_stop = destination_stop,
                    arrival_time = 0
                )
                # Increment counter
                self.passenger_counter += 1
                # Add passenger to stop queue
                origin_stop.add_passenger(passenger)