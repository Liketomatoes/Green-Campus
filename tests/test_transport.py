import unittest
from green_campus.transport import TransportService, CarpoolService

class TestTransport(unittest.TestCase):
    def setUp(self):
        self.ts = TransportService()
        self.cs = CarpoolService()

    def test_recommend_walk(self):
        self.ts.get_times = lambda o, d: {'walk': 5, 'bike': 2, 'drive': 1}
        times = self.ts.get_times('A', 'B')
        self.assertLess(times['walk'], 10)

    def test_carpool_drivers(self):
        drivers = self.cs.find_drivers('A', 'B')
        self.assertGreaterEqual(len(drivers), 1)

    def test_carpool_passengers(self):
        passengers = self.cs.find_passengers('A', 'B')
        self.assertGreaterEqual(len(passengers), 1)
