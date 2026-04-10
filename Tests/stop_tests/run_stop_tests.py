import unittest

from Tests.stop_tests.test_stop import StopTests
from Tests.stop_tests.test_stop_equality import StopEqualityTests


def stop_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(StopTests))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(StopEqualityTests))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(stop_suite())
