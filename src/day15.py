import re
from dataclasses import dataclass
from functools import cache
from typing import Optional


@dataclass
class BeaconSensorBase:
    x: int
    y: int


@dataclass
class Beacon(BeaconSensorBase):

    def __str__(self):
        return "B"


@dataclass
class Sensor(BeaconSensorBase):
    closest_beacon: Beacon

    def __str__(self):
        return "S"

    @property
    def distance_to_closest_beacon(self) -> int:
        return abs(self.x - self.closest_beacon.x) + abs(self.y - self.closest_beacon.y)

    @property
    def min_x(self) -> int:
        return self.x - self.distance_to_closest_beacon

    @property
    def min_y(self) -> int:
        return self.y - self.distance_to_closest_beacon

    @property
    def max_x(self) -> int:
        return self.x + self.distance_to_closest_beacon

    @property
    def max_y(self) -> int:
        return self.y + self.distance_to_closest_beacon


class BeaconAndSensors:

    @classmethod
    def from_file(cls, filename):
        result = cls()
        with open(filename, "r") as fp:
            for line in fp:
                if match := re.match(
                    "^Sensor at "
                    "x=(?P<x>[-]?\d+), "
                    "y=(?P<y>[-]?\d+): "
                    "closest beacon is at "
                    "x=(?P<closest_beacon_x>[-]?\d+), "
                    "y=(?P<closest_beacon_y>[-]?\d+)\s*$",
                    line
                ):
                    result.add_sensor(**{k: int(v) for k, v in match.groupdict().items()})
        return result

    def __init__(self):
        self._beacons: list[Beacon] = []
        self._sensors: list[Sensor] = []

    def __str__(self):
        result = ""
        for y in range(self.min[1], self.max[1] + 1):
            for x in range(self.min[0], self.max[0] + 1):
                result += f"{self.find_beacon(x, y) or self.find_sensor(x, y) or '.'}"
            if y < self.max[1]:
                result += "\n"
        return result

    @property
    def beacons(self) -> list[Beacon]:
        return self._beacons[:]

    @property
    def sensors(self) -> list[Sensor]:
        return self._sensors

    @property
    @cache
    def all_coordinates(self) -> list[tuple[int, int]]:
        return [(b.x, b.y) for b in self._beacons] + [(s.x, s.y) for s in self._sensors]

    @property
    @cache
    def min(self) -> tuple[int, int]:
        all_x = []
        all_y = []

        for x, y in self.all_coordinates:
            all_x.append(x)
            all_y.append(y)

        return min(all_x), min(all_y)

    @property
    @cache
    def max(self) -> tuple[int, int]:
        all_x = []
        all_y = []

        for x, y in self.all_coordinates:
            all_x.append(x)
            all_y.append(y)

        return max(all_x), max(all_y)

    def add_sensor(self, x: int, y: int, closest_beacon_x: int, closest_beacon_y: int) -> Sensor:
        if beacon := self.find_beacon(closest_beacon_x, closest_beacon_y) is None:
            beacon = Beacon(closest_beacon_x, closest_beacon_y)
            self._beacons.append(beacon)

        sensor = Sensor(x, y, beacon)
        self._sensors.append(sensor)
        return sensor

    def find_beacon(self, x: int, y: int) -> Optional[Beacon]:
        return next(iter([b for b in self._beacons if b.x == x and b.y == y]), None)

    def find_sensor(self, x: int, y: int) -> Optional[Sensor]:
        return next(iter([s for s in self._sensors if s.x == x and s.y == y]), None)


if __name__ == "__main__":
    beacon_and_sensors = BeaconAndSensors.from_file("../input/day15sample.txt")
    sensor = beacon_and_sensors.find_sensor(8, 7)
    beacon = sensor.closest_beacon
    print(sensor.x, sensor.y)
    print(beacon.x, beacon.y)
    print(sensor.min_x, sensor.min_y)
    print(sensor.max_x, sensor.max_y)
