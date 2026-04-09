import unittest

from Tests.test_standins import MockStop, MockRoute
from Vehicles import Bus

class VehicleTests(unittest.TestCase):

    def setUp(self):
        stops = [MockStop("A"), MockStop("B")]
        self.route = MockRoute(stops)
        self.bus = Bus("bus-1", self.route)

    def test_current_stop(self):
        self.assertEqual(self.bus.current_stop().name, "A")

    def test_has_next_stop(self):
        self.assertTrue(self.bus.has_next_stop())

    def test_at_last_stop(self):
        self.assertFalse(self.bus.at_last_stop())

        self.bus.current_stop_index = 1
        self.assertTrue(self.bus.at_last_stop())

    def test_total_service_time(self):
        self.bus.service_start_time = 5
        self.bus.service_end_time = 15
        self.assertEqual(self.bus.total_service_time(), 10)