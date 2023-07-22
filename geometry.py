import math


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = (x * x + y * y) ** 0.5

    def set_length(self, new_length):
        scale = new_length / self.length
        return Vector(self.x * scale, self.y * scale)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        if isinstance(other, Point):
            raise TypeError("Can't multiply points and vectors")
        else:
            return Vector(self.x * other, self.y * other)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        if isinstance(other, Point):
            return Point(other.x + self.x, other.y + self.y)
        else:
            return Vector(self.x + other, self.y + other)

    def __repr__(self):
        return f"[{self.x} {self.y}]"


class Point(tuple):

    def __new__(cls, x, y):
        return super(Point, cls).__new__(cls, tuple((x, y)))

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vector):
            return Point(self.x + other.x, self.y + other.y)
        if isinstance(other, Point):
            raise TypeError("Can't add points to points")
        else:
            raise TypeError("Can only add vectors to points")

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Point(self.x - other.x, self.y - other.y)
        if isinstance(other, Point):
            raise TypeError("Can't add points to points")
        else:
            raise TypeError("Can only add vectors to points")

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        else:
            raise TypeError(f"Can't equate to objects of type {type(other)}.")


class Coord(Point):
    def __init__(self, x, y):
        if not isinstance(x, int):
            raise ValueError("x coordinate value is not an integer")

        if not isinstance(y, int):
            raise ValueError("y coordinate value is not an integer")

        super(Coord, self).__init__(x, y)

    def __add__(self, other):
        if isinstance(other, Vector) and isinstance(other.x, int) and isinstance(other.y, int):
            return Coord(self.x + other.x, self.y + other.y)
        else:
            super(Coord, self).__add__(other)

    def __sub__(self, other):
        if isinstance(other, Vector) and isinstance(other.x, int) and isinstance(other.y, int):
            return Coord(self.x - other.x, self.y - other.y)
        else:
            super(Coord, self).__add__(other)
