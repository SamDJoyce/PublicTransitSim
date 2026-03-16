import random
from abc import ABC, abstractmethod
from typing import Any

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

# ============================= #
# ===== In Service Events ===== #
# ============================= #
class StartService(Event):
    """
    Begin vehicle lifecycle
    """
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        vehicle = self.vehicle
        current_time = self.time
        vehicle.service_start_time = current_time
        vehicle.state = State.IDLE
        simulator.schedule_event(AssignRoute(current_time, vehicle))
        # Print information to the console
        print(current_time)
        print("Vehicle #" + vehicle.vehicle_id + " has entered service.")
        print("Vehicle #" + vehicle.vehicle_id + " is now " + vehicle.state.__str__())

class AssignRoute(Event):
    """
    Assign a route to the current vehicle.
    """
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        current_time = self.time
        vehicle = self.vehicle

        # Ensure the vehicle does not already have a route assigned
        if vehicle.route is not None:
            raise RuntimeError("Vehicle has a route assigned already.")

        # Get route from the simulator
        route = simulator.get_next_route()
        if route is None:
            raise RuntimeError("No routes remaining in queue.")
        vehicle.route = route
        vehicle.state = State.HEADING_TO_ROUTE_START
        # Print information to the console
        print(current_time)
        print("Vehicle #" + vehicle.vehicle_id + " has been assigned route " + route.route_id + ".")
        print("Vehicle #" + vehicle.vehicle_id + " is now " + vehicle.state.__str__())

        # Check to see if the vehicle is already at the first stop
        if vehicle.current_stop() == vehicle.route.get_stop(self,0):
            # Vehicle is already at first stop
            simulator.schedule_event(
                ArriveAtStop(current_time, vehicle)
            )
        else:
            # Vehicle is not at first stop
            simulator.schedule_event(
                DepartStop(current_time, vehicle)
            )

class DeassignRoute(Event):
    """
    Remove the current vehicle from the route.
    """
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        current_time = self.time
        vehicle = self.vehicle
        vehicle.state = State.IDLE
        # Print information to the console
        print(current_time)
        print("Vehicle #" + vehicle.vehicle_id + " has been removed from route " + vehicle.route.route_id + ".")
        print("Vehicle #" + vehicle.vehicle_id + " is now " + vehicle.state.__str__())
        vehicle.route.deassign()

        # Check to see if there are more routes assigned
        if simulator.has_next_route():
            simulator.schedule_event(
                AssignRoute(current_time, vehicle)
            )
        else :
            simulator.schedule_event(
                EndService(current_time, vehicle)
            )


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
        # Print information to the console
        print(current_time)
        print("Vehicle #" + vehicle.vehicle_id + " arrived at stop " + vehicle.current_stop().name + ".")
        print("Vehicle #" + vehicle.vehicle_id + " is now " + vehicle.state.__str__())
        # Begin dwelling at stop
        simulator.schedule_event(
            DwellAtStop(current_time, vehicle)
        )

class DwellAtStop(Event):
    """
    Wait at a stop while passengers load and unload.
    """
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle
        self.per_passenger_time = 0.5

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
        exchange_time = self.per_passenger_time * passenger_exchange_count
        adjusted_dwell = base_dwell + exchange_time

        # Print information to the console
        print(current_time)
        print("Vehicle #" + vehicle.vehicle_id + " is at stop " + vehicle.current_stop().name + ".")
        print("Vehicle #" + vehicle.vehicle_id + " is now " + vehicle.state.__str__())

        # Schedule Departure
        if vehicle.has_next_stop():
            departure_time = current_time + adjusted_dwell
            simulator.schedule_event(
                DepartStop(departure_time, vehicle)
            )
        else:
            simulator.schedule_event(FinalDwellComplete(current_time, vehicle))

class DepartStop(Event):
    """
    Depart a stop and begin traveling.
    """
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle
        self.CHANCE_OF_TRAFFIC = 10
        self.CHANCE_OF_BREAKDOWN = 1
        self.traffic = random.randrange(1,100) <= self.CHANCE_OF_TRAFFIC
        self.breakdown = random.randrange(1,100) <= self.CHANCE_OF_BREAKDOWN

    def process(self, simulator):
        current_time = self.time
        vehicle = self.vehicle

        # Check for valid next stop
        if vehicle.at_last_stop():
            raise IndexError("Vehicle cannot depart final stop: no next stop.")

        # TODO conditional to check for delay or breakdown and direct down that route
        # Set State
        vehicle.state = State.IN_TRANSIT

        # Print information to the console
        print(current_time)
        print("Vehicle #" + vehicle.vehicle_id + " departed stop " + vehicle.current_stop().name + ".")
        print("Vehicle #" + vehicle.vehicle_id + " is now " + vehicle.state.__str__())

        # Get travel time to:
             # Route Start
        if vehicle.state == State.HEADING_TO_ROUTE_START:
            base_travel_time = simulator.get_time_to_next_route()
        else: # Next Stop
            base_travel_time = vehicle.route.get_travel_time(
                vehicle.current_stop_index
            )
            vehicle.current_stop_index += 1
        arrival_time = self.calculate_travel_time(base_travel_time, current_time, vehicle)

        # Check for delays
        if self.breakdown: # Breakdown delay
            simulator.schedule_event(Breakdown(arrival_time, vehicle))
        elif self.traffic: # Traffic delay
            simulator.schedule_event(TrafficDelay(arrival_time, vehicle))
        else: # Schedule Arrival
            simulator.schedule_event(
                ArriveAtStop(arrival_time, vehicle)
            )

    def calculate_travel_time(self, base_travel_time, current_time: int, vehicle) -> int | Any:
        adjusted_travel_time = base_travel_time * vehicle.speed()
        vehicle.total_travel_time += adjusted_travel_time
        arrival_time = current_time + adjusted_travel_time
        return arrival_time


class FinalDwellComplete(Event):
    """
    Executes after final stop dwell completes.
    """
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        current_time = self.time
        vehicle = self.vehicle

        if not vehicle.at_last_stop():
            raise RuntimeError("FinalDwellComplete triggered when not at last stop.")
        vehicle.state = State.ROUTE_COMPLETE
        # Print information to the console
        print(current_time)
        print("Vehicle #" + vehicle.vehicle_id + " is at stop " + vehicle.current_stop().name + ".")
        print("This was the final stop on this vehicles current route.")
        print("Vehicle #" + vehicle.vehicle_id + " is now " + vehicle.state.__str__())
        # TODO add possibility of route repeats,
        #  ie perform the same route 3 times in a row
        #  would schedule RestartRoute event
        simulator.schedule_event(
            DeassignRoute(current_time, vehicle)
        )

class RestartRoute(Event):
    """
    Begin the same route again, from the first stop.
    """
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        ... #TODO


class EndService(Event):
    """
    Vehicle exits service when no further routes
    are available.
    """
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        vehicle = self.vehicle
        current_time = self.time
        vehicle.service_end_time = current_time
        vehicle.state = State.OUT_OF_SERVICE
        # Print information to the console
        print(current_time)
        print("Vehicle #" + vehicle.vehicle_id + " is now " + vehicle.state.__str__())


# ======================== #
# ===== Delay Events ===== #
# ======================== #
class TrafficDelay(Event):
    """
    Delay transit from one stop to another.
    """
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        vehicle = self.vehicle
        current_time = self.time
        vehicle.state = State.DELAYED

        # Print information to the console
        print(current_time)
        print("Vehicle #" + vehicle.vehicle_id + " is now " + vehicle.state.__str__())

        # Calculate length of delay
        delay_time = random.randrange(1,5)
        current_time += delay_time

        #Schedule end of delay
        simulator.schedule_event(DelayComplete(current_time, vehicle))

class Breakdown(Event):
    """
    Mechanical problem with the vehicle.
    Determine if repair is possible.
    """
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle
        self.repair_chance = 80
        self.repairable = random.randrange(1, 100) <= self.repair_chance

    def process(self, simulator):
        vehicle = self.vehicle
        current_time = self.time
        vehicle.state = State.BREAKDOWN

        # Print information to the console
        print(current_time)
        print("Vehicle #" + vehicle.vehicle_id + " is experiencing a " + vehicle.state.__str__())
        if self.repairable:
            # Vehicle cannot be repaired
            print("Vehicle cannot be repaired.")
            simulator.schedule_event(CannotRepair(current_time, vehicle))
        else:
            # Vehicle can be repaired
            print("Vehicle can be repaired")
            simulator.schedule_event(RepairInProgress(current_time, vehicle))

class RepairInProgress(Event):
    """
    Repairs are possible, add delay time.
    """
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        vehicle = self.vehicle
        current_time = self.time
        vehicle.state = State.DELAYED
        # Print information to the console
        print(current_time)
        print("Vehicle #" + vehicle.vehicle_id + " is being repaired.")

        # Calculate length of delay
        delay_time = random.randrange(10,30)
        current_time += delay_time
        # Schedule end of delay
        simulator.schedule_event(DelayComplete(current_time, vehicle))

class DelayComplete(Event):
    """
    Delay is complete and vehicle can continue to next stop.
    """
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        vehicle = self.vehicle
        current_time = self.time
        vehicle.state = State.IN_TRANSIT
        # Print information to the console
        print(current_time)
        print("Vehicle #" + vehicle.vehicle_id + " has completed its delay.")
        # Schedule next event
        simulator.schedule_event(ArriveAtStop(current_time, vehicle))

class CannotRepair(Event):
    """
    Mechanical problem is too significant,
    and cannot be repaired.
    This ends the route prematurely.
    """
    def __init__(self, time: int, vehicle):
        super().__init__(time)
        self.vehicle = vehicle

    def process(self, simulator):
        vehicle = self.vehicle
        current_time = self.time
        vehicle.service_end_time = current_time
        vehicle.state = State.OUT_OF_SERVICE
        # Print information to the console
        print(current_time)
        print("Vehicle #" + vehicle.vehicle_id + " is now " + vehicle.state.__str__())
