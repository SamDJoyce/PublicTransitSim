from typing import List

from SimulationLog import SimulationLog


class Metrics:
    def __init__(self):
        self.saved_logs: List[SimulationLog] = []

    def save_log(self, log):
        self.saved_logs.append(log)

    def get_log(self, index: int):
        return self.saved_logs[index]

    def clear_saved_logs(self):
        self.saved_logs = []

    def number_of_saved_logs(self):
        return len(self.saved_logs)

    def print_log(self, index: int):
        for event in self.saved_logs[index].event_log:
            print(event.__str__())

    def print_vehicle_data(self, index: int):
        log = self.saved_logs[index]
        for vehicle in log.vehicles.values():
            print(f"\nVehicle: {vehicle.vehicle_id}")
            print(f"Began Service: {vehicle.service_start_time}")
            print(f"Ended Service: {vehicle.service_end_time:.2f}")
            print(f"Total travel time: {vehicle.total_travel_time}")
            print(f"Total service time: {vehicle.total_service_time():.2f}")
            print(f"Total carried passengers: {vehicle.total_passengers_carried}")
        print("-" * 30)
        print(f"\nCumulative Vehicle Data")
        print(f"Total number of vehicles: {log.num_vehicles()}")
        print(f"Total passengers carried by all vehicles: {log.total_passengers_carried()}")
        print(f"Average service time per vehicle: {log.avg_service_time():.2f}")
        print(f"Average passengers carried per vehicle: {log.avg_passengers_carried()}")

    def print_passenger_data(self, index: int):
        log = self.saved_logs[index]
        print("-" * 30)
        print(f"\nCompleted Trips: {log.num_completed_trips()}")
        print("")

    def print_all(self, index: int):
        self.print_log(index)
        self.print_vehicle_data(index)
        self.print_passenger_data(index)

