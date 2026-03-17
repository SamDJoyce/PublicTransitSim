from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
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
        self._waiting_passengers: List["Passenger"] = []

        # Metrics
        self.total_arrivals = 0
        self.total_boarded = 0

    #   ======================
    # || Passenger Management ||
    #   ======================
    def add_passenger(self, passenger: "Passenger"):
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
    def get_waiting_passengers(self) -> List["Passenger"]:
        return self._waiting_passengers

    def set_queue(self, passengers: List["Passenger"]):
        self._waiting_passengers = passengers

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