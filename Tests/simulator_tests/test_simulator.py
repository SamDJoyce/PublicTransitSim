import heapq
import unittest
from typing import List

from Events import StartService
from Simulator import Simulator
from Tests.test_standins import MockEvent, create_test_route, ChainedEvent
from Vehicles import Bus


class SimulatorTests(unittest.TestCase):
    def setUp(self):
        self.e1 = MockEvent(10)
        self.e2 = MockEvent(5)
        self.e3 = MockEvent(20)
        self.r1 = create_test_route()
        self.r2 = create_test_route()

    def test_schedule_event_orders_by_time(self):
        """
        Events are ordered by time
        """
        sim = Simulator()
        e1 = self.e1
        e2 = self.e2
        e3 = self.e3
        sim.schedule_event(e1)
        sim.schedule_event(e2)
        sim.schedule_event(e3)

        # heap pops smallest first
        assert sim.event_queue[0].time == 5

    def test_get_next_route(self):
        """
        Simulator should return the next available route
        """
        r1 = self.r1
        r2 = self.r2
        sim = Simulator()
        sim.route_queue.append(r1)
        sim.route_queue.append(r2)

        assert sim.has_next_route()

        route = sim.get_next_route()
        assert route is not None

    def test_get_next_route_empty(self):
        """
        Simulator can detect empty route_queue
        """
        sim = Simulator()
        assert sim.get_next_route() is None

    def test_run_processes_events_in_order(self):
        """
        Simulator should process the events in order
        """
        sim = Simulator()

        e1 = self.e1
        e2 = self.e2
        e3 = self.e3

        sim.schedule_event(e1)
        sim.schedule_event(e2)
        sim.schedule_event(e3)

        sim.run()

        # Check final time = last event
        assert sim.current_time == 20

        # Check logs include processed events
        messages = [entry.message for entry in sim.log]

        assert "Processed event at 5" in messages
        assert "Processed event at 10" in messages
        assert "Processed event at 20" in messages

    def test_run_with_no_events(self):
        """
        Simulator handles empty event_queue
        """
        sim = Simulator()
        sim.run()
        messages = [entry.message for entry in sim.log]

        assert "Starting simulation." in messages
        assert "Simulation complete." in messages

    def test_current_time_updates_correctly(self):
        """
        Simulator time should progress as events are processed
        """
        sim = Simulator()

        e1 = self.e1
        e2 = self.e2

        sim.schedule_event(e2)
        sim.schedule_event(e1)

        sim.run()

        assert sim.current_time == 10

    def test_event_can_schedule_new_events(self):
        """
        Events should schedule a next event
        """
        sim = Simulator()
        sim.schedule_event(ChainedEvent(5))
        sim.run()

        messages = [entry.message for entry in sim.log]

        assert "Processed event at 5" in messages
        assert "Processed event at 10" in messages

    def test_simulator_with_vehicle_event_flow(self):
        """
        Simulator handles vehicle event flow
        """
        sim = Simulator()
        route = self.r1
        bus = Bus("bus-1")
        sim.route_queue.append(route)
        event = StartService(5, bus)
        sim.schedule_event(event)

        sim.run()

        # Ensure simulation progressed
        assert sim.current_time >= 5
        assert len(sim.log) > 0

if __name__ == '__main__':
    unittest.main()
