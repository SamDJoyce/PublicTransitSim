import unittest
import pytest
from Passengers import Passenger
from Tests.test_standins import MockStop


class PassengerHandlingTests(unittest.TestCase):
    def setUp(self):
        self.stop_A = MockStop("A")
        self.stop_B = MockStop("B")

    def test_double_embark_raises(self):
        """
        Cannot embark twice
        """
        a = self.stop_A
        b = self.stop_B
        p = Passenger(1, a, b, 0)
        p.embark(10)

        with pytest.raises(ValueError):
            p.embark(15)

    def test_double_disembark_raises(self):
        """
        Cannot disembark twice
        """
        a = self.stop_A
        b = self.stop_B
        p = Passenger(1, a, b, 0)

        p.embark(5)
        p.disembark(10)

        with pytest.raises(ValueError):
            p.disembark(15)

    def test_disembark_before_embark_raises(self):
        """
        Cannot disembark before embark
        """
        a = self.stop_A
        b = self.stop_B
        p = Passenger(1, a, b, 0)

        with pytest.raises(ValueError):
            p.disembark(10)

    def test_disembark_sets_time(self):
        """
        Disembark sets disembark_time
        """
        a = self.stop_A
        b = self.stop_B
        p = Passenger(1, a, b, 0)

        p.embark(5)
        p.disembark(15)

        assert p.disembark_time == 15


if __name__ == '__main__':
    unittest.main()
