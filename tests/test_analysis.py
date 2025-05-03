import unittest, datetime
from green_campus.analysis import classroom_analysis, restroom_analysis, lab_analysis, library_analysis, OCCUPANCY, SCHEDULE
from green_campus.sensors import AlertManager

events = []
AlertManager._subscribers.clear()
AlertManager.subscribe(lambda m: events.append(m))

class TestAnalysis(unittest.TestCase):
    def setUp(self):
        events.clear()
        OCCUPANCY.clear()
        SCHEDULE.clear()

    def test_classroom_alert(self):
        OCCUPANCY['C1'] = False
        classroom_analysis('C1', 10)
        self.assertTrue(events)

    def test_classroom_no_alert(self):
        OCCUPANCY['C1'] = True
        classroom_analysis('C1', 10)
        self.assertFalse(events)
