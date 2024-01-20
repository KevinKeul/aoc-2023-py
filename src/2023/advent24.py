import re
import time
from typing import List, Tuple, Dict


class Exercise:
    def __init__(self, advent: int, input_file: str):
        self.input_file = input_file
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_two(self) -> int:
        return 0


class Vec3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, o: 'Vec3') -> float:
        return self.x * o.x + self.y * o.y + self.z * o.z

    def cross(self, o: 'Vec3') -> 'Vec3':
        return Vec3(self.y * o.z - o.y * self.z, self.z * o.x - o.z * self.x, self.x * o.y - o.x * self.y)  # right hand

    def to(self, o: 'Vec3') -> 'Vec3':
        return Vec3(o.x - self.x, o.y - self.y, o.z - self.z)

    def add(self, o: 'Vec3') -> 'Vec3':
        return Vec3(self.x + o.x, self.y + o.y, self.z + o.z)

    def mul(self, a: float) -> 'Vec3':
        return Vec3(self.x * a, self.y * a, self.z * a)

    def __str__(self):
        return f'Vec3({self.x}, {self.y}, {self.z})'


class Line:
    def __init__(self, p: Vec3, v: Vec3):
        self.p = p
        self.v = v

    @staticmethod
    def create_from_to(p1: Vec3, p2: Vec3) -> 'Line':
        return Line(p1, p1.to(p2))

    def calc(self, s: float) -> Vec3:
        return self.p.add(self.v.mul(s))

    def __str__(self):
        return f'Line({self.p} + s * {self.v})'


class LineFamily:
    def __init__(self, p: Line, v: Line):
        self.p = p
        self.v = v

    def calc_line(self, r: float):
        return Line(self.p.calc(r), self.v.calc(r))


class Plane:
    def __init__(self, p: Vec3, u: Vec3, v: Vec3):
        self.p = p
        self.u = u
        self.v = v
        self.n = u.cross(v)
        self.d = p.dot(self.n)

    def intersect(self, point: Vec3) -> float:
        return (self.p.to(point)).dot(self.n)

    def calc(self, s: float, t: float) -> Vec3:
        return self.p.add(self.u.mul(s)).add(self.v.mul(t))

    def intersect_line(self, line: Line) -> Vec3 | None:
        v_part = line.v.dot(self.n)
        if v_part == 0:
            return None
        s = (self.d - line.p.dot(self.n)) / v_part
        return line.calc(s)

    def __str__(self):
        return f'Plane({self.n.x}x + {self.n.y}y + {self.n.z}z = {self.d}) <==> Plane({self.p} + s * {self.u} + t * {self.v})'


class Hail:
    COUNT = 1

    def __init__(self, line: str):
        match = re.match('(-?\\d+),\\s*(-?\\d+),\\s*(-?\\d+)\\s*@\\s*(-?\\d+),\\s*(-?\\d+),\\s*(-?\\d+)', line)
        self.name = f'Hailstone {Hail.COUNT}'
        Hail.COUNT += 1
        self.p: Tuple[int, int, int] = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        self.v: Tuple[int, int, int] = (int(match.group(4)), int(match.group(5)), int(match.group(6)))

    def get_vectors(self) -> Tuple[Vec3, Vec3]:
        return Vec3(self.p[0], self.p[1], self.p[2]), Vec3(self.v[0], self.v[1], self.v[2])

    def get_normal2(self) -> Tuple[Tuple[int, int], int]:
        vx, vy, vz = self.v
        return (-vy, vx), -vy * self.p[0] + vx * self.p[1]

    def get_border_points2(self, min_: int, max_: int) -> List[Tuple[float, float]]:
        px, py, pz = self.p
        vx, vy, vz = self.v

        result: List[Tuple[float, float]] = []
        num_v1 = (min_ - px) / vx
        r1 = (min_, num_v1 * vy + py)
        if num_v1 > 0 and min_ <= r1[0] <= max_ and min_ <= r1[1] <= max_:
            result.append(r1)
        num_v2 = (max_ - px) / vx
        r2 = (max_, num_v2 * vy + py)
        if num_v2 > 0 and min_ <= r2[0] <= max_ and min_ <= r2[1] <= max_:
            result.append(r2)
        num_v3 = (min_ - py) / vy
        r3 = (num_v3 * vx + px, min_)
        if num_v3 > 0 and min_ <= r3[0] <= max_ and min_ <= r3[1] <= max_:
            result.append(r3)
        num_v4 = (max_ - py) / vy
        r4 = (num_v4 * vx + px, max_)
        if num_v4 > 0 and min_ <= r4[0] <= max_ and min_ <= r4[1] <= max_:
            result.append(r4)
        if min_ <= px <= max_ and min_ <= py <= max_:
            result.append((px, py))
        return result

    def __str__(self):
        return self.name


class Advent24(Exercise):
    def __init__(self, input_file: str):
        super().__init__(24, input_file)
        self.hails: List[Hail] = [Hail(line) for line in self.content.split('\n') if len(line) > 0]

    def part_one(self, min_: int, max_: int) -> int:
        result = 0
        border_points: Dict[Hail, List[Tuple[float, float]]] = {x: x.get_border_points2(min_, max_) for x in self.hails}
        for i in range(len(self.hails)):
            h1 = self.hails[i]
            for j in range(i + 1, len(self.hails)):
                h1 = self.hails[i]
                h2 = self.hails[j]
                if self.intersect(border_points, h1, h2) and self.intersect(border_points, h2, h1):
                    result += 1
        return result

    @staticmethod
    def intersect(border_points, h1, h2):
        normal, d = h1.get_normal2()
        above: bool = False
        under: bool = False
        for bp in border_points[h2]:
            if (normal[0] * bp[0]) + (normal[1] * bp[1]) >= d:
                above = True
            if (normal[0] * bp[0]) + (normal[1] * bp[1]) <= d:
                under = True
        if above and under:
            return True
        return False

    def part_two(self) -> int:
        p1, v1 = self.hails[0].get_vectors()
        p2, v2 = self.hails[1].get_vectors()
        p3, v3 = self.hails[3].get_vectors()
        p4, v4 = self.hails[4].get_vectors()

        # => all on one line (p1, s1, t1)
        e1 = Plane(p2, p1.to(p2), v2)
        s1 = e1.intersect_line(Line(p3, v3))
        es1 = Plane(p1, p1.to(s1), p1.to(s1).cross(v2))
        t1 = es1.intersect_line(Line(p2, v2))

        # => all on one line (p1_, s2, t2)
        p1_ = Line(p1, v1).calc(1)
        e2 = Plane(p2, p1_.to(p2), v2)
        s2 = e2.intersect_line(Line(p3, v3))
        es2 = Plane(p1_, p1_.to(s2), p1_.to(s2).cross(v2))
        t2 = es2.intersect_line(Line(p2, v2))

        # => all on one line (p1__, s3, t3)
        p1__ = Line(p1, v1).calc(2)
        e3 = Plane(p2, p1__.to(p2), v2)
        s3 = e3.intersect_line(Line(p3, v3))
        es3 = Plane(p1__, p1__.to(s3), p1__.to(s3).cross(v2))
        t3 = es3.intersect_line(Line(p2, v2))

        # => all on one line (p1___, s4, t4)
        p1___ = Line(p1, v1).calc(5)
        e4 = Plane(p2, p1___.to(p2), v2)
        s4 = e4.intersect_line(Line(p3, v3))
        es4 = Plane(p1___, p1___.to(s4), p1___.to(s4).cross(v2))
        t4 = es4.intersect_line(Line(p2, v2))

        # lf =
        lf = LineFamily(Line(p1, v1), Line.create_from_to(p1.to(t1), p1.add(v1).to(t2)))

        return super().part_two()


def main():
    start = time.time()
    exercise = Advent24('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one(7, 27)))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent24('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one(200000000000000, 400000000000000)))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))
    print(f'Elapsed time: {time.time() - start}')


if __name__ == '__main__':
    main()
