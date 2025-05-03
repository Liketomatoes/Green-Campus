"""Energy use pattern analysis"""
import datetime
from .sensors import AlertManager

OCCUPANCY = {}  # region -> bool
SCHEDULE = {}   # lab -> bool

def classroom_analysis(region, consumption):
    if not OCCUPANCY.get(region, False) and consumption > 0:
        AlertManager.notify(f"High electricity in empty classroom {region}")

def restroom_analysis(region, flow_records):
    night_flows = [f for t, f in flow_records if datetime.time(1,0) <= t <= datetime.time(5,0)]
    if not OCCUPANCY.get(region, False) and any(f > 0 for f in night_flows):
        AlertManager.notify(f"Water usage detected overnight in restroom {region}")

def lab_analysis(region, consumption):
    if not SCHEDULE.get(region, False) and consumption > 0:
        AlertManager.notify(f"Electricity use in unscheduled lab {region}")

def library_analysis(region, consumption):
    if not OCCUPANCY.get(region, False) and consumption > 0:
        AlertManager.notify(f"Electricity in empty library area {region}")
