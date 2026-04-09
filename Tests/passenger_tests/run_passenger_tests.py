import unittest

from Tests.passenger_tests.test_embark_disembark import PassengerHandlingTests
from Tests.passenger_tests.test_passenger import PassengerTests
from Tests.passenger_tests.test_passenger_time_calc import PassengerTimeCalcTests
from Tests.passenger_tests.test_passenger_trip_completion import TripCompletionTests


def passenger_suite():
   suite = unittest.TestSuite()
   suite.addTest(unittest.TestLoader().loadTestsFromTestCase(PassengerTests))
   suite.addTest(unittest.TestLoader().loadTestsFromTestCase(PassengerHandlingTests))
   suite.addTest(unittest.TestLoader().loadTestsFromTestCase(PassengerTimeCalcTests))
   suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TripCompletionTests))
   return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(passenger_suite())
