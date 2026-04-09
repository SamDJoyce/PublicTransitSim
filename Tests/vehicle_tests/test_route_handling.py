import unittest
from Tests.test_standins import MockRoute, MockStop
from Vehicles import Bus

class RouteHandlingTests(unittest.TestCase):
    def test_reset_route(self):
        bus = Bus("bus-1")
        bus.current_stop_index = 5

        bus.reset_route()

        self.assertEqual(bus.current_stop_index, 0)

    def test_deassign(self):
        route = MockRoute([MockStop("A")])
        bus = Bus("bus-1", route)

        bus.deassign()

        self.assertIsNone(bus.route)
        self.assertEqual(bus.current_stop_index, 0)
        self.assertEqual(len(bus.completed_routes), 1)


if __name__ == '__main__':
    unittest.main()
