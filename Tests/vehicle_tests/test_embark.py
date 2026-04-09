import unittest

from Tests.test_standins import MockPassenger, MockSimulator
from Vehicles import Bus


class EmbarkTests(unittest.TestCase):
    def setUp(self):
        self.bus = Bus("bus-1")
        self.sim = MockSimulator()

    def test_embark_with_space(self):
        passengers = [MockPassenger(i) for i in range(3)]

        remaining = self.bus.embark_passengers(passengers, self.sim)

        self.assertEqual(len(self.bus.embarked_passengers), 3)
        self.assertEqual(self.bus.current_passenger_count, 3)
        self.assertEqual(len(remaining), 0)

    def test_embark_respects_capacity(self):
        self.bus._capacity = 2  # override for test

        passengers = [MockPassenger(i) for i in range(5)]
        remaining = self.bus.embark_passengers(passengers, self.sim)

        self.assertEqual(self.bus.current_passenger_count, 2)
        self.assertEqual(len(remaining), 3)

    def test_embark_logs_events(self):
        passengers = [MockPassenger(1)]
        self.bus.embark_passengers(passengers, self.sim)

        self.assertTrue(any("has boarded vehicle" in log for log in self.sim.logs))


if __name__ == '__main__':
    unittest.main()
