import unittest
from green_campus.sensors import ElectricSensor, WaterSensor, AlertManager

events = []
AlertManager._subscribers.clear()
AlertManager.subscribe(lambda m: events.append(m))

class TestResourceMonitoring(unittest.TestCase):
    def setUp(self):
        events.clear()

    def test_electric_positive(self):
        es = ElectricSensor('TestRegion')
        es.read(1500)
        self.assertTrue(any('High electricity' in m for m in events))

    def test_electric_negative(self):
        es = ElectricSensor('TestRegion')
        es.read(800)
        self.assertFalse(events)

    def test_water_positive(self):
        ws = WaterSensor('TestRegion')
        ws.read(600)
        self.assertTrue(any('High water' in m for m in events))

    def test_water_negative(self):
        ws = WaterSensor('TestRegion')
        ws.read(400)
        self.assertFalse(events)
