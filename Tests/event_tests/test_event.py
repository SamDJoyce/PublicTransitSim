import random
import unittest
from unittest.mock import patch

import pytest
from Events import Event, StartService, AssignRoute, ArriveAtStop, DwellAtStop, DepartStop, FinalDwellComplete, \
    DeassignRoute, EndService, TrafficDelay, DelayComplete, Breakdown, CannotRepair, RepairInProgress
from Tests.test_standins import MockSimulator, create_test_route, MockPassenger
from VehicleStates import State
from Vehicles import Bus

class EventTests(unittest.TestCase):
    def setUp(self):
        self.bus = Bus("bus-1")
        self.sim = MockSimulator()
        self.route = create_test_route()

    def test_start_service_sets_state_and_schedules(self):
        """
        Event properly beings service and sets state
        """
        sim = self.sim
        bus = self.bus

        event = StartService(10, bus)
        event.process(sim)

        assert bus.service_start_time == 10
        assert bus.state == State.IDLE
        assert isinstance(sim.events[0], AssignRoute)


    def test_assign_route_assigns_and_sets_state(self):
        """
        Event properly assigns route and sets state
        """
        sim = self.sim
        bus = self.bus
        route = self.route
        sim.routes = [route]

        event = AssignRoute(10, bus)
        event.process(sim)

        assert bus.route == route
        assert bus.state.name == "HEADING_TO_ROUTE_START"
        assert len(sim.events) == 1

    def test_assign_route_when_already_assigned(self):
        """
        Vehicle already has route
        """
        sim = self.sim
        route = self.route
        bus = self.bus
        bus.route = route
        event = AssignRoute(10, bus)

        with pytest.raises(RuntimeError):
            event.process(sim)

    def test_arrive_at_stop_sets_state_and_schedules(self):
        """
        Vehicle properly arrives at stop and sets state
        """
        sim = self.sim
        route = self.route
        bus = self.bus
        bus.route = route
        event = ArriveAtStop(10, bus)

        event.process(sim)

        assert bus.state.name == "AT_STOP"
        assert isinstance(sim.events[0], DwellAtStop)

    def test_dwell_processes_passengers_and_schedules_departure(self):
        """
        Vehicle dwells and processes passengers, then sets state
        """
        sim = self.sim
        route = self.route
        bus = self.bus
        bus.route = route
        stop = route.get_stop(0)

        # Add passenger
        p = MockPassenger(1, route.get_stop(1))
        stop.add_passenger(p)

        event = DwellAtStop(10, bus)
        event.process(sim)

        assert bus.state.name == "DWELL"
        assert bus.current_passenger_count >= 0
        assert len(sim.events) == 1

    def test_depart_stop_normal_flow(self):
        """
        Vehicle departs stop and sets state
        """
        sim = self.sim
        route = self.route
        bus = self.bus
        bus.route = route

        # No breakdowns/traffic
        with patch("random.randrange", return_value=100):
            event = DepartStop(10, bus)
            event.process(sim)

        assert bus.state.name == "IN_TRANSIT"
        assert isinstance(sim.events[0], ArriveAtStop)

    def test_depart_stop_at_last_stop_raises(self):
        """
        Vehicle cannot depart last stop
        """
        sim = self.sim
        route = self.route
        bus = self.bus
        bus.route = route
        bus.current_stop_index = 2  # last stop

        event = DepartStop(10, bus)

        with pytest.raises(IndexError):
            event.process(sim)

    def test_final_dwell_complete(self):
        """
        Vehicle completes final dwell and sets state
        """
        sim = self.sim
        route = self.route
        bus = self.bus
        bus.route = route
        bus.current_stop_index = 2  # last stop

        event = FinalDwellComplete(10, bus)
        event.process(sim)

        assert bus.state.name == "ROUTE_COMPLETE"
        assert isinstance(sim.events[0], DeassignRoute)

    def test_end_service(self):
        """
        Vehicle ends service, records end time, and sets state
        """
        sim = self.sim
        bus = self.bus

        event = EndService(20, bus)
        event.process(sim)

        assert bus.service_end_time == 20
        assert bus.state == State.OUT_OF_SERVICE

    def test_traffic_delay(self):
        """
        Vehicle experiences a delay and sets state
        """
        sim = self.sim
        bus = self.bus

        event = TrafficDelay(10, bus)
        event.process(sim)

        assert bus.state.name == "DELAYED"
        assert isinstance(sim.events[0], DelayComplete)

    def test_breakdown_branching(self):
        """
        Vehicle breaks down but is repairable
        """

        sim = self.sim
        bus = self.bus

        # Force repairable = True
        with patch("random.randrange", return_value=1):
            event = Breakdown(10, bus)
        event.process(sim)

        assert bus.state.name == "BREAKDOWN"
        assert isinstance(sim.events[0], CannotRepair) or isinstance(sim.events[0], RepairInProgress)

    def test_delay_complete(self):
        """
        Vehicle completes delay and sets state
        """
        sim = self.sim
        bus = self.bus

        event = DelayComplete(10, bus)
        event.process(sim)

        assert bus.state.name == "IN_TRANSIT"
        assert isinstance(sim.events[0], ArriveAtStop)

    def test_cannot_repair(self):
        sim = self.sim
        route = self.route
        bus = self.bus
        bus.route = route

        event = CannotRepair(10, bus)
        event.process(sim)

        assert bus.state == State.OUT_OF_SERVICE
        assert bus.route is None

if __name__ == '__main__':
    unittest.main()
