import unittest

from Routes import Route
from Stops import Stop
from Tests.test_standins import create_test_route


class RouteTimingTests(unittest.TestCase):
    def setUp(self):
        self.route = create_test_route()

    def test_get_travel_time(self):
        route = self.route

        assert route.get_travel_time(0) == 5
        assert route.get_travel_time(1) == 10

    def test_total_route_duration(self):
        route = self.route
        assert route.get_total_route_duration() == 15

    def test_zero_travel_time_allowed(self):
        a = Stop("A")
        b = Stop("B")
        segments = {
            a: 0,
            b: None
        }
        route = Route(1, segments)
        assert route.get_travel_time(0) == 0

    def test_full_route_traversal(self):
        route = self.route
        a = Stop("A")
        b = Stop("B")
        c = Stop("C")

        index = 0
        visited = []

        while True:
            visited.append(route.get_stop(index))
            if route.is_last_stop(index):
                break
            index += 1

        assert visited == [a, b, c]


if __name__ == '__main__':
    unittest.main()
