import csv
import os

from SimulationLog import SimulationLog
from Vehicles import Vehicle


class SaveFile:
    """
    Saves simulation data to CSV files.
    """
    def __init__(self, log: SimulationLog):
        self.save_dir = "sim_logs"
        self.log = log

    def save_log_to_disk(self):
        """
        Save the data from a Simulation Log as CSV files.
        Saves Log messages to file event_log_DATE_TIME.csv.
        Saves Vehicle data to file vehicles_DATE_TIME.csv.
        Saves Passenger data to file passengers_DATE_TIME.csv.
        """
        log = self.log
        # Ensure the save directory exists
        os.makedirs(self.save_dir, exist_ok=True)
        # Save log data
        self._save_log_data(log)
        # Save Vehicle data
        self._save_vehicle_data(log)
        # Save Passenger data
        self._save_passenger_data(log)

    def _save_log_data(self, log: SimulationLog):
        """
        Save the logged events to a CSV file with columns:
        time, message
        :param log: The event log to be saved
        """
        log_file = self._format_save_name(log, "event_log")

        with open(log_file, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Time", "Message"])

            for entry in log.event_log:
                writer.writerow([entry.time, entry.message])

    def _save_vehicle_data(self, log: SimulationLog):
        """
        Save vehicle data to a CSV file with columns:
        vehicle_id, routes, vehicle_type, service_start_time,
        service_end_time, total_service_time, total_passengers_carried
        :param log: The log to be saved
        """
        vehicles_file = self._format_save_name(log, "vehicles")
        with open(vehicles_file, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Vehicle_ID",
                             "Vehicle_type",
                             "Routes",
                             "service_start_time",
                             "service_end_time",
                             "total_service_time",
                             "total_passengers_carried"])
            for vehicle in log.vehicles.values():
                routes = self._format_routes(vehicle)
                writer.writerow([vehicle.vehicle_id,
                                 vehicle.type,
                                 routes,
                                 vehicle.service_start_time,
                                 vehicle.service_end_time,
                                 vehicle.total_service_time(),
                                 vehicle.total_passengers_carried])

    def _save_passenger_data(self, log: SimulationLog):
        """
        Save passenger data to a CSV file with columns:
        passenger_id, embark_time, disembark_time, origin,
        destination, travel_time, wait_time, trip_time
        :param log: The log to be saved
        """
        passengers_file = self._format_save_name(log, "passengers")
        with open(passengers_file, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Passenger_ID",
                             "Embark_Time",
                             "Disembark_Time",
                             "Origin",
                             "Destination",
                             "Travel_time",
                             "Wait_time",
                             "Trip_time"])
            for passenger in log.completed_passengers:
                writer.writerow([passenger.passenger_id,
                                 passenger.embark_time,
                                 passenger.disembark_time,
                                 passenger.origin_stop.name,
                                 passenger.destination_stop.name,
                                 passenger.travel_time(),
                                 passenger.wait_time(),
                                 passenger.total_trip_time()])

    def _format_save_name(self, log, file_type: str):
        """
        Construct the name of the log file to be saved
        :param log:         The log to be saved
        :param file_type:   The type of data to be saved
        :return:            The path of the saved file
        """
        save_time = log.timestamp.strftime("%Y-%m-%d_%H-%M")
        file_name = file_type + "_" + save_time + ".csv"
        log_file = os.path.join(self.save_dir, file_name)
        return log_file

    def _format_routes(self, vehicle: Vehicle):
        """
        Format the route information to be saved
        :param vehicle: The vehicle whose routes are to be formatted
        :return:        String of all route data
        """
        routes: str = ""
        first = True
        for route in vehicle.completed_routes:
            if not first:
                routes = routes + "; " + str(route.route_id)
            else:
                routes = str(route.route_id)
                first = False
        return routes