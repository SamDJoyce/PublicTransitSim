import unittest

from Tests.simulator_tests.test_full_sim import FullSimTests
from Tests.simulator_tests.test_logging import LoggingTests
from Tests.simulator_tests.test_simulator import SimulatorTests


def simulator_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(SimulatorTests))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(LoggingTests))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(FullSimTests))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(simulator_suite())
