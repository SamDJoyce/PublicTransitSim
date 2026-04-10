import unittest

from Tests.event_tests.test_event import EventTests


def event_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(EventTests))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(event_suite())
