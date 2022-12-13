from __future__ import annotations

import abc
import re
from typing import Optional


class FSItem(metaclass=abc.ABCMeta):
    def __init__(self, name: str, parent: Optional[FSItem] = None):
        self.name = name
        self.parent = parent

    def __str__(self):
        return self.name

    @property
    @abc.abstractmethod
    def size(self) -> int:
        ...


class Dir(FSItem):
    def __init__(self, name: str, parent: Optional[FSItem] = None):
        super().__init__(name, parent)
        self._children = []

    @property
    def children(self):
        return self._children[:]

    @property
    def size(self):
        result = 0
        for child in self.children:
            result += child.size
        return result

    def add_child(self, child: FSItem):
        self._children.append(child)


class File(FSItem):
    def __init__(self, name: str, size: int, parent: Optional[FSItem] = None):
        super().__init__(name, parent)
        self._size = size

    @property
    def size(self):
        return self._size


def parse_input(input_: str) -> Dir:
    root = Dir(name="/")
    current = root

    with open(input_, "r") as fp:
        for line in fp:
            if match := re.match(r"^\$ cd (?P<name>/|\.\.|[^\s]+)", line):
                name = match.group("name")
                if name == "/":
                    current = root
                elif name == "..":
                    current = current.parent
                else:
                    dir_ = next(iter([c for c in current.children if isinstance(c, Dir) and c.name == name]), None)
                    if not dir_:
                        dir_ = Dir(name=name, parent=current)
                        current.add_child(dir_)
                    current = dir_

            elif line.startswith("$ ls"):
                continue

            else:
                if match := re.match(r"^dir (?P<name>[^\s]+)", line):
                    dir_ = next(
                        iter(
                            [
                                c
                                for c in current.children
                                if isinstance(c, Dir)
                                and c.name == match.group("name")
                            ]
                        ),
                        None,
                    )
                    if not dir_:
                        current.add_child(Dir(name=match.group("name"), parent=current))
                else:
                    size, name = line.strip().split(" ")
                    current.add_child(File(name=name, size=int(size), parent=current))

    return root


def puzzle1(root_: Dir) -> int:

    def recurse(dir_: Dir) -> int:
        result = 0
        if dir_.size <= 100000:
            result += dir_.size
        return result + sum([recurse(d) for d in dir_.children if isinstance(d, Dir)])

    # def print_recursively(fs_item: FSItem, indent=0) -> None:
    #     print("\t" * indent + f"- {fs_item} ({type(fs_item).__name__.lower()}, size={fs_item.size})")
    #     if isinstance(fs_item, Dir):
    #         for child_item in fs_item.children:
    #             print_recursively(child_item, indent + 1)

    return recurse(root_)


def puzzle2(root_: Dir) -> int:

    def recurse(dir_: Dir, results: Optional[list[int]] = None) -> list[int]:
        results_ = results or []
        if dir_.size + (70000000 - root_.size) >= 30000000:
            results_.append(dir_.size)
        for child in [c for c in dir_.children if isinstance(c, Dir)]:
            recurse(child, results_)
        return results_

    return min(recurse(root_))


if __name__ == "__main__":
    root = parse_input("../input/day7.txt")
    print(puzzle1(root))
    print(puzzle2(root))
