import unittest

from Tests.route_tests.test_route import RouteTests
from Tests.route_tests.test_route_timing import RouteTimingTests


def route_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(RouteTests))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(RouteTimingTests))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(route_suite())