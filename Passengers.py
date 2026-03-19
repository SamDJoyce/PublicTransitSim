from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from Routes import Stop


# =========================== #
# ===== Passenger Class ===== #
# =========================== #

class Passenger:
    """
    Represents a single passenger within the simulation.
    Tracks trip data.
    """
    #   =============
    # || Constructor ||
    #   =============
    def __init__(
            self,
            passenger_id: int,
            origin_stop: "Stop",
            destination_stop: "Stop",
            arrival_time: float
    ):
        if origin_stop == destination_stop:
            raise Exception('origin_stop and destination_stop cannot be the same')

        self.passenger_id = passenger_id
        self.origin_stop = origin_stop
        self.destination_stop = destination_stop
        self.arrival_time = arrival_time
        self.embark_time: Optional[float] = None
        self.disembark_time: Optional[float] = None

    #   ===============
    # || State Updates ||
    #   ===============

    def embark(self, time: float):
        if self.embark_time is not None:
            raise ValueError("Passenger has already embarked.")
        self.embark_time = time

    def disembark(self, time: float):
        if self.embark_time is None:
            raise ValueError("Passenger cannot disembark before embarking.")
        if self.disembark_time is not None:
            raise ValueError("Passenger has already disembarked.")
        self.disembark_time = time

    #   =========
    # || Metrics ||
    #   =========
    def wait_time(self) -> Optional[float]:
        """
        Time waited at stop before boarding.
        """
        if self.embark_time is None:
            return None
        return self.embark_time - self.arrival_time

    def travel_time(self) -> Optional[float]:
        """
        Time spent onboard a vehicle.
        """
        if self.embark_time is None or self.disembark_time is None:
            return None
        return self.disembark_time - self.embark_time

    def total_trip_time(self) -> Optional[float]:
        """
        Total time from arrival at origin to destination.
        This includes wait time at the stop.
        """
        if self.disembark_time is None:
            return None
        return self.disembark_time - self.arrival_time

    def has_completed_trip(self) -> bool:
        return self.disembark_time is not None

    #   =========
    # || Helpers ||
    #   =========
    def at_destination(self, stop: "Stop") -> bool:
        """
        Returns True if the provided stop is this passenger's destination.
        """
        return self.destination_stop == stop
