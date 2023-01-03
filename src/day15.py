import re
from dataclasses import dataclass
from functools import cache
from typing import Iterable, Optional


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

    def __hash__(self):
        return hash((self.x, self.y))

    @property
    @cache
    def distance_to_closest_beacon(self) -> int:
        return abs(self.x - self.closest_beacon.x) + abs(self.y - self.closest_beacon.y)

    @property
    @cache
    def min_x(self) -> int:
        return self.x - self.distance_to_closest_beacon

    @property
    @cache
    def min_y(self) -> int:
        return self.y - self.distance_to_closest_beacon

    @property
    @cache
    def max_x(self) -> int:
        return self.x + self.distance_to_closest_beacon

    @property
    @cache
    def max_y(self) -> int:
        return self.y + self.distance_to_closest_beacon

    def row_coverage(self, y: int) -> Optional[tuple[int, int]]:
        if not self.min_y <= y <= self.max_y:
            return None

        x_offset = self.distance_to_closest_beacon - abs(self.y - y)
        return self.x - x_offset, self.x + x_offset

    @property
    def coverage(self) -> Iterable[tuple[int, int]]:
        for y in range(self.min_y, self.max_y + 1):
            row_coverage = self.row_coverage(y)
            for x in range(row_coverage[0], row_coverage[1] + 1):
                yield x, y


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
        if not (beacon := self.find_beacon(closest_beacon_x, closest_beacon_y)):
            beacon = Beacon(closest_beacon_x, closest_beacon_y)
            self._beacons.append(beacon)

        sensor = Sensor(x, y, beacon)
        self._sensors.append(sensor)
        return sensor

    def find_beacon(self, x: int, y: int) -> Optional[Beacon]:
        return next(iter([b for b in self._beacons if b.x == x and b.y == y]), None)

    def find_sensor(self, x: int, y: int) -> Optional[Sensor]:
        return next(iter([s for s in self._sensors if s.x == x and s.y == y]), None)


def puzzle1(filename: str, y: int):
    beacon_and_sensors = BeaconAndSensors.from_file(filename)
    row_coverage: set[int] = set()
    for sensor in beacon_and_sensors.sensors:
        if rc := sensor.row_coverage(y):
            row_coverage |= {x for x in range(rc[0], rc[1] + 1) if not beacon_and_sensors.find_beacon(x, y)}
    return len(row_coverage)


if __name__ == "__main__":
    print(puzzle1("../input/day15.txt", 2000000))
