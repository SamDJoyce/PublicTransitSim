import unittest

from Vehicles import Bus


class VehicleCapacityTests(unittest.TestCase):
    def test_has_space_true(self):
        bus = Bus("bus-1")
        bus.current_passenger_count = 10
        self.assertTrue(bus.has_space())

    def test_has_space_false(self):
        bus = Bus("bus-1")
        bus.current_passenger_count = bus.capacity()
        self.assertFalse(bus.has_space())


if __name__ == '__main__':
    unittest.main()
