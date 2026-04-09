import unittest
import pytest

from Passengers import Passenger
from Tests.test_standins import MockStop


class PassengerTests(unittest.TestCase):
    def setUp(self):
        self.stop_A = MockStop("A")
        self.stop_B = MockStop("B")

    def test_invalid_same_origin_destination(self):
        """
        Passenger cannot have the same destination and origin
        """
        a = self.stop_A
        with pytest.raises(Exception):
            Passenger(1, a, a, 0)

    def test_valid_passenger_creation(self):
        """
        Passenger creation assigns values correctly
        """
        a = self.stop_A
        b = self.stop_B
        p = Passenger(1, a, b, 5)

        assert p.passenger_id == 1
        assert p.arrival_time == 5
        assert p.embark_time is None
        assert p.disembark_time is None

if __name__ == '__main__':
    unittest.main()
