import unittest
import pytest
from Routes import Route
from Stops import Stop
from Tests.test_standins import create_test_route


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.stop_A = Stop("A")
        self.stop_B = Stop("B")
        self.stop_C = Stop("C")
        self.route = create_test_route()

    def test_route_requires_minimum_stops(self):
        a = self.stop_A
        with pytest.raises(ValueError):
            Route(1, {a: None})

    def test_route_requires_final_time_none(self):
        a = self.stop_A
        b = self.stop_B
        c = self.stop_C
        segments = {
            a: 5,
            b: 10
        }
        with pytest.raises(ValueError):
            Route(1, segments)

    def test_is_last_stop(self):
        route = self.route
        assert not route.is_last_stop(0)
        assert route.is_last_stop(2)

    def test_has_next_stop(self):
        route = self.route
        assert route.has_next_stop(0)
        assert not route.has_next_stop(2)

    def test_get_next_stop(self):
        route = self.route
        b = self.stop_B
        c = self.stop_C
        assert route.get_next_stop(0) == b
        assert route.get_next_stop(1) == c

    def test_route_preserves_stop_order(self):
        a = self.stop_A
        b = self.stop_B
        c = self.stop_C
        segments = {
            a: 1,
            b: 2,
            c: None
        }
        route = Route(1, segments)

        assert route.stops() == [a, b, c]

if __name__ == '__main__':
    unittest.main()
