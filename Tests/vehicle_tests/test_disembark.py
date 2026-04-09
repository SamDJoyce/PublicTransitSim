import unittest
from Tests.test_standins import MockStop, MockRoute, MockSimulator, MockPassenger
from Vehicles import Bus

class DisembarkTests(unittest.TestCase):
    def setUp(self):
        stops = [MockStop("A"), MockStop("B")]
        self.route = MockRoute(stops)
        self.bus = Bus("bus-1", self.route)
        self.sim = MockSimulator()

    def test_disembark_at_destination(self):
        passenger = MockPassenger(1, destination=self.route.get_stop(0))
        self.bus.embarked_passengers = [passenger]
        self.bus.current_passenger_count = 1

        done = self.bus.disembark_passengers(self.sim)

        self.assertEqual(len(done), 1)
        self.assertEqual(self.bus.current_passenger_count, 0)

    def test_passenger_stays_if_not_destination(self):
        passenger = MockPassenger(1, destination=None)
        self.bus.embarked_passengers = [passenger]
        self.bus.current_passenger_count = 1

        done = self.bus.disembark_passengers(self.sim)

        self.assertEqual(len(done), 0)
        self.assertEqual(self.bus.current_passenger_count, 1)


if __name__ == '__main__':
    unittest.main()
