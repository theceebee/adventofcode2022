

class Graph:

    @classmethod
    def from_file(cls, filename):
        with open(filename, "r") as fp:
            lines = [line.strip() for line in fp]

        n = len(lines) * len(lines[0])
        print(n)
        return cls(n)

    def __init__(self, number_of_vertices: int):
        self._number_of_vertices = number_of_vertices
        self._adjacency_list: list[set[int]] = []

    @property
    def number_of_vertices(self) -> int:
        return self._number_of_vertices

    def add_edge(self, u: int, v: int):
        self._adjacency_list[v].add(u)


if __name__ == "__main__":

    map_ = {"S": "a", "E": "z"}

    with open("../input/day12sample.txt", "r") as fp:
        lines = [line.strip() for line in fp]

    g = Graph(len(lines) * len(lines[0]))

    sentinel = 0
    start = 0
    end = 0
    for v in range(1, len(lines)):
        for u in range(1, len(lines[0])):
            value = lines[v - 1][u - 1]
            if value == "S":
                start = sentinel
            elif value == "E":
                end = sentinel
            right = lines[v - 1][u]
            down = lines[v][u - 1]

            if map_.get(right, right) - map_.get(value, value) <= 1:
                g.add_edge(u, v - 1)



            sentinel += 1

        # print("\n", end="")
