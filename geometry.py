import math


class Vector(tuple):

    def __new__(cls, x, y):
        return super(Vector, cls).__new__(cls, tuple((x, y)))

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = (x * x + y * y) ** 0.5

    def scale_to(self, new_length):
        scale = new_length / self.length
        return Vector(self.x * scale, self.y * scale)

    def normalize(self):
        return self.scale_to(1)

    def perpendicular_clockwise(self):
        return Vector(self.y, -self.x)

    def perpendicular_counterclockwise(self):
        return Vector(-self.y, self.x)

    def rotate(self, angle):
        angle = math.radians(angle)
        x = self.x * math.cos(angle) - self.y * math.sin(angle)
        y = self.x * math.sin(angle) + self.y * math.cos(angle)

        return Vector(x, y)

    @classmethod
    def zero(cls):
        return cls(0, 0)

    @classmethod
    def up(cls):
        return cls(0, -1)

    @classmethod
    def down(cls):
        return cls(0, 1)

    @classmethod
    def left(cls):
        return cls(-1, 0)

    @classmethod
    def right(cls):
        return cls(1, 0)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        if isinstance(other, Point):
            raise TypeError("Can't add points to vectors! Add vectors to points instead.")
        else:
            return Vector(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        if isinstance(other, Point):
            raise TypeError("Can't subtract points from vectors! Subtract vectors to points instead.")
        else:
            return Vector(self.x + other, self.y + other)

    def __neg__(self):
        return Vector(- self.x, - self.y)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        if isinstance(other, Point):
            raise TypeError("Can't multiply vectors and points!")
        else:
            return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        if isinstance(other, Vector):
            return other.x * self.x + other.y * self.y
        if isinstance(other, Point):
            raise TypeError("Can't multiply points and vectors!")
        else:
            return Vector(other * self.x, other * self.y)

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        else:
            raise TypeError(f"Can't compare to objects of type {type(other)}!")

    def __gt__(self, other):
        if isinstance(other, Vector):
            return self.length > other.length
        else:
            raise TypeError(f"Can't compare to objects of type {type(other)}!")

    def __ge__(self, other):
        if isinstance(other, Vector):
            return self.length >= other.length
        else:
            raise TypeError(f"Can't compare to objects of type {type(other)}!")

    def __lt__(self, other):
        if isinstance(other, Vector):
            return self.length < other.length
        else:
            raise TypeError(f"Can't compare to objects of type {type(other)}!")

    def __le__(self, other):
        if isinstance(other, Vector):
            return self.length <= other.length
        else:
            raise TypeError(f"Can't compare to objects of type {type(other)}!")

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
            raise TypeError("Can't add points to points!")
        else:
            raise TypeError("Can only add vectors to points!")

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Point(self.x - other.x, self.y - other.y)
        if isinstance(other, Point):
            return Vector(self.x - other.x, self.y - other.y)
        else:
            raise TypeError("Can only subtract vectors or points from points!")

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        else:
            raise TypeError(f"Can't compare to objects of type {type(other)}!")
