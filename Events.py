from abc import ABC, abstractmethod

from VehicleStates import State


# ================================ #
# ===== Abstract Event Class ===== #
# ================================ #
class Event(ABC):
    """
    Base class for all simulation events.
    Events are ordered by scheduled time.
    """
    def __init__(self, time: int):
        if time < 0:
            raise ValueError("Time cannot be negative.")
        self.time = time

    @abstractmethod
    def process(self, simulator):
        pass
        """
        Execute the event logic.
        """

    def __lt__(self, other):
        return self.time < other.time

# =========================== #
# ===== Concrete Events ===== #
# =========================== #
class StartService(Event):
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        pass

class AssignRoute(Event):
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        pass

class DeassignRoute(Event):
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        pass

class ArriveAtStop(Event):
    """
    Arrive at a stop.
    """
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        current_time = self.time
        vehicle = self.vehicle
        # Set vehicle state
        vehicle.state = State.AT_STOP
        # Begin dwelling at stop
        simulator.schedule_event(
            DwellAtStop(current_time, vehicle)
        )

class DwellAtStop(Event):
    """
    Wait at a stop while passengers load and unload
    """
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        current_time = self.time
        vehicle = self.vehicle
        stop = vehicle.current_stop()
        # Set state
        self.vehicle.state = State.DWELL

        # Disembark Passengers
        completed = vehicle.disembark_passengers(stop, current_time)
        simulator.completed_passengers.extend(completed)

        # Embark Passengers
        waiting_queue = stop.get_waiting_passengers()
        remaining_queue = vehicle.embark_passengers(waiting_queue, current_time)
        # Excess passengers remain at the stop
        stop.set_queue(remaining_queue)

        # Calculate dwell time
        base_dwell = vehicle.dwell_time()
        passenger_exchange_count = len(completed) + (len(waiting_queue)-len(remaining_queue))
        per_passenger_time = 0.5
        exchange_time = per_passenger_time * passenger_exchange_count
        adjusted_dwell = base_dwell + exchange_time

        # Schedule Departure
        if vehicle.has_next_stop():
            departure_time = current_time + adjusted_dwell
            simulator.schedule_event(
                DepartStop(departure_time, vehicle)
            )
        else:
            simulator.schedule_event(FinalDwellComplete(current_time, vehicle))

class DepartStop(Event):
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        pass

class FinalDwellComplete(Event):
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        pass

class EndService(Event):
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        pass

class TrafficDelay(Event):
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        pass

class Breakdown(Event):
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        pass

class RepairInProgression(Event):
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        pass

class DelayComplete(Event):
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        pass

class CannotRepair(Event):
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        pass

