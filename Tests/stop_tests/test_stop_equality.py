import unittest
from Stops import Stop

class StopEqualityTests(unittest.TestCase):

    def test_stop_equality_same_name(self):
        s1 = Stop("A")
        s2 = Stop("A")
        assert s1 == s2

    def test_stop_equality_different_name(self):
        s1 = Stop("A")
        s2 = Stop("B")
        assert s1 != s2

    def test_stop_equality_other_type(self):
        stop = Stop("A")
        assert stop != "A"

    def test_stop_hash(self):
        s1 = Stop("A")
        s2 = Stop("A")
        assert hash(s1) == hash(s2)

    def test_stop_in_set(self):
        s1 = Stop("A")
        s2 = Stop("A")
        stops = {s1}
        assert s2 in stops

    def test_str_representation(self):
        stop = Stop("A")
        assert str(stop) == "Stop(A)"

if __name__ == '__main__':
    unittest.main()
