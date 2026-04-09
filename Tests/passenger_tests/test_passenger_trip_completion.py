import unittest
from Passengers import Passenger
from Tests.test_standins import MockStop


class TripCompletionTests(unittest.TestCase):
    def setUp(self):
        self.stop_A = MockStop("A")
        self.stop_B = MockStop("B")

    def test_has_completed_trip_false(self):
        """
        Passenger has not completed trip until after disembark
        """
        a = self.stop_A
        b = self.stop_B
        p = Passenger(1, a, b, 0)
        assert not p.has_completed_trip()

    def test_has_completed_trip_true(self):
        """
        Passenger has completed trip after disembark
        """
        a = self.stop_A
        b = self.stop_B
        p = Passenger(1, a, b, 0)
        p.embark(5)
        p.disembark(10)
        assert p.has_completed_trip()

    def test_at_destination_true(self):
        """
        Passenger detects destination stop
        """
        a = self.stop_A
        b = self.stop_B
        p = Passenger(1, a, b, 0)
        assert p.at_destination(b)

    def test_at_destination_false(self):
        """
        Passenger detects non-destination stop
        """
        a = self.stop_A
        b = self.stop_B
        c = MockStop("C")
        p = Passenger(1, a, b, 0)
        assert not p.at_destination(c)

if __name__ == '__main__':
    unittest.main()
