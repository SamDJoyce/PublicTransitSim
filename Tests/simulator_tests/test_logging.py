import unittest

from Simulator import Simulator
from Tests.test_standins import MockPassenger


class LoggingTests(unittest.TestCase):
    def setUp(self):
        self.passenger = MockPassenger(1)

    def test_log_event_adds_entry(self):
        """
        Log entries are saved
        """
        sim = Simulator()
        sim.log_event("Test message")

        assert len(sim.log) == 1
        assert sim.log[0].message == "Test message"

    def test_clear_logs_resets_state(self):
        """
        Clear_logs resets the state of the log_queue
        """
        sim = Simulator()
        p = self.passenger

        sim.log_event("Test")
        sim.completed_passengers.append(p)
        sim.current_time = 50

        sim.clear_logs()

        assert sim.log == []
        assert sim.completed_passengers == []
        assert sim.current_time == 0.0



if __name__ == '__main__':
    unittest.main()
