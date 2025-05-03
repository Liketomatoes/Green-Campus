"""Green transport recommendation & car‑pool mock"""
import random

class TransportService:
    def get_times(self, origin, destination):
        dist = random.uniform(0.5, 10.0)  # km
        return {
            'walk': dist / 5 * 60,   # minutes
            'bike': dist / 15 * 60,
            'drive': dist / 40 * 60
        }

class CarpoolService:
    def find_drivers(self, origin, destination):
        return [f"Driver{i}" for i in range(1, 4)]

    def find_passengers(self, origin, destination):
        return [f"Passenger{i}" for i in range(1, 4)]
