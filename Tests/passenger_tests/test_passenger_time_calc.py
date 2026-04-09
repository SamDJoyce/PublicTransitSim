import unittest
from Passengers import Passenger
from Tests.test_standins import MockStop

class PassengerTimeCalcTests(unittest.TestCase):
    def setUp(self):
        self.stop_A = MockStop("A")
        self.stop_B = MockStop("B")

    def test_wait_time_before_embark(self):
        """
        Wait time should be none before embark
        """
        a = self.stop_A
        b = self.stop_B
        p = Passenger(1, a, b, 5)
        assert p.wait_time() is None

    def test_wait_time_after_embark(self):
        """
        Wait time should be calculated after embark
        """
        a = self.stop_A
        b = self.stop_B
        p = Passenger(1, a, b, 5)
        p.embark(10)
        assert p.wait_time() == 5

    def test_travel_time_incomplete(self):
        """
        Travel time should be none before disembark
        """
        a = self.stop_A
        b = self.stop_B
        p = Passenger(1, a, b, 0)
        p.embark(5)
        assert p.travel_time() is None

    def test_travel_time_complete(self):
        """
        Travel time should be calculated after disembark
        """
        a = self.stop_A
        b = self.stop_B
        p = Passenger(1, a, b, 0)
        p.embark(5)
        p.disembark(15)
        assert p.travel_time() == 10

if __name__ == '__main__':
    unittest.main()
