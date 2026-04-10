import unittest

from Stops import Stop
from Tests.test_standins import MockPassenger


class StopTests(unittest.TestCase):

    def setUp(self):
        self.stop_A = Stop("A")

    def test_stop_initial_state(self):
        stop = self.stop_A
        assert stop.name == "A"
        assert stop.queue_length() == 0
        assert stop.total_arrivals == 0
        assert stop.total_boarded == 0

    def test_add_passenger(self):
        stop = self.stop_A
        p = MockPassenger(1)
        stop.add_passenger(p)
        assert stop.queue_length() == 1
        assert stop.total_arrivals == 1

    def test_add_multiple_passengers(self):
        stop = self.stop_A
        for i in range(5):
            stop.add_passenger(MockPassenger(i))

        assert stop.queue_length() == 5
        assert stop.total_arrivals == 5

    def test_queue_length(self):
        stop = self.stop_A
        stop.add_passenger(MockPassenger(1))
        assert stop.queue_length() == 1

    def test_has_waiting_passengers_true(self):
        stop = self.stop_A
        stop.add_passenger(MockPassenger(1))

        assert stop.has_waiting_passengers()

    def test_has_waiting_passengers_false(self):
        stop = self.stop_A
        assert not stop.has_waiting_passengers()

    def test_get_waiting_passengers(self):
        stop = self.stop_A
        p = MockPassenger(1)
        stop.add_passenger(p)
        queue = stop.get_waiting_passengers()
        assert queue == [p]

    def test_set_queue(self):
        stop = self.stop_A
        passengers = [MockPassenger(i) for i in range(3)]
        stop.set_queue(passengers)
        assert stop.queue_length() == 3

if __name__ == '__main__':
    unittest.main()
