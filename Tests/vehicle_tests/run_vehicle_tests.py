import unittest

from Tests.vehicle_tests.test_disembark import DisembarkTests
from Tests.vehicle_tests.test_embark import EmbarkTests
from Tests.vehicle_tests.test_route_handling import RouteHandlingTests
from Tests.vehicle_tests.test_vehicle_capacity import VehicleCapacityTests
from Tests.vehicle_tests.test_vehicles import VehicleTests


def vehicle_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(VehicleTests))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(VehicleCapacityTests))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(RouteHandlingTests))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(EmbarkTests))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(DisembarkTests))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(vehicle_suite())
