from typing import List

from SimulationLog import SimulationLog


class Metrics:
    """
    Collects logs and stats from simulation logs.
    """
    def __init__(self):
        self.saved_logs: List[SimulationLog] = []

    def save_log(self, log):
        """
        Save the event to the log
        :param log:    event to be saved
        """
        self.saved_logs.append(log)

    def get_log(self, index: int):
        """
        Return the log entry at the given index
        :param index:
        """
        return self.saved_logs[index]

    def clear_saved_logs(self):
        """
        Clear the saved logs
        """
        self.saved_logs = []

    def number_of_saved_logs(self):
        """
        :return: a count of saved logs
        """
        return len(self.saved_logs)

    def print_log(self, index: int):
        """
        Print the event at the given index
        :param index:
        """
        for event in self.saved_logs[index].event_log:
            print(event.__str__())

    def print_vehicle_data(self, index: int):
        """
        Print the data for the vehicle at the given index
        :param index:
        """
        log = self.saved_logs[index]
        for vehicle in log.vehicles.values():
            print(f"\nVehicle: {vehicle.vehicle_id}")
            print(f"Vehicle Type: {vehicle.type}")
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
        """
        Print the data for the passenger at the given index
        :param index:
        """
        log = self.saved_logs[index]
        print("-" * 30)
        print(f"\nCompleted Trips: {log.num_completed_trips()}")
        print("")

    def print_all(self, index: int):
        """
        Print log, vehicle, and passenger for the log at the given index
        :param index:
        """
        self.print_log(index)
        self.print_vehicle_data(index)
        self.print_passenger_data(index)

