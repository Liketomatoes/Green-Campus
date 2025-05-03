"""Sensor classes & Observer (AlertManager) pattern"""
from abc import ABC, abstractmethod

class AlertManager:
    _subscribers = []

    @classmethod
    def subscribe(cls, fn):
        cls._subscribers.append(fn)

    @classmethod
    def notify(cls, message):
        for fn in cls._subscribers:
            fn(message)

class Sensor(ABC):
    """Abstract base class for different sensors"""
    def __init__(self, region):
        self.region = region

    @abstractmethod
    def read(self, value):
        ...

class ElectricSensor(Sensor):
    threshold = 1000  # kWh

    def read(self, value):
        if value > self.threshold:
            AlertManager.notify(f"High electricity consumption in {self.region}: {value} kWh")

class WaterSensor(Sensor):
    threshold = 500  # cubic meters

    def read(self, value):
        if value > self.threshold:
            AlertManager.notify(f"High water consumption in {self.region}: {value} m³")
