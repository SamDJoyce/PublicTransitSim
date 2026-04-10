import unittest

from Tests.event_tests.run_event_tests import event_suite
from Tests.passenger_tests.run_passenger_tests import passenger_suite
from Tests.route_tests.run_route_tests import route_suite
from Tests.simulator_tests.run_simulator_tests import simulator_suite
from Tests.stop_tests.run_stop_tests import stop_suite
from Tests.vehicle_tests.run_vehicle_tests import vehicle_suite


def all_tests():
    suite = unittest.TestSuite()
    suite.addTests(vehicle_suite())
    suite.addTests(passenger_suite())
    suite.addTests(stop_suite())
    suite.addTests(route_suite())
    suite.addTests(event_suite())
    suite.addTests(simulator_suite())
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(all_tests())
