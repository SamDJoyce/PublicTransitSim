import unittest
from unittest.mock import patch

from Events import StartService
from Passengers import Passenger
from Routes import Route
from Simulator import Simulator
from Stops import Stop
from Vehicles import Bus


class FullSimTests(unittest.TestCase):
    def test_full_simulation_passenger_trip(self):
        # --- Setup simulator ---
        sim = Simulator()

        # --- Create stops ---
        a = Stop("A")
        b = Stop("B")

        # --- Create route ---
        segments = {
            a: 5,  # A -> B takes 5 time units
            b: None
        }
        route = Route(1, segments)

        # Add route to simulator
        sim.route_queue.append(route)

        # --- Create vehicle ---
        bus = Bus("bus-1")

        # --- Create passenger ---
        passenger = Passenger(
            passenger_id=1,
            origin_stop=a,
            destination_stop=b,
            arrival_time=0
        )

        # Passenger is already waiting at stop A
        a.add_passenger(passenger)

        # --- Schedule simulation start ---
        sim.schedule_event(StartService(0, bus))

        # --- Disable randomness (no traffic, no breakdowns) ---
        with patch("Events.random.randrange", return_value=100):
            sim.run()

        # --- Assertions ---

        # Passenger completed trip
        assert passenger.has_completed_trip()

        # Passenger ended at correct time
        assert passenger.disembark_time is not None

        # Travel time should be 6.1
        # (5 + bus dwell time[1] + passenger embark time[0.1])
        assert passenger.travel_time() == 6.1

        # Passenger recorded in simulator
        assert passenger in sim.completed_passengers

        # Vehicle finished route
        assert bus.route is None or bus.state.name in ["ROUTE_COMPLETE", "OUT_OF_SERVICE"]

        # Simulation progressed
        assert sim.current_time >= 5


if __name__ == '__main__':
    unittest.main()
