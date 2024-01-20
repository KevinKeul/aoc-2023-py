from collections import deque
from math import sqrt
from typing import List, Dict


class Vec2i:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def dot(self, o: 'Vec2i') -> int: return self.x * o.x + self.y * o.y

    def length(self) -> float: return sqrt(self.dot(self))

    def to(self, o: 'Vec2i') -> 'Vec2i': return Vec2i(o.x - self.x, o.y - self.y)

    def add(self, o: 'Vec2i') -> 'Vec2i': return Vec2i(self.x + o.x, self.y + o.y)

    def mul(self, a: int) -> 'Vec2i': return Vec2i(self.x * a, self.y * a)

    def mul_c(self, o: 'Vec2i') -> 'Vec2i': return Vec2i(self.x * o.x, self.y * o.y)

    def inv(self): return Vec2i(-self.x, -self.y)

    def __eq__(self, o: 'Vec2i') -> bool: return isinstance(o, Vec2i) and self.x == o.x and self.y == o.y

    def __hash__(self): return hash((self.x, self.y))

    def __str__(self): return f'Vec2i({self.x}, {self.y})'


RIGHT, DOWN, LEFT, UP = Vec2i(1, 0), Vec2i(0, -1), Vec2i(-1, 0), Vec2i(0, 1)
R, D, L, U = RIGHT, DOWN, LEFT, UP
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = Vec2i(1, 1), Vec2i(1, -1), Vec2i(-1, -1), Vec2i(-1, 1)
UR, DR, DL, UL = UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT
inv_dir: Dict[Vec2i, Vec2i] = {x: x.inv() for x in [UR, R, DR, D, DL, L, UL, U]}


class Field:
    def __init__(self, content: str, default_value: str = None,
                 split_lines=lambda x: x.split('\n'), split_values=lambda x: list(x)):
        self.cells: List[List[str]] = [split_values(x) for x in split_lines(content) if len(x) > 0]
        self.dims: Vec2i = Vec2i(len(self.cells[0]), len(self.cells))
        self.dir_x: Vec2i = Vec2i(1, 0)
        self.dir_y: Vec2i = Vec2i(0, -1)
        self.origin: Vec2i = Vec2i(0, self.dims.y - 1)
        self.default_value: str = default_value
        self.connections = None

    def get(self, x: int, y: int, outside_value: str = None) -> str:
        if x < 0 or x >= self.dims.x or y < 0 or y >= self.dims.y:
            return outside_value if outside_value else self.default_value
        coord: Vec2i = self.get_access_coord(x, y)
        return self.cells[coord.y][coord.x]

    #    def get(self, x: int = None, y: int = None, outside_value: str = None) -> str | List[str] | List[list[str]]:
    #        outside = outside_value if outside_value else self.default_value
    #        if x is not None and y is not None:
    #            c: Vec2i = self.get_access_coord(x, y)
    #            return self.cells[c.y][c.x] if 0 <= c.x < self.dims.x and 0 <= c.y < self.dims.y else outside
    #        if x is not None:
    #            cs: List[Vec2i] = [self.get_access_coord(x, y) for y in range(abs(self.dir_y.dot(self.dims)))]
    #            return [self.cells[c.y][c.x] if 0 <= c.x < self.dims.x and 0 <= c.y < self.dims.y else outside for c in cs]
    #        if y is not None:
    #            cs: List[Vec2i] = [self.get_access_coord(x, y) for x in range(abs(self.dir_x.dot(self.dims)))]
    #            return [self.cells[c.y][c.x] for c in cs if 0 <= c.x < self.dims.x and 0 <= c.y < self.dims.y]
    #        css: List[List[Vec2i]] = [[self.get_access_coord(x, y)
    #                                   for x in range(abs(self.dir_x.dot(self.dims)))]
    #                                  for y in range(abs(self.dir_y.dot(self.dims)))]
    #        return [[self.cells[c.y][c.x] for c in cs if 0 <= c.x < self.dims.x and 0 <= c.y < self.dims.y] for cs in css]

    def set(self, x: int, y: int, value: str) -> None:
        if x < 0 or x >= self.dims.x or y < 0 or y >= self.dims.y:
            return
        coord: Vec2i = self.get_access_coord(x, y)
        self.cells[coord.y][coord.x] = value

    def findall(self, to_find: str) -> List[Vec2i]:
        return [self.get_access_coord(x, y)
                for y, line in enumerate(self.cells)
                for x, char in enumerate(line)
                if char == to_find]

    def get_access_coord(self, x: int, y: int) -> Vec2i:
        return self.origin.add(self.dir_x.mul(x)).add(self.dir_y.mul(y))

    def __str__(self):
        return f'Field({self.dims.x} * {self.dims.y}, dir_x: {self.dir_x}, dir_y: {self.dir_y})'


def search_stack(start, is_goal, adjacent, done=lambda v, pre: v, breadth_first=False, return_history=False):
    q = deque([(start, None)])
    explored = {done(start, None)}
    parent = {start: None}
    while q:
        v, pre = q.popleft() if breadth_first else q.pop()
        if is_goal(v, pre):
            if return_history:
                p = v
                history = deque([p])
                while (p := parent[p]) and p != start:
                    history.appendleft(p)
                history.appendleft(start)
                return list(history)
            return v
        for a in adjacent(v, pre):
            if done(a, v) not in explored:
                explored.add(done(a, v))
                parent[a] = v
                q.append((a, v))
    return None
