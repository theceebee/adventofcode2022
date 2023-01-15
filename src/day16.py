from __future__ import annotations
import re
import sys
from functools import cache
from operator import itemgetter


class Valve:

    def __init__(self, name: str, flow_rate: int):
        self.name: str = name
        self.flow_rate: int = flow_rate
        self.is_open: bool = False
        self._connected_valves: list[Valve] = []

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return f"Valve {self.name} has flow rate={self.flow_rate}; tunnels lead to valves {', '.join([valve.name for valve in self._connected_valves])}"

    @property
    def connected_valves(self):
        return self._connected_valves[:]

    def add_connected_valve(self, valve: Valve):
        self._connected_valves.append(valve)

    def open_valve(self):
        self.is_open = True


class ValveList(list):

    @classmethod
    def from_file(cls, filename):
        result = cls()

        with open(filename, "r") as fp:

            while line := fp.readline():
                match = re.match("Valve (?P<name>[A-Z]{2}) has flow rate=(?P<flow_rate>[0-9][0-9]?);.*", line)
                result.append(Valve(name=match.group("name"), flow_rate=int(match.group("flow_rate"))))

            fp.seek(0)

            index_sentinel = 0
            while line := fp.readline():
                line_ = line.split(";")[-1].strip()
                for valve in re.findall("[A-Z]{2}", line_):
                    other = next(iter([r for r in result if r.name == valve]))
                    result[index_sentinel].add_connected_valve(other)
                index_sentinel += 1

        return result

    @property
    def graph(self) -> Graph:
        result = Graph(number_of_vertices=len(self))
        for u, valve in enumerate(self):
            for connected_valve in valve.connected_valves:
                v = next(iter([i for i, other in enumerate(self) if connected_valve == other]))
                result.add_edge(u, v)
        return result


class Graph:

    @classmethod
    def from_file(cls, filename):
        with open(filename, "r") as fp:
            lines = fp.readlines()

        result = cls(number_of_vertices=len(lines))
        for line in lines:
            ...

    def __init__(self, number_of_vertices: int):
        self._number_of_vertices = number_of_vertices
        self._adjacency_matrix = [
            [
                0 for __ in range(number_of_vertices)
            ]
            for __ in range(number_of_vertices)
        ]

    def __str__(self):
        result = ""

        for i in range(self._number_of_vertices):
            result += " ".join([str(j) for j in self._adjacency_matrix[i]])
            if i < self._number_of_vertices - 1:
                result += "\n"

        return result

    def add_edge(self, u: int, v: int, w: int = 1):
        self._adjacency_matrix[u][v] = w

    @cache
    def dijkstra(self, src: int) -> list[int]:

        visited: list[int] = []
        cost: list[int] = []
        prev: list[int] = []

        for __ in range(self._number_of_vertices):
            visited.append(0)
            cost.append(sys.maxsize)
            prev.append(-1)

        cost[src] = 0

        for i in range(self._number_of_vertices):
            min_cost = sorted([(i, c, v) for i, (c, v) in enumerate(zip(cost, visited)) if not v], key=itemgetter(1))[0][0]

            if cost[min_cost] == sys.maxsize:
                break

            for j in range(self._number_of_vertices):

                if not self.is_adjacent(i, j):
                    continue

                new_cost = cost[min_cost] + self.weight(i, j)
                if new_cost < cost[j]:
                    cost[j] = new_cost
                    prev[j] = min_cost

            visited[min_cost] = 1

        return cost

    def is_adjacent(self, u: int, v: int) -> bool:
        return self._adjacency_matrix[u][v] > 0

    def weight(self, u: int, v: int) -> int:
        return self._adjacency_matrix[u][v]


if __name__ == "__main__":
    valve_list = ValveList.from_file("../input/day16sample.txt")
    for valve in valve_list:
        print(valve)

    costs = valve_list.graph.dijkstra(0)
    print(valve_list.graph)
    print(costs)
